#!/usr/bin/env python

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

import json
# import migration_epc_to_osis.v1.base.organization
# from config import properties
# from esb_export import settings
# from lib import config_example
# from lib.databases import postgres_connection
# from lib.utils import cache_utils
# from migration_epc_to_osis.v1.base import entity
# from migration_epc_to_osis.v1.base import entity_version
# from migration_epc_to_osis.v1.base import organization
from operator import itemgetter

from django.core.management.base import BaseCommand

from entity.models.entity import Entity
from entity.models.entity_year import EntityYear
from reference.models.academic_year import AcademicYear
from reference.models.country import Country

FIXTURE_PATH = "entity/fixtures/entities_esb.json"

ESB_OSIS_TYPES_MATCH = {
    'S': 'SECTOR',
    'F': 'FACULTY',
    'E': 'SCHOOL',
    'I': 'INSTITUTE',
    'P': 'POLE',
    'D': 'DOCTORAL_COMMISSION',
    'T': 'PLATFORM',
    'L': 'LOGISTICS_ENTITY',
    'N': None,
}

ESB_NOT_ENDING_PERIOD_END_DATE = 99991231


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.load_json_esb(FIXTURE_PATH)

    @staticmethod
    def load_json_esb(path):
        with open(path, encoding="utf-8") as f:
            data = json.loads(f.read())
            process_esb_data(data['entities']['entity'])


def process_esb_data(esb_data):
    current_hierarchy_data = {}
    counter = 0
    sorted_esb_data = sort_esb_data_by_level(esb_data)
    print(sorted_esb_data)
    for esb_item in sorted_esb_data:
        counter += 1
        entity = build_entity(esb_item, current_hierarchy_data)

        print(entity)


def sort_esb_data_by_level(esb_data):
    for item in esb_data:
        acronyms = item.get('acronyms')
        try:
            item['level'] = len(acronyms.split("/"))
        except AttributeError:
            item['level'] = 0

    return sorted(esb_data, key=itemgetter('level'))


def build_entity(esb_item, current_hierarchy_data):
    entityversion_set = build_versions(esb_item, current_hierarchy_data)
    entity, _ = Entity.objects.update_or_create(
        esb_id=esb_item["entity_id"],
        defaults={
            "website": esb_item['web'] or '',
            "country": Country.objects.get(iso_code='BE'),
        }
    )
    print(entity)
    for env in entityversion_set:

        qa = AcademicYear.objects.filter(
            start_date__lt=env['start_date']
        )
        if env['end_date']:
            qa = qa.filter(end_date__gte=env['end_date'])

        academic_year = qa.last()
        print(academic_year, type(academic_year))

        try:
            ey = EntityYear.objects.get(
                academic_year=academic_year.pk,
                entity=entity,
            )
        except EntityYear.DoesNotExist:
            ey = EntityYear(
                academic_year=academic_year,
                entity=entity,
            )

        ey.update({
                'acronym': env['acronym'],
                'title': env['title'],
                'entity_type': env['entity_type'],
            })

        return entity


def build_versions(esb_item, current_hierarchy_data):
    try:
        entity_parent = current_hierarchy_data.get(esb_item['parent_entity_id'])
    except TypeError:
        entity_parent = None
    start_date = format_date_for_osis(esb_item['begin'])
    end_date = format_date_for_osis(esb_item['end'])
    return [
        {
            "acronym": esb_item['acronym'],
            "parent": entity_parent,
            "title": esb_item['name_fr'],
            "entity_type": get_entity_type(esb_item),
            "start_date": start_date,
            "end_date": end_date,
        }
    ]


def get_entity_type(esb_item):
    return ESB_OSIS_TYPES_MATCH.get(esb_item.get('departmentType'))


def format_date_for_osis(esb_date):
    if esb_date != ESB_NOT_ENDING_PERIOD_END_DATE:
        return "{}-{}-{}".format(str(esb_date)[0:4], str(esb_date)[4:6], str(esb_date)[6:8])
    else:
        return None
