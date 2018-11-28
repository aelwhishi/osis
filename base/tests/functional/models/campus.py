from base.tests.factories.campus import CampusFactory


class LearningContainerMixin:

    @staticmethod
    def init(organization=None):

        if not organization:
            campus = CampusFactory(organization=organization)
        else:
            campus = CampusFactory()

        return campus
