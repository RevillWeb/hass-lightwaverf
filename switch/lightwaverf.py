import custom_components.lightwaverf as lightwaverf

# 'switch' will receive discovery_info={'optional': 'arguments'}
# as passed in above. 'light' will receive discovery_info=None
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Your switch/light specific code."""
    # You can now use hass.data[myflashyhub.DATA_MFH]