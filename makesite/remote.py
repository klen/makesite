from .core import LOGGER
from .settings import USER

import ssh


class SSHClient:

    def __init__(self, host):
        self.user, self.host = host_params(host)
        self.client = ssh.SSHClient()

    def connect(self):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(ssh.WarningPolicy())
        self.client.connect(self.host, port=22, username=self.user)

    def close(self):
        self.client.close()

    def exec_command(self, command):
        _, stdout, stderr = self.client.exec_command(command)

        for line in stdout.readlines():
            LOGGER.debug("%s: %s" % (self.host, line))

        for line in stderr.readlines():
            LOGGER.error("%s: %s" % (self.host, line))


def host_params(host):
    user, _, host = host.partition('@')
    if not host:
        host = user
        user = USER
    return user, host
