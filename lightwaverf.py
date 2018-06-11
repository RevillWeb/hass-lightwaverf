import voluptuous as vol
#import validation
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.components.light import (PLATFORM_SCHEMA)
#import schema known light config
from homeassistant.const import (CONF_NAME, CONF_ID, CONF_LIGHTS)

DOMAIN = 'lightwaverf'

#set defaults incase of user error
DEFAULT_NAME = 'Hub 1'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 15672
DEFAULT_STATE = False
DEFAULT_RFLINK = '255.255.255.255'

#assign non known config
#rabbitmq
CONF_RABBIT_HOST = 'localhost'
CONF_RABBITQUE = 'rabbitque'
CONF_RABBITUNAME = 'rabbituname'
CONF_RABBITPASS = 'rabbitpass'
CONF_RABBITPORT = 'rabbitport'
CONF_RFLINK = 'rflink'

#validate user config
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_RABBIT_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_RABBITPORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_RABBITQUE): cv.string,
    vol.Required(CONF_RABBITUNAME): cv.string,
    vol.Required(CONF_RABBITPASS): cv.string,
    vol.Optional(CONF_LIGHTS, default=[]):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ID): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_RFLINK, default=DEFAULT_RFLINK): cv.string,
            })
        ])
})

def setup(hass, config):

    load_platform(hass, 'light', DOMAIN)
    load_platform(hass, 'switch', DOMAIN)
    hass.states.set('lightwaverf.LightwaveRF', f'Works! {CONF_RABBITHOST}')