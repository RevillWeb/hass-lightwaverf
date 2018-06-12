import pika
from homeassistant.helpers.discovery import load_platform

#Requirements
REQUIREMENTS = ['pika==0.11.2']

DOMAIN = 'lightwaverf'

RABBIT_HOST = 'localhost'
RABBIT_PORT = 15672
RABBIT_QUEUE = 'LightwaveRF'
RABBIT_USERNAME = None
RABBIT_PASS = None
RF_LINK = '255.255.255.255'
HASS = None

def queue_command(msg):
    HASS.states.set('lightwaverf.LightwaveRF', f'Message: {msg}')
    if not RABBIT_USERNAME or not RABBIT_PASS:
        return False
    credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, RABBIT_PORT, '/', credentials))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=RABBIT_QUEUE, body=msg)
    connection.close()
    return True

def setup(hass, config):
    global HASS
    HASS = hass
    conf = config.get(DOMAIN)
    conf_rabbit_username = conf['rabbit_username']
    if conf_rabbit_username:
        global RABBIT_USERNAME
        RABBIT_USERNAME = conf_rabbit_username
    conf_rabbit_pass = conf['rabbit_pass']
    if conf_rabbit_pass:
        global RABBIT_PASS
        RABBIT_PASS = conf_rabbit_pass
    lights = conf['lights']
    load_platform(hass, 'light', DOMAIN, lights)
    hass.states.set('lightwaverf.LightwaveRF', f'Works! {RABBIT_USERNAME}, {RABBIT_PASS}')