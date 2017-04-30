import requests

from pipelines import BasePipeline


class Pipeline(BasePipeline):
    """ ESPMeter project backend. """

    endpoint = 'http://34.208.165.234:8000/api/'
    log_device = 'sensors'
    log_all = 'logs'

    LOG_DEVICE = 'device'
    LOG_ALL = 'all'


    def send(self):
        data = {
            'sensor': self.settings['sensor_id'],
            'value': self.sensor_value
        }

        response = requests.post(f"{self.endpoint}{self.log_all}/", data, auth=self.settings['auth'])