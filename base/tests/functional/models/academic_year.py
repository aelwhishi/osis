from base.tests.factories.academic_year import AcademicYearFactory


class LearningContainerMixin:

    @staticmethod
    def init(year=None):
        return AcademicYearFactory(year=year) if year else AcademicYearFactory()
