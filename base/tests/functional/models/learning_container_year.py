from base.tests.factories.learning_container_year import LearningContainerYearFactory

from base.tests.functional.models import academic_year as fake_academic_year
from base.tests.functional.models import learning_container as fake_learning_container


class LearningContainerMixin:

    @staticmethod
    def init(academic_year=None, learning_container=None):

        if not academic_year:
            academic_year = fake_academic_year.init()

        if not learning_container:
            learning_container = fake_learning_container.init()

        learning_container_year = LearningContainerYearFactory(
            academic_year=academic_year,
            learning_container=learning_container
        )

        return learning_container_year
