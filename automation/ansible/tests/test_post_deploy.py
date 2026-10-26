"""Execute the real student/Gitea orchestration against a local fixture API."""

import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile
import threading
import unittest
from urllib.parse import urlsplit

import yaml


COLLECTION = Path(__file__).resolve().parents[1]
REPO = COLLECTION.parents[1]


@unittest.skipUnless(shutil.which("ansible-playbook"), "ansible-playbook required")
class PostDeployTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="aia-post-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.collection = self.root / "automation/ansible"
        self.collection.mkdir(parents=True)
        shutil.copy(COLLECTION / "post_deploy.yml", self.collection)
        library = self.collection / "library"
        library.mkdir()
        (library / "aia_ctfd_flags.py").write_text('''from ansible.module_utils.basic import AnsibleModule
module = AnsibleModule(argument_spec={
    'url': {'type': 'str'}, 'username': {'type': 'str'},
    'password': {'type': 'str', 'no_log': True},
    'challenges': {'type': 'list', 'elements': 'dict', 'no_log': True},
    'validate_certs': {'type': 'bool'},
})
module.exit_json(changed=False, updated=0)
''')
        shutil.copytree(COLLECTION / "roles/configure_student", self.collection / "roles/configure_student")
        tasks = self.collection / "roles/instructor_config/tasks"
        tasks.mkdir(parents=True)
        (tasks / "oc_login.yml").write_text(yaml.safe_dump([
            {"ansible.builtin.debug": {"msg": "OpenShift interaction stub"}},
        ]))
        (tasks / "ctfd_config.yml").write_text(yaml.safe_dump([{
            "name": "Verify the CTFd handoff contains resolved flags for this student",
            "ansible.builtin.assert": {"that": [
                "ctfd_challenges | length == 25",
                "ctfd_challenges_advanced | length == 0",
                "ctfd_challenges[0].flags[0].content == 'synthetic-event-answer'",
                "gitea_username in ctfd_challenges[8].description",
            ]},
        }]))
        definitions = self.root / "ansible-testing/vars"
        definitions.mkdir(parents=True)
        source = (REPO / "ansible-testing/vars/challenges.yml").read_text()
        (definitions / "challenges.yml").write_text(source)
        keys = set(re.findall(r"ctfd_flags\.(\w+)", source))
        self.flags = definitions / "flags.yml"
        self.flags.write_text(yaml.safe_dump({"ctfd_flags": {key: "synthetic-event-answer" for key in keys}}))
        self.users = {"instructor-one": secrets.token_hex(12), "instructor-two": secrets.token_hex(12)}
        self.guides = {}
        self.forks = {(user, repo) for user in self.users for repo in ("ansible-survival-kit", "aia-instructor")}
        self.forks.remove(("instructor-two", "ansible-survival-kit"))
        self.writes = []
        self.requests = []
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def handle_request(self):
                auth = self.headers.get("Authorization", "").removeprefix("Basic ")
                user, password = base64.b64decode(auth).decode().split(":", 1)
                fixture.requests.append((self.command, self.path, user))
                code, data = 200, {}
                path = urlsplit(self.path).path.split("/")
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                if fixture.users.get(user) != password:
                    code = 401
                elif self.path == "/api/v1/user":
                    data = {"login": user}
                elif self.command == "POST" and path[-1] == "forks":
                    fixture.forks.add((user, path[-2]))
                    fixture.writes.append((user, "fork"))
                    code = 202
                elif "contents" in path:
                    if self.command == "GET":
                        if user in fixture.guides:
                            data = {"sha": "file-sha", "content": base64.b64encode(fixture.guides[user].encode()).decode()}
                        else:
                            code = 404
                    else:
                        if self.command == "PUT" and body.get("sha") != "file-sha":
                            code = 409
                        else:
                            fixture.guides[user] = base64.b64decode(body["content"]).decode()
                            fixture.writes.append((user, "guide"))
                            code = 201 if self.command == "POST" else 200
                elif "branches" in path:
                    data = {"name": path[-1]}
                elif len(path) == 6 and path[3] == "repos":
                    if (user, path[-1]) not in fixture.forks or path[-2] != user:
                        code = 404
                    else:
                        data = {"name": path[-1], "owner": {"login": user}}
                else:
                    code = 404
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())

            do_GET = do_POST = do_PUT = handle_request

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.url = f"http://127.0.0.1:{server.server_port}"
        hosts = {}
        for user, password in self.users.items():
            guid = user.removeprefix("instructor-")
            hosts[user] = {
                "guid": guid, "gitea_url": self.url, "gitea_username": user, "gitea_password": password,
                "ctfd_admin_username": "admin", "ctfd_admin_password": password,
                "student_name": "lab-user", "instructor": {"name": user},
                "aia_student": {"guid": guid, "ctfd_username": "lab-user", "ctfd_url": f"https://ctfd-{guid}.example.test",
                                "gitea_url": self.url, "aap_url": "https://aap.example.test", "aap_username": user,
                                "devspaces_url": "https://devspaces.example.test", "managed_node": "rhel"},
            }
        self.inventory = self.root / "students.json"
        self.inventory.write_text(json.dumps({"all": {"children": {"aia_students": {
            "hosts": hosts, "vars": {"ansible_connection": "local", "ansible_python_interpreter": "/usr/bin/python3",
                                      "aia_kubeconfig": str(self.root / "kubeconfig")},
        }}}}))
        self.config = self.root / "ansible.cfg"
        self.config.write_text("[defaults]\nstdout_callback=default\n")

    def run_playbook(self):
        result = subprocess.run(["ansible-playbook", "-i", str(self.inventory), str(self.collection / "post_deploy.yml")],
                                env=dict(os.environ, ANSIBLE_CONFIG=str(self.config), ANSIBLE_NOCOLOR="1"),
                                capture_output=True, text=True, timeout=90)
        return result.returncode, result.stdout + result.stderr

    def test_two_students_link_to_their_own_repos_and_rerun_does_not_commit(self):
        rc, output = self.run_playbook()
        self.assertEqual(rc, 0, output)
        self.assertEqual(len(self.guides), 2)
        for user, content in self.guides.items():
            self.assertIn(self.url + "/" + user + "/ansible-survival-kit", content)
            other = next(name for name in self.users if name != user)
            self.assertNotIn(other, content)
            self.assertNotIn(self.users[user], content)
        writes = list(self.writes)
        rc, output = self.run_playbook()
        self.assertEqual(rc, 0, output)
        self.assertEqual(self.writes, writes)

    def test_missing_event_flag_stops_before_any_service_request(self):
        self.flags.write_text("ctfd_flags: {}\n")
        rc, output = self.run_playbook()
        self.assertNotEqual(rc, 0, output)
        self.assertEqual(self.requests, [])


if __name__ == "__main__":
    unittest.main()
