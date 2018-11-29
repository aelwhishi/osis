##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _

from base.models import group_element_year, authorized_relationship
from base.models.education_group_year import EducationGroupYear
from base.models.enums import count_constraint
from base.models.exceptions import IncompatiblesTypesException, MaxChildrenReachedException
from base.models.group_element_year import GroupElementYear
from base.models.learning_unit_year import LearningUnitYear
from base.utils.cache import cache

LEARNING_UNIT_YEAR = 'learningunityear'
EDUCATION_GROUP_YEAR = 'educationgroupyear'
SELECT_CACHE_KEY = 'child_to_cache_id'


def select_education_group_year(education_group_year):
    return _set_selected_element_on_cache(education_group_year.pk, EDUCATION_GROUP_YEAR)


def select_learning_unit_year(learning_unit_year):
    return _set_selected_element_on_cache(learning_unit_year.pk, LEARNING_UNIT_YEAR)


def _set_selected_element_on_cache(id, modelname):
    data_to_cache = {'id': id, 'modelname': modelname}
    cache.set(SELECT_CACHE_KEY, data_to_cache, timeout=None)
    return True


def attach_from_cache(parent):
    selected_data = cache.get(SELECT_CACHE_KEY)
    if selected_data:
        kwargs = {'parent': parent}
        if selected_data['modelname'] == LEARNING_UNIT_YEAR:
            luy = LearningUnitYear.objects.get(pk=selected_data['id'])
            kwargs['child_leaf'] = luy
        elif selected_data['modelname'] == EDUCATION_GROUP_YEAR:
            egy = EducationGroupYear.objects.get(pk=selected_data['id'])
            if not _types_are_compatible(parent, egy):
                raise IncompatiblesTypesException(
                    errors=_("You cannot attach \"%(child)s\" (type \"%(child_type)s\") "
                             "to \"%(parent)s\" (type \"%(parent_type)s\")") % {
                        'child': egy,
                        'child_type': egy.education_group_type,
                        'parent': parent,
                        'parent_type': parent.education_group_type,
                    }
                )
            if _is_max_child_reached(parent, egy):
                raise MaxChildrenReachedException(
                    errors=_("The number of children of type \"%(child_type)s\" for \"%(parent)s\" "
                             "has already reached the limit.") % {
                        'child_type': egy.education_group_type,
                        'parent': parent
                    }
                )
            kwargs['child_branch'] = egy
        new_gey = group_element_year.get_or_create_group_element_year(**kwargs)
        _clear_cache()
        return new_gey
    raise ObjectDoesNotExist


def _clear_cache():
    cache.set(SELECT_CACHE_KEY, None, timeout=None)


def _types_are_compatible(parent, child):
    return authorized_relationship.AuthorizedRelationship.objects.filter(
        parent_type=parent.education_group_type,
        child_type=child.education_group_type,
    ).exists()


def _is_max_child_reached(parent, child):
    child_education_type = child.education_group_type
    number_children_of_same_type = GroupElementYear.objects.filter(
        parent=parent,
        child_branch__education_group_type=child_education_type
    ).count()
    auth_rel = authorized_relationship.AuthorizedRelationship.objects.get(
        parent_type=parent.education_group_type,
        child_type=child.education_group_type,
    )
    max_count = auth_rel.max_count_authorized
    return number_children_of_same_type > 0 and max_count == count_constraint.ONE


def _is_min_child_reached(parent, child):
    child_education_type = child.education_group_type
    number_children_of_same_type = GroupElementYear.objects.filter(
        parent=parent,
        child_branch__education_group_type=child_education_type
    ).count()
    auth_rel = authorized_relationship.AuthorizedRelationship.objects.get(
        parent_type=parent.education_group_type,
        child_type=child.education_group_type,
    )
    min_count = auth_rel.min_count_authorized
    return number_children_of_same_type <= 1 and min_count == count_constraint.ONE
