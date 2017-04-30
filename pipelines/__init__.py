import importlib


class BasePipeline(object):
    url = None
    settings = {}
    sensor_value = None

    def __init__(self, settings, value):
        self.settings = settings
        self.sensor_value = value

    def send(self):
        raise NotImplementedError('Send is not implemented yet.')


class OutSensor(object):
    def do_send(self, **kwargs):
        if not getattr(self, 'pipelines'):
            raise AttributeError('Pipelines is not set.')

        for pipeline_name, pipeline_settings in self.pipelines.items():
            pipeline = importlib.import_module(f"pipelines.{pipeline_name}")

            value = getattr(self, pipeline_settings['source'])

            obj = pipeline.Pipeline(pipeline_settings, value)
            obj.send()