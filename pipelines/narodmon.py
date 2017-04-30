import socket

from pipelines import BasePipeline

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Pipeline(BasePipeline):
    """ Narodmon.ru stats backend. """

    endpoint = 'narodmon.ru'
    port = 8283

    def send(self):
        sock = socket.socket()

        try:
            sock.connect((self.endpoint, self.port))

            data = f"#{self.settings['device_id']}\n#{self.settings['sensor_id']}#{self.sensor_value}\n##"

            sock.send(bytes(data, 'utf-8'))

            response = sock.recv(1024)

            sock.close()
        except socket.error as e:
            logging.error(e)