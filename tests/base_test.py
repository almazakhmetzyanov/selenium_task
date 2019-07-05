import logging
from pageobjects.careers_page.careers_page import CareersPage

LOGGER = logging.getLogger(__name__)


class BaseTest:
    """
    Base tests class.
    """
    careers_page = CareersPage()

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        cls.careers_page.driver.quit()
