#import 
import custom_components.lightwaverf as lightwaverf
import logging
import random
import sys
import pika
import voluptuous as vol

#import light info
from homeassistant.components.light import (Light, ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)
from homeassistant.const import (CONF_NAME, CONF_ID, CONF_LIGHTS)

#Requirements
REQUIREMENTS = ['pika==0.11.2']

#set brightness support
SUPPORT_LIGHTWAVE = (SUPPORT_BRIGHTNESS)

#logger?
_LOGGER = logging.getLogger(__name__)


# 'switch' will receive discovery_info={'optional': 'arguments'}
# as passed in above. 'light' will receive discovery_info=None
def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Setup LightWave RF lights """    
    devices = []
    lights = config[CONF_LIGHTS]
    for light in lights:
        deviceid = light[CONF_ID]
        name = light[CONF_NAME]
        device = LRFLight(name, False, deviceid, lightwaverf.CONF_LINK_IP, lightwaverf.CONF_RABBIT_HOST, lightwaverf.CONF_RABBIT_PORT, lightwaverf.CONF_RABBIT_QUEUE, lightwaverf.CONF_RABBIT_USERNAME, lightwaverf.CONF_RABBIT_PASS)
        devices.append(device)
    
    add_devices(devices)
    numLights = len(devices)
    hass.states.set('lightwaverf.lights', f'Number of lights: {numLights}')

#light class
class LRFLight(Light):
    """ LRF Light """
    def __init__(self, name, state, deviceid, rflink, rabbithost, rabbitport, rabbitque, rabbituname, rabbitpass, brightness=255):
        self._rabbithost = rabbithost
        self._rabbitport = rabbitport 
        self._rabbitque = rabbitque
        self._rabbituname = rabbituname
        self._rabbitpass = rabbitpass
        self._deviceid = deviceid
        self._rflink = rflink
        self._name = name
        self._state = state
        self._brightness = brightness

    @property
    def should_poll(self):
        """ No polling needed for a demo light. """
        return False        
        
    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name
        
    @property
    def rabbithost(self):
        """ Returns the host of the device if any. """
        return self._rabbithost
        
    @property
    def rabbitport(self):
        """ Returns the name of the device if any. """
        return self._rabbitport
        
    @property
    def rabbitque(self):
        """ Returns the que of the device if any. """
        return self._rabbitque
        
    @property
    def rabbituname(self):
        """ Returns the username of the device if any. """
        return self._rabbituname
        
    @property
    def rabbitpass(self):
        """ Returns the password of the device if any. """
        return self._rabbitpass
				
    @property
    def brightness(self):
        """ Brightness of this light between 0..255. """
        return self._brightness
    
    @property
    def deviceid(self):
        """ The Lightwave Device ID """
        return self._deviceid
    
    @property
    def is_on(self):
        """ True if device is on. """
        return self._state
    
    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_LIGHTWAVE

    def send_command(self, msg):
        credentials = pika.PlainCredentials(self._rabbituname, self._rabbitpass)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self._rabbithost, self._rabbitport, '/', credentials))
        channel = connection.channel()
        channel.basic_publish(exchange='', routing_key=self._rabbitque, body=msg)
        connection.close()

    def calculate_brightness(self, brightness):
        # the scale is 0 to 255 so we need to normalize to 0 to 100 first.
        old_range = 255 # 255 - 0 = 255
        new_range = 100 # 100 - 9 = 100
        new_value = (((brightness - 0) * new_range) / old_range)
        brightness32 = round(new_value * 0.32)
        return brightness32


    def turn_on(self, **kwargs):
        """ Turn the device on. """
        self._state = True

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]
            brightness_value = self.calculate_brightness(self._brightness)
            msg = '%s|666, !%sFdP%d|Lights %d|%s ' % (self._rflink, self._deviceid, brightness_value, brightness_value, self._name)
            self.send_command(msg)
        else:
            msg = '%s|666, !%sFdP32|Turn On|%s ' % (self._rflink, self._deviceid, self._name)
            self.send_command(msg)

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """ 
        msg = "%s|666, !%sF0|Turn Off|%s " % (self._rflink, self._deviceid, self._name)
        self.send_command(msg)
        self._state = False
        self.schedule_update_ha_state()