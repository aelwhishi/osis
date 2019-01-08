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
from django import forms
from django.utils.translation import gettext as _

from base.models.enums.education_group_types import GroupType
from base.models.group_element_year import GroupElementYear


class GroupElementYearForm(forms.ModelForm):
    class Meta:
        model = GroupElementYear
        fields = [
            "relative_credits",
            "is_mandatory",
            "block",
            "quadrimester_derogation",
            "link_type",
            "comment",
            "comment_english",
        ]
        widgets = {
            "comment": forms.Textarea(attrs={'rows': 5}),
            "comment_english": forms.Textarea(attrs={'rows': 5}),

        }

    def __init__(self, *args, parent=None, child_branch=None, child_leaf=None, **kwargs):
        super().__init__(*args, **kwargs)

        # No need to attach FK to an existing GroupElementYear
        if self.instance.pk:
            return

        self.instance.parent = parent
        self.instance.child_leaf = child_leaf
        self.instance.child_branch = child_branch

    def clean_link_type(self):
        data_cleaned = self.cleaned_data.get('link_type')
        if data_cleaned:
            parent_type = self.instance.parent.education_group_type
            if self.instance.child_branch and not parent_type.authorized_parent_type.filter(
                    child_type=self.instance.child_branch.education_group_type,
                    reference=True,
            ).exists():
                self.add_error('link_type', _(
                    "You are not allow to create a reference link between a %(parent_type)s and a %(child_type)s."
                ) % {
                        "parent_type": self.instance.parent.education_group_type,
                        "child_type": self.instance.child_branch.education_group_type,
                    })
            elif self.instance.child_leaf:
                self.add_error('link_type', _("You are not allowed to create a reference with a learning unit"))
        return data_cleaned


class GroupElementYearMinorMajorOptionForm(GroupElementYearForm):
    class Meta(GroupElementYearForm.Meta):
        fields = GroupElementYearForm.Meta.fields + ["access_condition"]

    def save(self, commit=True):
        obj = super().save(commit)
        self._reorder_children_by_partial_acronym(obj.parent)
        return obj

    @staticmethod
    def _reorder_children_by_partial_acronym(parent):
        children = parent.children.order_by("child_branch__partial_acronym")

        for counter, child in enumerate(children):
            child.order = counter
            child.save()
