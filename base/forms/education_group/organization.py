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
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from base.models.education_group_organization import EducationGroupOrganization
from base.models.education_group_year import EducationGroupYear
from reference.models.country import Country
from base.models.organization import Organization, find_by_id
from base.models.entity import Entity


class OrganizationEditForm(forms.ModelForm):
    country = ModelChoiceField(
        queryset=Country.objects.filter(entity__isnull=False).distinct().order_by('name'),
        required=True,
        label=_("country")
    )

    organization = ModelChoiceField(
        queryset=Organization.objects.filter(entity__country__isnull=False).distinct(),
        required=True,
        label=_("institution")
    )

    class Meta:
        model = EducationGroupOrganization
        fields = ['country', 'organization', 'all_students', 'enrollment_place', 'diploma',
                  'is_producing_cerfificate', 'is_producing_annexe']

    def __init__(self, data=None, education_group_year=None, *args, **kwargs):
        if not education_group_year and not kwargs.get('instance'):
            raise ImproperlyConfigured("Provide an education_group_year or an instance")

        super().__init__(data, *args, **kwargs)
        if not kwargs.get('instance'):
            self.instance.education_group_year = education_group_year

        if self.instance.pk:
            country = Country.objects.filter(entity__organization=self.instance.organization).first()
            self.fields['country'].initial = country
            self.fields['organization'].queryset = Organization.objects.filter(entity__country=country).distinct()

    def check_unique_constraint_between_education_group_year_organization(self):
        qs = EducationGroupOrganization.objects.filter(
            education_group_year=self.instance.education_group_year,
            organization=self.cleaned_data['organization'],
        )
        if self.instance and self.instance.pk:
            qs = qs.exclude(id=self.instance.pk)

        if qs.exists():
            self.add_error('organization', _('There is already a coorganization with this organization'))
            return False
        return True

    def is_valid(self):
        return super(OrganizationEditForm, self).is_valid() and \
               self.check_unique_constraint_between_education_group_year_organization()
