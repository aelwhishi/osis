# ##################################################################################################
#  OSIS stands for Open Student Information System. It's an application                            #
#  designed to manage the core business of higher education institutions,                          #
#  such as universities, faculties, institutes and professional schools.                           #
#  The core business involves the administration of students, teachers,                            #
#  courses, programs and so on.                                                                    #
#                                                                                                  #
#  Copyright (C) 2015-2019 Université catholique de Louvain (http://www.uclouvain.be)              #
#                                                                                                  #
#  This program is free software: you can redistribute it and/or modify                            #
#  it under the terms of the GNU General Public License as published by                            #
#  the Free Software Foundation, either version 3 of the License, or                               #
#  (at your option) any later version.                                                             #
#                                                                                                  #
#  This program is distributed in the hope that it will be useful,                                 #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of                                  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                   #
#  GNU General Public License for more details.                                                    #
#                                                                                                  #
#  A copy of this license - GNU General Public License - is available                              #
#  at the root of the source code of this program.  If not,                                        #
#  see http://www.gnu.org/licenses/.                                                               #
# ##################################################################################################
from django.contrib.admin import ModelAdmin
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from base.models.enums import entity_type
from reference.models.academic_year import AcademicYear


class EntityYearAdmin(ModelAdmin):
    list_display = ('id', 'entity', 'acronym', 'parent', 'title', 'entity_type')
    search_fields = ['title', 'acronym', 'entity_type']
    raw_id_fields = ('entity', 'parent')


class EntityYear(MPTTModel):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE)

    title = models.CharField(db_index=True, max_length=255, verbose_name=_("title"))

    acronym = models.CharField(db_index=True, max_length=20, verbose_name=_("acronym"))

    academic_year = models.ForeignKey(
        AcademicYear,
        verbose_name=_('academic year'),
        related_name="entities"
    )

    entity_type = models.CharField(
        choices=entity_type.ENTITY_TYPES,
        max_length=50,
        blank=True,
        verbose_name=_("Type")
    )

    parent = TreeForeignKey(
        'self', related_name='children',
        blank=True, null=True,
        verbose_name=_("Parent")
    )

    logo = models.ImageField(
        upload_to='organization_logos',
        null=True, blank=True,
        verbose_name=_("logo")
    )

    def __str__(self):
        return "{} ({} - {} - {})".format(self.acronym, self.title, self.entity_type, self.academic_year)

    class Meta:
        unique_together = ('entity', 'academic_year')
        verbose_name = _("Annualized entity")
        verbose_name_plural = _("Annualized entities")

    class MPTTMeta:
        order_insertion_by = ['acronym']
