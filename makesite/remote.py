from os import environ
from .core import LOGGER

import ssh


class SSHClient:

    def __init__(self, host):
        self.host = host
        self.client = ssh.SSHClient()

    def connect(self):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(ssh.WarningPolicy)
        self.client.connect(self.host, port=22, username=environ.get('USER', 'root'))

    def close(self):
        self.client.close()

    def exec_command(self, command):
        _, stdout, stderr = self.client.exec_command(command)

        for line in stdout.readlines():
            LOGGER.debug("%s: %s" % (self.host, line))

        for line in stderr.readlines():
            LOGGER.error("%s: %s" % (self.host, line))
