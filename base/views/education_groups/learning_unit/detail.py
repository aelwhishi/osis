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
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView

from base.business.education_groups.learning_units.prerequisite import \
    get_prerequisite_acronyms_which_are_outside_of_education_group
from base.models import group_element_year
from base.models.education_group_year import EducationGroupYear
from base.models.enums import education_group_categories
from base.models.learning_unit_year import LearningUnitYear
from base.models.person import Person
from base.models.prerequisite import Prerequisite


@method_decorator(login_required, name='dispatch')
class LearningUnitGenericDetailView(PermissionRequiredMixin, DetailView):
    model = LearningUnitYear
    context_object_name = "learning_unit_year"
    pk_url_kwarg = 'learning_unit_year_id'

    permission_required = 'base.can_access_education_group'
    raise_exception = True

    def get_person(self):
        return get_object_or_404(Person, user=self.request.user)

    def get_root(self):
        return get_object_or_404(EducationGroupYear, pk=self.kwargs.get("root_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['person'] = self.get_person()
        context['root'] = self.get_root()
        context['root_id'] = self.kwargs.get("root_id")
        context['parent'] = self.get_root()

        context['group_to_parent'] = self.request.GET.get("group_to_parent") or '0'
        return context


class LearningUnitUtilization(LearningUnitGenericDetailView):
    template_name = "education_group/learning_unit/tab_utilization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group_element_years"] = group_element_year.find_by_child_leaf(self.object).select_related("parent")
        return context


class LearningUnitPrerequisite(LearningUnitGenericDetailView):
    template_name = "education_group/learning_unit/tab_prerequisite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        learning_unit_year = context["learning_unit_year"]
        education_group_year_root_id = context["root_id"]
        is_root_a_training = context["root"].education_group_type.category in \
            education_group_categories.TRAINING_CATEGORIES

        if is_root_a_training:
            qs = EducationGroupYear.objects.filter(id=education_group_year_root_id)
        else:
            formations_id = group_element_year.find_learning_unit_formations([learning_unit_year]).\
                get(learning_unit_year.id, [])
            qs = EducationGroupYear.objects.filter(id__in=formations_id)

        prefetch_prerequisites = Prefetch("prerequisite_set",
                                          Prerequisite.objects.filter(learning_unit_year=learning_unit_year),
                                          to_attr="prerequisites")
        context["formations"] = qs.prefetch_related(prefetch_prerequisites)
        context["is_root_a_training"] = is_root_a_training

        if is_root_a_training:
            learning_unit_inconsistent = get_prerequisite_acronyms_which_are_outside_of_education_group(context["root"],
                                                                                                        context["formations"][0].prerequisites[0])
            if learning_unit_inconsistent:
                messages.warning(self.request, _("The prerequisites %s for the learning unit %s are not inside the selected formation %s") % (", ".join(learning_unit_inconsistent), learning_unit_year, context["root"]))

        return context
