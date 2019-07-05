import logging
from time import sleep
from pageobjects.base_page import BasePage
from pageobjects.careers_page.locators import locators
from tests_config import BASE_URL

LOGGER = logging.getLogger(__name__)


class CareersPage(BasePage):

    def go_to_careers_page(self):
        """
        Open careers page method
        """
        self.driver.get(BASE_URL)
        LOGGER.info('Opened page {}'.format(BASE_URL))

    def choose_vacancy_country(self, country_name='Romania'):
        """
        Choose country filter language
        :param country_name: Ex. Romania
        """
        self.driver.find_element_by_id(locators['country-element']).click()
        LOGGER.info('Clicked on {}'.format(locators['country-element']))

        elements = self.driver.find_elements_by_class_name(locators['selecter-item'])
        LOGGER.debug('Got elements {}. {}'.format(locators['country-element'], elements))

        for element in elements:
            if element.get_attribute('data-value') == country_name:
                LOGGER.debug('Found {} button'.format(country_name))
                element.click()
                LOGGER.info('Clicked on {} button'.format(country_name))
                break

    def choose_vacancy_language(self, language='english'):
        """
        Choose vacancy filter language
        :param language: english, or russian or german
        """
        available_languages = {'english': 'ch-7',
                               'russian': 'ch-22',
                               'german': 'ch-11'}

        if language not in available_languages.keys():
            raise NameError(
                '{} language is not available. Available languages: {}'.format(language, available_languages.keys()))
        LOGGER.debug('Chosen language is {}'.format(language))

        self.driver.find_element_by_id(locators['language']).click()
        LOGGER.info('Clicked on {} button'.format(locators['language']))

        elements = self.driver.find_elements_by_class_name(locators['controls-checkbox'])
        LOGGER.debug('Got elements {}. {}'.format(locators['controls-checkbox'], elements))
        for element in elements:
            if element.get_attribute('for') == available_languages[language]:
                LOGGER.debug('Found {} button'.format(language))
                element.click()
                LOGGER.info('Clicked on {} button'.format(language))

    def click_to_apply_filter_button(self):
        """
        Find and click to apply filter button method
        """
        self.driver.find_element_by_class_name(locators['selecter-fieldset-submit']).click()
        LOGGER.info('Clicked on {} button'.format(locators['selecter-fieldset-submit']))

    def click_show_all_jobs_button(self):
        """
        Find and click to show all jobs button method
        """
        self.driver.find_element_by_class_name(locators['content-loader-button']).click()
        LOGGER.info('Clicked on {} button'.format(locators['content-loader-button']))

    def get_current_vacancy_counters(self):
        """
        Get current vacancy counters.
        :return: Tuple with count from jobs founder element and vacancy blocks on a page
        """
        LOGGER.info('Getting current vacancy counters...')
        elements = self.driver.find_elements_by_class_name(locators['text-center-md-down'])
        LOGGER.debug('Got elements {}. {}'.format(locators['text-center-md-down'], elements))
        vacancy_blocks = len(self.driver.find_elements_by_class_name(locators['vacancies-blocks-item']))
        LOGGER.debug('Got {} vacancy blocks'.format(vacancy_blocks))
        for element in elements:
            if element.tag_name == 'h3':
                LOGGER.info(
                    'Extracted counts vacancy counters: {} {}'.format(element.text.split(' ')[0], vacancy_blocks))
                return element.text.split(' ')[0], vacancy_blocks

    def wait_for_all_vacancy_blocks_count_equal_expected(self, start_vacancy_counts, expected_count, waiting_time=30):
        """
        This method at start checking what vacancy count updated and then checking vacancy blocks count
        :param start_vacancy_counts: tuple with count from jobs founder element and vacancy blocks
        :param expected_count: expected vacancy blocks count
        :param waiting_time: waiting iterations
        """
        start_vacancy_count_text, start_vacancy_count_blocks = start_vacancy_counts
        LOGGER.info(
            'Started waiting for vacancy blocks count equal to expected process. Start counts {} {}'.format(
                start_vacancy_count_text,
                start_vacancy_count_blocks))
        for i in range(waiting_time):
            vacancy_count_text, vacancy_count_blocks = self.get_current_vacancy_counters()
            if start_vacancy_count_text != vacancy_count_text:
                self.click_show_all_jobs_button()
                LOGGER.info('Vacancy list updated success. Clicked on show all jobs button')
                break
            else:
                LOGGER.debug('Try #{}. Vacancy list does not currently updated')
                sleep(1)

        vacancy_count_blocks = int()
        for i in range(waiting_time):
            vacancy_count_text, vacancy_count_blocks = self.get_current_vacancy_counters()
            if vacancy_count_blocks == expected_count:
                LOGGER.info('Vacancy blocks list updated success. ALL OK')
                return True
            else:
                LOGGER.debug('Try #{}. Vacancy blocks list does not currently updated')
                sleep(1)
        self.error = 'Expected vacancy count {} but received {}'.format(expected_count, vacancy_count_blocks)
        return False
