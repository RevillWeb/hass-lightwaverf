import pika
from homeassistant.helpers.discovery import load_platform

#Requirements
REQUIREMENTS = ['pika==0.11.2']

DOMAIN = 'lightwaverf'

RABBIT_HOST = 'localhost'
RABBIT_PORT = 5672
RABBIT_QUEUE = 'LightwaveRF'
RABBIT_USERNAME = None
RABBIT_PASS = None
LINK_IP = '255.255.255.255'
HASS = None

def queue_command(msg):
    if not RABBIT_USERNAME or not RABBIT_PASS:
        return False
    credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, RABBIT_PORT, '/', credentials))
    channel = connection.channel()
    payload = f'{LINK_IP}{msg}'
    channel.basic_publish(exchange='', routing_key=RABBIT_QUEUE, body=payload)
    connection.close()
    return True

def setup(hass, config):
    # Get the configuration for this platform
    conf = config.get(DOMAIN)
    # Get the rabbit username from the config file
    conf_rabbit_username = conf['rabbit_username']
    if conf_rabbit_username:
        global RABBIT_USERNAME
        RABBIT_USERNAME = conf_rabbit_username
    # Get the rabbit password from the config file
    conf_rabbit_pass = conf['rabbit_pass']
    if conf_rabbit_pass:
        global RABBIT_PASS
        RABBIT_PASS = conf_rabbit_pass
    # Get the link IP from the config if specified
    conf_link_ip = conf['link_ip']
    if conf_link_ip:
        global LINK_IP
        LINK_IP = conf_link_ip

    lights = conf['lights']
    if lights:
        load_platform(hass, 'light', DOMAIN, lights)
    
    return True