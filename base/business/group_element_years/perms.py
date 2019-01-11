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
from django.utils.text import ugettext_lazy as _
from base.business.education_groups.perms import _is_eligible_education_group, can_raise_exception
from base.models.enums.education_group_types import GroupType


def is_eligible_to_create_group_element_year(person, egy, raise_exception):

    return _is_eligible_education_group(person, egy, raise_exception) and \
           _user_can_update_group_element_year_of_type(person, egy, raise_exception)


def _user_can_update_group_element_year_of_type(person, egy, raise_exception):
    group_type_only_central_can_create = (GroupType.MAJOR_LIST_CHOICE.name, GroupType.MINOR_LIST_CHOICE.name)
    result = person.is_central_manager or egy.education_group_type.name not in group_type_only_central_can_create
    can_raise_exception(raise_exception, result, _("The user cannot modify content for (%(education_group_types)s)") %
                        {"education_group_types":
                            ", ".join([str(GroupType.MAJOR_LIST_CHOICE.value), str(GroupType.MINOR_LIST_CHOICE.name)])
                         })
    return result
