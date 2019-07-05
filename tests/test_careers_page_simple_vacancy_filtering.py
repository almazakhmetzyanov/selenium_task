import pytest
import logging
from tests.base_test import BaseTest

LOGGER = logging.getLogger(__name__)


class TestCareersPageSimpleVacancyFiltering(BaseTest):
    """
    Simple vacancy filtering tests suite
    """

    @pytest.mark.parametrize('country_name,language,expected_vacancy_count', [
        ('Romania', 'english', 38)
    ])
    def test_careers_page_simple_vacancy_filtering(self, country_name, language, expected_vacancy_count):
        """
        Description:
        Simple vacancy filtering test

        Steps:
        1) Go to careers page
        2) Get started vacancy counts
        3) Choose vacancy country
        4) Choose vacancy language
        5) Click to apply filter button
        6) Check what received vacancy equals to expected

        Expectation:
        1) Vacancy counts equal to expected
        """
        self.careers_page.go_to_careers_page()
        start_vacancy_count = self.careers_page.get_current_vacancy_counters()
        self.careers_page.choose_vacancy_country(country_name=country_name)
        self.careers_page.choose_vacancy_language(language=language)
        self.careers_page.click_to_apply_filter_button()

        ret = self.careers_page.wait_for_all_vacancy_blocks_count_equal_expected(
            expected_count=expected_vacancy_count,
            start_vacancy_counts=start_vacancy_count
        )
        assert ret, 'Received vacancy count does not equal to expected. Error: {}'.format(
            self.careers_page.get_last_error())
