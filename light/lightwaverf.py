import logging
import random
import sys
import custom_components.lightwaverf as lightwaverf
from homeassistant.components.light import (Light, ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS)
SUPPORT_LIGHTWAVE = (SUPPORT_BRIGHTNESS)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Setup LightWave RF lights """        
    lightwaverf.queue_command("TEST123")
    hass.states.set('lightwaverf.lights', f'Lights: {lightwaverf.RABBIT_PASS}')
    devices = []
    for light in discovery_info:
        id = light['id']
        name = light['name']
        device = LWRFLight(id, name)
        devices.append(device)
    
    add_devices(devices)
    return True


# LightwaveRF Light class
class LWRFLight(Light):
    """ LWRF Light Class """
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._state = False
        self._brightness = 255

    @property
    def should_poll(self):
        """ No polling needed for a demo light. """
        return False        
        
    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name
				
    @property
    def brightness(self):
        """ Brightness of this light between 0..255. """
        return self._brightness
    
    @property
    def deviceid(self):
        """ The LightwaveRF Device ID """
        return self._id
    
    @property
    def is_on(self):
        """ True if device is on. """
        return self._state
    
    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_LIGHTWAVE

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
            msg = '|666, !%sFdP%d|Lights %d|%s ' % (self._id, brightness_value, brightness_value, self._name)
            lightwaverf.queue_command(msg)
        else:
            msg = '|666, !%sFdP32|Turn On|%s ' % (self._id, self._name)
            lightwaverf.queue_command(msg)

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """ 
        msg = "|666, !%sF0|Turn Off|%s " % (self._id, self._name)
        lightwaverf.queue_command(msg)
        self._state = False
        self.schedule_update_ha_state()