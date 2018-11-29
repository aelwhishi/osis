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
from django.core.management import BaseCommand
from openpyxl import Workbook

from base.models.program_manager import ProgramManager


class Command(BaseCommand):
    def handle(self, *args, **options):
        _extract_program_managers_to_xls()


def _extract_program_managers_to_xls():
    qs_list = ProgramManager.objects.filter(
        offer_year__academic_year__year=2018,
    ).order_by(
        'offer_year__entity_management_fac__acronym',
        'offer_year__entity_management__acronym',
        'offer_year__acronym',
        'person__last_name',
        'person__first_name',
    ).select_related(
        'offer_year',
        'person',
        'offer_year__entity_management_fac',
        'offer_year__entity_management',
    )

    workbook = Workbook()
    worksheet = workbook.active

    worksheet.append(["Faculté de l'entité de gestion", 'Entité de gestion', 'Sigle', 'Intitulé', 'Nom', 'Prénom'])
    for program_manager in qs_list:
        row = [
            program_manager.offer_year.entity_management_fac.acronym,
            program_manager.offer_year.entity_management.acronym,
            program_manager.offer_year.acronym,
            program_manager.offer_year.title,
            program_manager.person.last_name,
            program_manager.person.first_name
        ]
        worksheet.append(row)

    workbook.save(filename='program_managers_2018.xlsx')
