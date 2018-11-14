from base.tests.factories.user import UserFactory
from osis_common.tests.functional.models.model import FunctionalTestCase
from osis_common.tests.functional.models.report import can_be_reported


class BasicLoginTestCase(FunctionalTestCase):

    def setUp(self):
        super(BasicLoginTestCase, self).setUp()
        self.valid_user = UserFactory()

    @can_be_reported
    def test_login_page(self):
        """
        As a non connected user
        I should see the login page
        """
        self.open_url_by_name('login')
        self.check_page_title(self.config.get('LOGIN').get('PAGE_TITLE'))

    @can_be_reported
    def test_valid_login(self):
        """
        As a registered user with valid password
        I should be able to connect
        """
        self.login(self.valid_user.username)
        self.check_page_title(self.config.get('DASHBOARD').get('PAGE_TITLE'))
        string = self.get_localized_message('my_osis', 'en')
        self.check_page_contains_string(string)

    @can_be_reported
    def test_invalid_login(self):
        """
        As a registered user with wrong password
        I should not be able to connect
        """
        self.login(self.valid_user.username, 'wrong_password')
        string = self.get_localized_message('msg_error_username_password_not_matching', 'en')
        self.check_page_contains_string(string)