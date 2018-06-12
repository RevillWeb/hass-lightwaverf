import logging
import random
import sys
import custom_components.lightwaverf as lightwaverf
from homeassistant.helpers.entity import (ToggleEntity)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Setup LightWave RF Switches """        
    devices = []
    for switch in discovery_info:
        id = switch['id']
        name = switch['name']
        device = LWRFSwitch(id, name)
        devices.append(device)
    
    add_devices(devices)
    return True


# LightwaveRF Light class
class LWRFSwitch(ToggleEntity):
    """ LWRF Light Class """
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._state = False

    @property
    def should_poll(self):
        """ No polling needed for a demo light. """
        return False        
        
    @property
    def name(self):
        """ Returns the name of the device if any. """
        return self._name
    
    @property
    def deviceid(self):
        """ The LightwaveRF Device ID """
        return self._id
    
    @property
    def is_on(self):
        """ True if device is on. """
        return self._state
    
    def turn_on(self, **kwargs):
        """ Turn the device on. """        
        msg = '|666, !%sF1|Turn On|%s ' % (self._id, self._name)
        lightwaverf.queue_command(msg)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """ Turn the device off. """ 
        msg = "|666, !%sF0|Turn Off|%s " % (self._id, self._name)
        lightwaverf.queue_command(msg)
        self._state = False
        self.schedule_update_ha_state()