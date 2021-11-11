import socket
import time
import bisect


class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except:
            raise ClientError()

    def _read(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except:
                raise ClientError()
        data = data.decode('utf-8')
        return data

    def _send(self, data):
        try:
            self.connection.sendall(data)
        except:
            raise ClientError()

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        self._send(f"put {key} {value} {timestamp}\n".encode())
        string = self._read()
        if string == 'ok\n\n':
            return
        raise ClientError()

    def get(self, key):
        self._send(f"get {key}\n".encode())
        string = self._read()
        data = {}
        response_status, load = string.split("\n", 1)
        load = load.strip()
        if response_status != 'ok':
            raise ClientError()
        if load == '':
            return data
        try:
            for row in load.splitlines():
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                bisect.insort(data[key], ((int(timestamp), float(value))))
        except:
            raise ClientError()
        return data

    def close(self):
        try:
            self.connection.close()
        except:
            raise ClientError()