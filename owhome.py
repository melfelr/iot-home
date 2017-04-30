#!/usr/bin/python

import os, sys, getopt, argparse
from owsensors import get_owobject

SENSOR_ALL = 'ALL'
SILENT_ACTIONS = 'SEND'

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

    with open(config_filename) as config_file:
        config_code = compile(config_file.read(), config_filename, 'exec')
        exec(config_code, config)
    
    if not config.get('OWSENSOR'):
        raise NameError('Configuration file is not correct!')

    sensors = {}

    for sensor in config['OWSENSOR']:
        obj = get_owobject(sensor.get('address'))
        sensors[sensor['name'].upper()] = obj(**sensor)

    if sensor_name.upper() != SENSOR_ALL:
        sensors = {sensor_name: sensors.get(sensor_name)}

    if not sensors:
        print(f"Sensor {sensor_name} does not exist.")

    fail_silently = action.upper() in SILENT_ACTIONS

    for name, sensor in sensors.items():
        print(sensor.do(action=action, port=port, fail_silently=fail_silently))


if __name__ == "__main__":
   main(sys.argv[1:])
