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
from dal import autocomplete
from django import forms
from django.forms import TextInput
from django.utils.translation import ugettext_lazy as _

from attribution.models.attribution_charge_new import AttributionChargeNew
from attribution.models.attribution_new import AttributionNew
from base.models.enums import learning_component_year_type
from base.models.learning_component_year import LearningComponentYear
from base.models.tutor import Tutor


class AttributionForm(forms.ModelForm):
    duration = forms.IntegerField(min_value=1, required=True, label=_("duration"))

    class Meta:
        model = AttributionNew
        fields = ["function", "start_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["duration"].initial = self.instance.duration

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.end_year = instance.start_year + self.cleaned_data["duration"] - 1
        if commit:
            instance.save()
        return instance


class AttributionCreationForm(AttributionForm):
    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.all().select_related("person").order_by("person__last_name", "person__first_name"),
        required=True,
        widget=autocomplete.ModelSelect2(
            url='tutor_autocomplete',
            attrs={'data-theme': 'bootstrap', 'data-width': 'null', 'data-placeholder': '---------'}
        ),
        label=_('tutor'),
    )

    class Meta:
        model = AttributionNew
        fields = ["tutor", "function", "start_year"]

    class Media:
        css = {
            'all': ('css/select2-bootstrap.css',)
        }

    def save(self, commit=True, **kwargs):
        luy = kwargs.pop("learning_unit_year")
        instance = super().save(commit=False)
        instance.learning_container_year = luy.learning_container_year
        if commit:
            instance.save()
        return instance


class AttributionChargeForm(forms.ModelForm):
    component_type = None

    class Meta:
        model = AttributionChargeNew
        fields = ["allocation_charge"]

    def save(self, commit=True,  **kwargs):
        attribution_new_obj = kwargs.pop("attribution")
        luy_obj = kwargs.pop("learning_unit_year")
        learning_component_year = LearningComponentYear.objects.get(type=self.component_type,
                                                                    learningunitcomponent__learning_unit_year=luy_obj)

        attribution_charge_obj = super().save(commit=False)
        attribution_charge_obj.attribution = attribution_new_obj
        attribution_charge_obj.learning_component_year = learning_component_year
        if commit:
            attribution_charge_obj.save()
        return attribution_charge_obj


class LecturingAttributionChargeForm(AttributionChargeForm):
    component_type = learning_component_year_type.LECTURING

    class Meta:
        model = AttributionChargeNew
        fields = ('allocation_charge',)
        labels = {
            'allocation_charge': _("Volume 1"),
        }


class PracticalAttributionChargeForm(AttributionChargeForm):
    component_type = learning_component_year_type.PRACTICAL_EXERCISES

    class Meta:
        model = AttributionChargeNew
        fields = ('allocation_charge',)
        labels = {
            'allocation_charge': _("Volume 2"),
        }
