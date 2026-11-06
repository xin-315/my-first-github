import socket


def pytest_configure(config):
    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def blocked(self, address):
        if isinstance(address, tuple) and address[0] in ('127.0.0.1', '::1', 'localhost'):
            return original_connect(self, address)
        raise RuntimeError('External network disabled for the chapter 6 test audit')

    def blocked_ex(self, address):
        if isinstance(address, tuple) and address[0] in ('127.0.0.1', '::1', 'localhost'):
            return original_connect_ex(self, address)
        raise RuntimeError('External network disabled for the chapter 6 test audit')

    socket.socket.connect = blocked
    socket.socket.connect_ex = blocked_ex
