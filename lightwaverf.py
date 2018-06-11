from homeassistant.helpers.discovery import load_platform

DOMAIN = 'lightwaverf'

def setup(hass, config):

    load_platform(hass, 'light', DOMAIN)
    load_platform(hass, 'switch', DOMAIN)
    hass.states.set('lightwaverf.LightwaveRF', 'Works!')