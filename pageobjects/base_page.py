import logging
from utils import driver_path_resolver
from selenium.webdriver import Chrome
from tests_config import DEFAULT_IMPLICITLY_WAIT, BASE_URL

LOGGER = logging.getLogger(__name__)


class BasePage:

    def __init__(self, maximize_window=True, hide_cookie_notice=True):
        self.hide_cookie_notice = hide_cookie_notice
        self.driver = Chrome(driver_path_resolver.resolve_driver_path())
        self._hide_cookie_notice() if self.hide_cookie_notice else None
        self.driver.implicitly_wait(DEFAULT_IMPLICITLY_WAIT)
        self.driver.maximize_window() if maximize_window else None
        self.error = None

    def _hide_cookie_notice(self):
        """
        Hiding cookie notice object by adding hideCookieNotice cookie
        """
        LOGGER.info('Started hiding cookie notice')
        wrong_path = '404'
        if self.hide_cookie_notice:
            self.driver.get(BASE_URL + wrong_path)
            LOGGER.debug('Opened 404 page')
            self.driver.delete_all_cookies()
            LOGGER.debug('Deleted all cookies')
            cookie = {'name': 'hideCookieNotice', 'value': '1'}
            self.driver.add_cookie(cookie)
            LOGGER.debug('Added cookie {}'.format(cookie))
            LOGGER.info('Cookie notice hiding finished success')
        else:
            pass

    def get_last_error(self):
        return repr(self.error)
