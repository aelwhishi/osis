from osis_common.tests.functional.models.model import FunctionalTestCase
from base.tests.functional.models.common import CommonMixin
from base.tests.functional.models.user_type import FacAdministratorMixin


class DayToDayManagementLearningUnitsAsFacultyManager(FunctionalTestCase, FacAdministratorMixin):
    """
    Search for teaching units in day-to-day management as a Faculty Manager.
    """

    def setUp(self):
        super(DayToDayManagementLearningUnitsAsFacultyManager, self).setUp()
        self.faculty_administrator = self.create_fac_admin()
        self.academic_years = CommonMixin.init_academic_years(2007, 20)
        self.login(self.faculty_administrator.user.username)
        self.open_url_by_name('home')

    @classmethod
    def setUpClass(cls):
        super(DayToDayManagementLearningUnitsAsFacultyManager, cls).setUpClass()
        cls.learning_units_config = cls.config.get('LEARNING_UNITS')

    def test_all_existing_courses_for_the_year_n(self):
        # As a Faculty Manager
        # When I am on the home page
        # And I click on the "Formation catalogue" link
        self.click_element_by_id('lnk_home_catalog')

        # And then click on the "Learning units" link
        self.click_element_by_id('lnk_learning_units')

        # I am on the learning units search page, learning units tab
        self.check_page_contains_ids(self.learning_units_config.get('BY_ACTIVITY_LINKS'))

        # And there are no results yet
        self.check_page_not_contains_ids(('table_learning_units_wrapper',))

        # And the search form is empty

        # Except for the academic year, which is pre-selected

        # If I click on the search button
        self.click_element_by_id('search_button')

        # - I should see a message to warn me that there is too many results.
        self.check_page_contains_string(self.get_localized_message('too_many_results', 'en'))
