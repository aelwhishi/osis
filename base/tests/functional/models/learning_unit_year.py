
from base.tests.functional.models import academic_year as fake_academic_year
from base.tests.functional.models import learning_unit as fake_learning_unit
from base.tests.functional.models import learning_container_year as fake_learning_container_year
from models.enums import learning_unit_year_periodicity, learning_unit_year_subtypes
from tests.factories.business.learning_units import LearningUnitsMixin


class LearningUnitYearMixin:

    @staticmethod
    def init(academic_year=None,
             learning_unit=None,
             learning_container_year=None,
             learning_unit_year_subtype=None,
             periodicity=None):

        if not academic_year:
            academic_year = fake_academic_year.init()

        if not learning_unit:
            learning_unit = fake_learning_unit.init()

        if not learning_container_year:
            learning_unit = fake_learning_container_year.init(
                academic_year=academic_year,
                learning_container=learning_unit.learning_container
            )

        if not learning_unit_year_subtype:
            learning_unit_year_subtype = learning_unit_year_subtypes.FULL

        if not periodicity:
            periodicity = learning_unit_year_periodicity.ANNUAL

        learning_unit_year = LearningUnitsMixin.setup_learning_unit_year(
            academic_year=academic_year,
            learning_unit=learning_unit,
            learning_container_year=learning_container_year,
            learning_unit_year_subtype=learning_unit_year_subtype,
            periodicity=periodicity
        )

        return learning_unit_year
