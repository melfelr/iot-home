import os, re
from time import sleep


DS18B20 = '28' # Programmable resolution digital thermometer
DS2413 = '3A' # Dual channel addressable switch


class OWSensor(object):
    """ A basic 1-wire sensor representation """
    
    type = None
    name = None
    address = None
    description = None
    device = None
    
    def __init__(self, name, address, device, description=None):
        self.name = name
        self.address = address
        self.device = device
        self.description = description
    
    def do(self, action, port=None):
        if not self.ACTIONS:
            raise AttributeError('Actions is not set')
        
        action_func = getattr(self, 'do_{}'.format(action.lower()))
        
        if not callable(action_func):
            raise AttributeError('Action is not exist')
        
        return action_func(port=port)


class OWTemperatureSensor(OWSensor):
    """ 1-wire programmable resolution digital thermometer representation """
    
    type = DS18B20
    
    ACTIONS = ('VALUE', )
    
    @property
    def filename(self):
        return os.path.join(self.device, self.address, "temperature")
    
    @property
    def temperature(self):
        sensor_filename = self.filename
        
        value = None
        
        if os.path.exists(sensor_filename):
            sensor_file = open(sensor_filename, 'r')
            value = sensor_file.read()
            sensor_file.close()
        
        return value
    
    def do_value(self, **kwargs):
        return self.temperature


class OWIOSensor(OWSensor):
    """ 1-wire dual channel addressable switch representation """
    
    type = DS2413
    PIOA, PIOB = range(1, 3)
    
    TURN_ON_SEQ = '1'
    TURN_OFF_SEQ = '0'
    
    PORTS = {PIOA: 'PIO.A', PIOB: 'PIO.B'}
    SEQUENCES = (TURN_ON_SEQ, TURN_OFF_SEQ)
    
    ACTIONS = ('ONCE', 'ON', 'OFF')
    
    DEFAULT_PORT = None
    
    def __init__(self, **kwargs):
        self.DEFAULT_PORT = kwargs.pop('default_port')
        super(OWIOSensor, self).__init__(**kwargs)
    
    def filename(self, port):
        return os.path.join(
            self.device, 
            self.address, 
            OWIOSensor.PORTS.get(port)
        )
    
    def write_sensor(self, port, seq):
        # Check for existing port
        if port not in OWIOSensor.PORTS:
            raise AttributeError('Port doesn\'t exist')
        
        if seq not in OWIOSensor.SEQUENCES:
            raise AttributeError('Sequency is not allowed')
        
        sensor_filename = self.filename(port)
        
        sensor_file = open(sensor_filename, 'w')
        sensor_file.write(seq)
        sensor_file.close()
    
    def turn_on(self, port):
        return self.write_sensor(
            port=port,
            seq=OWIOSensor.TURN_ON_SEQ
        )
    
    def turn_off(self, port):
        return self.write_sensor(
            port=port,
            seq=OWIOSensor.TURN_OFF_SEQ
        )
    
    def turn_on_once(self, port):
        self.turn_on(port)
        sleep(0.5)
        self.turn_off(port)
    
    def do(self, action, port=None):
        if not port:
            port = self.DEFAULT_PORT
        
        if not port:
            raise AttributeError('Port is not set')
        
        return super(OWIOSensor, self).do(action, port)
    
    def do_once(self, port=None):
        self.turn_on_once(port)
        
        return 'Set {}/{} to {} once'.format(
            self.address,
            OWIOSensor.PORTS.get(port), 
            OWIOSensor.TURN_ON_SEQ
        )
    
    def do_on(self, port):
        self.turn_on(port)
        
        return 'Set {}/{} to {} on'.format(
            self.address,
            OWIOSensor.PORTS.get(port), 
            OWIOSensor.TURN_ON_SEQ
        )
    
    def do_off(self, port):
        self.turn_off(port)
        
        return 'Set {}/{} to {} off'.format(
            self.address,
            OWIOSensor.PORTS.get(port), 
            OWIOSensor.TURN_OFF_SEQ
        )
        

OWSENSOR_OBJ = {
    DS18B20: OWTemperatureSensor,
    DS2413: OWIOSensor
}


def get_owobject(address):
    match = re.search(r'(\w+)\.', address, re.I)
    
    if match:
        family_code = match.group(1)
        
        obj = OWSENSOR_OBJ.get(family_code)
        
        if obj:
            return obj
        
        raise NotImplementedError(
            'Family code {} is not supported yet.'.format(family_code)
        )
    
    raise LookupError('Device address seems invalid, can\'t find family code.')
