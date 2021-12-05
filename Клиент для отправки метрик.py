import socket, time


class ClientError(Exception):
    pass

class Client:
    def __init__(self, host, port, timeout = None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.connection = socket.create_connection((self.host, self.port), self.timeout)
        except socket.error as error:
            raise ClientError(error)

    def put(self, key, value, timestamp = None):
        timestamp = timestamp or int(time.time())
        data = 'put {} {} {}\n'.format(key, value, timestamp).encode('utf8')
        self.connection.sendall(data)
        response = self.connection.recv(1024)
        if 'ok' not in str(response):
            raise ClientError

    def get(self, key):
        dict = {}
        data = 'get {}\n'.format(key).encode('utf8')
        try:
            self.connection.sendall(data)
            response = self.connection.recv(1024)
            if 'ok' not in str(response):
                raise ClientError

            response = str(response).strip('\n').split('\\n')

            for i in range(len(response)):
                if response[i] != '' and response[i] != "'" and response[i] != "b'ok":
                    metrics = response[i].split(' ')
                    try:
                        metrics[1] = float(metrics[1])
                        metrics[2] = int(metrics[2])
                        if metrics[0] not in dict:
                            dict[metrics[0]]=list()
                            dict[metrics[0]].append((metrics[2], metrics[1]))
                        else:
                            dict[metrics[0]].append((metrics[2], metrics[1]))
                    except:
                        raise ClientError

            for value in dict:
                dict[value].sort()

        except Exception as error:
            raise ClientError(error)
        
        return dict

    def close(self):
        try:
            self.connection.close()
        except socket.error as error:
            raise ClientError(error)

if __name__ == '__main__':
    pass