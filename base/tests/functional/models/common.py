from base.tests.factories.academic_year import AcademicYearFactory


class CommonMixin:

    @staticmethod
    def init_academic_years(start_year=None, count_year=1):
        academics_years = []
        if start_year:
            for i in range(count_year):
                academics_years.append(AcademicYearFactory(year=start_year+i))
        else:
            academics_years = [AcademicYearFactory()]
        return academics_years
