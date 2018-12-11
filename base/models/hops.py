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
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin


class HopsAdmin(SerializableModelAdmin):
    list_display = ('ARES_study', 'ARES_GRACA', 'ARES_ability', 'changed')
    list_filter = ('ARES_study', )
    raw_id_fields = (
        'education_group_year'
    )
    search_fields = ['ARES_study']


class Hops(SerializableModel):

    external_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    changed = models.DateTimeField(null=True, auto_now=True)
    education_group_year = models.OneToOneField('base.EducationGroupYear', on_delete=models.CASCADE)

    ARES_study = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('ARES study code'),
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
    )

    ARES_GRACA = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('ARES-GRACA'),
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
    )

    ARES_ability = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('ARES ability'),
        validators=[MinValueValidator(1), MaxValueValidator(9999)],

    )

    def __str__(self):
        return str(self.ARES_study) if self.ARES_study else ''
