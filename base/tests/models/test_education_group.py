##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2018 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.core.exceptions import ValidationError
from django.test import TestCase
from base.models.education_group_year import EducationGroupYear
from base.tests.factories.academic_year import AcademicYearFactory
from base.tests.factories.education_group import EducationGroupFactory
from base.tests.factories.education_group_year import EducationGroupYearFactory


class EducationGroupTest(TestCase):

    def test_most_recent_acronym(self):
        education_group = EducationGroupFactory()
        most_recent_year = 2018
        for year in range(2016, most_recent_year + 1):
            EducationGroupYearFactory(education_group=education_group, academic_year=AcademicYearFactory(year=year))
        most_recent_educ_group_year = EducationGroupYear.objects.get(academic_year__year=most_recent_year,
                                                                     education_group=education_group)
        self.assertEqual(education_group.most_recent_acronym, most_recent_educ_group_year.acronym)

    def test_clean_case_start_year_greater_than_end_year_error(self):
        education_group = EducationGroupFactory.build(
            start_year=2000,
            end_year=1999
        )
        with self.assertRaises(ValidationError):
            education_group.clean()

    def test_clean_case_start_year_equals_to_end_year_no_error(self):
        education_group = EducationGroupFactory.build(
            start_year=2000,
            end_year=2000
        )
        education_group.clean()
        education_group.save()

    def test_clean_case_start_year_lower_to_end_year_no_error(self):
        education_group = EducationGroupFactory.build(
            start_year=1999,
            end_year=2000
        )
        education_group.clean()
        education_group.save()
