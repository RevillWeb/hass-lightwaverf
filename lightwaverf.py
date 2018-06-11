import voluptuous as vol
#import validation
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.components.light import (PLATFORM_SCHEMA)
#import schema known light config
from homeassistant.const import (CONF_NAME, CONF_ID, CONF_LIGHTS)

#Requirements
REQUIREMENTS = ['pika==0.11.2']

DOMAIN = 'lightwaverf'

#set defaults incase of user error
DEFAULT_NAME = 'Hub 1'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 5672
DEFAULT_STATE = False
DEFAULT_LINK_IP = '255.255.255.255'

#assign non known config
#rabbitmq
CONF_RABBIT_HOST = 'rabbit_host'
CONF_RABBIT_QUEUE = 'rabbit_queue'
CONF_RABBIT_USERNAME = 'rabbit_username'
CONF_RABBIT_PASS = 'rabbit_pass'
CONF_RABBIT_PORT = 'rabbit_port'
CONF_LINK_IP = 'link_ip'

#validate user config
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_RABBIT_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_RABBIT_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_RABBIT_QUEUE): cv.string,
    vol.Required(CONF_RABBIT_USERNAME): cv.string,
    vol.Required(CONF_RABBIT_PASS): cv.string,
    vol.Optional(CONF_LIGHTS, default=[]):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ID): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_LINK_IP, default=DEFAULT_LINK_IP): cv.string,
            })
        ])
})

def setup(hass, config):
    load_platform(hass, 'light', DOMAIN)
    #load_platform(hass, 'switch', DOMAIN)
    conf = config.get(CONF_RABBIT_PASS)
    hass.states.set('lightwaverf.LightwaveRF', f'Works! {conf}')