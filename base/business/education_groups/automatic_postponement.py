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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.utils.translation import ugettext as _

from base.business.education_groups.postponement import duplicate_education_group_year
from base.business.utils.postponement import AutomaticPostponement
from base.models.education_group_year import EducationGroupYear
from base.models.enums.education_group_categories import GROUP
from base.utils.send_mail import send_mail_before_annual_procedure_of_automatic_postponement, \
    send_mail_after_annual_procedure_of_automatic_postponement


class EducationGroupAutomaticPostponement(AutomaticPostponement):
    model = EducationGroupYear

    send_before = send_mail_before_annual_procedure_of_automatic_postponement
    send_after = send_mail_after_annual_procedure_of_automatic_postponement
    extend_method = duplicate_education_group_year
    msg_result = _("%s education group(s) extended and %s error(s)")

    def get_queryset(self, queryset=None):
        return super().get_queryset(queryset).exclude(education_group_type__category=GROUP)

    def get_already_duplicated(self):
        return self.queryset.filter(education_group__educationgroupyear__academic_year=self.last_academic_year)

    def get_to_not_duplicated(self):
        return self.queryset.filter(education_group__end_year__lt=self.last_academic_year.year)
