#!/usr/bin/python2.7

import os, sys, getopt, argparse
from owsensors import get_owobject

def main(argv):
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    parser.add_argument(
        'sensor',
        help='sensor name'
    )
    parser.add_argument(
        'action',
        help='action to do'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        help='port integer'
    )
    parser.add_argument(
        '-c', '--config',
        help='config file'
    )
    
    args = parser.parse_args()
    
    sensor_name = args.sensor.upper()
    action = args.action.upper()
    config_filename = args.config or 'owconfig.conf'
    port = args.port
    
    # Check for existing config file
    if not os.path.exists(config_filename):
        raise IOError(
            'Configuration file {} does not exist!'.format(config_filename)
        )
        
    
    config = {}
    execfile(config_filename, config) 
    
    if not config.get('OWSENSOR'):
        raise NameError('Configuration file is not correct!')

    sensors = {}

    for sensor in config['OWSENSOR']:
        obj = get_owobject(sensor.get('address'))
        sensors[sensor['name'].upper()] = obj(**sensor)

    sensor = sensors.get(sensor_name)

    if not sensor:
        print 'Sensor does not exist'

    print sensor.do(action, port)


if __name__ == "__main__":
   main(sys.argv[1:])
