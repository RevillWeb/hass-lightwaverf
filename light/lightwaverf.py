#import 
import custom_components.lightwaverf as lightwaverf
import logging
import random
import sys

# 'switch' will receive discovery_info={'optional': 'arguments'}
# as passed in above. 'light' will receive discovery_info=None
def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Setup LightWave RF lights """        
    conf = config.get(lightwaverf.DOMAIN)
    rabbit_username = conf['rabbit_username']
    hass.states.set('lightwaverf.lights', f'Lights: {rabbit_username}')