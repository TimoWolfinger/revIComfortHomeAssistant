import socket
from io import BytesIO
from urllib import parse
class iComfortAPI:
    """provide handlers for iComfort API"""

    def __init__(self,
    coordinatorIp ) -> None:
        """ intitialize api"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._coordinatorIp = coordinatorIp
        self._socket.connect( coordinatorIp, 5555)
        self._socket.close()

    def getDevices(self):
        devicesList = []
        self._socket.connect(self._coordinatorIp, 5555)
        self._socket.sendall(b'G')
        data = self._socket.recv(1024)
        self._socket.close()
        buffer = BytesIO()
        buffer.write(data)
        buffer.seek(0)
        start_index = 0
        for line in buffer:
            start_index += len(line)
            """ parse line """
            if (line[0:1] == 'G'):
                devicesList.append(line[3:12])
            elif (line[0:1] == 'C'):
                """ initialize after pressing learn"""
                self.switch_on(line[3:12])
                self.switch_off(line[3:12])
                devicesList.append(line[3:12])
        return devicesList

    def getInfo(self):
        info = {}
        self._socket.connect(self._coordinatorIp, 5555)
        self._socket.sendall(b'I')
        data = self._socket.recv(1024)
        info = parse.parse_qs(data)
        """I?g=60&i=192.168.0.176&j=255.255.0.0&n=192.168.3.142&o=255.255.255.0&p=192.168.3.254&q=192.168.3.254&r=0.0.0.0&s=1&t=1672606306&u=F8-D7-BF-00-1E-49&v=1.1&w=1&x=REV iComfort"""
        return info
    
    def switch_on(self, deviceId) -> bool:
        self._socket.connect(self._coordinatorIp, 5555)
        self._socket.sendall(b'S?a=' + deviceId + '&d=3F')
        res = self._socket.recv(200)
        self._socket.close()
        buffer = BytesIO()
        buffer.write(res)
        buffer.seek(0)
        startIndex = 0
        for line in res:
            startIndex += len(line)
            if (line[0:1] == 'F'):
                return False
        return True

    def get_device_status(self, deviceId):
        self._socket.connect(self._coordinatorIp, 5555)
        res = self._socket.recv(200)
        for line in res:
            parsed  = parse.parse_qs(line)
            if parsed.a is deviceId:
                return line.d == "3F"


    def switch_off(self, deviceId) -> bool:
        self._socket.connect(self._coordinatorIp, 5555)
        self._socket.sendall(b'S?a=' + deviceId + '&d=00')
        res = self._socket.recv(200)
        self._socket.close()
        buffer = BytesIO()
        buffer.write(res)
        buffer.seek(0)
        startIndex = 0
        for line in res:
            startIndex += len(line)
            if (line[0:1] == 'F'):
                return False
        return True