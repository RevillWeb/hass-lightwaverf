from homeassistant.helpers.discovery import load_platform

#Requirements
REQUIREMENTS = ['pika==0.11.2']

DOMAIN = 'lightwaverf'

def setup(hass, config):
    load_platform(hass, 'light', DOMAIN)
    conf = config.get(DOMAIN)
    hass.states.set('lightwaverf.LightwaveRF', f'Works! {conf}')