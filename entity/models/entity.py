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
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy

from reference.models.country import Country


class EntityAdmin(ModelAdmin):
    list_display = ('most_recent_acronym', 'external_id', 'organization', 'location', 'postal_code', 'phone')
    search_fields = ['external_id', 'entityyear__acronym', 'entityyear__title', 'organization__name']
    readonly_fields = ('organization', 'external_id')


class Entity(models.Model):
    location = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True, related_name='true_entity')
    phone = models.CharField(max_length=30, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)

    esb_id = models.IntegerField(unique=True)

    class Meta:
        verbose_name = gettext_lazy("entity")
        verbose_name_plural = gettext_lazy("entities")

    def __str__(self):
        try:
            return self.entityyear_set.latest('academic_year__year')
        except ObjectDoesNotExist:
            return ""
