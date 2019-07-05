import logging
import platform
from tests_config import DRIVERS_PATH

LOGGER = logging.getLogger(__name__)


def resolve_driver_path():
    available_drivers = ['Darwin', 'Linux', 'Windows']
    os_name = platform.system()
    if os_name not in available_drivers:
        raise EnvironmentError('Unable to find driver for your system. Supported OS list: {}'.format(available_drivers))
    else:
        LOGGER.info('Resolved OS name to {}'.format(os_name))
        return DRIVERS_PATH[os_name]
