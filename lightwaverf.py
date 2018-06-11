from homeassistant.helpers.discovery import load_platform

#Requirements
REQUIREMENTS = ['pika==0.11.2']

DOMAIN = 'lightwaverf'

def setup(hass, config):
    conf = config.get(DOMAIN)
    lights = conf['lights']
    load_platform(hass, 'light', DOMAIN, lights)
    hass.states.set('lightwaverf.LightwaveRF', f'Works! {lights}')