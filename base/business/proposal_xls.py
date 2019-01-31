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

from django.utils.translation import ugettext_lazy as _

from osis_common.document import xls_build
from base.business.learning_unit import get_entity_acronym
from base.business.xls import get_name_or_username
from base.models.campus import find_by_id as find_campus_by_id
from base.models.entity import find_by_id

from base.models.learning_unit_year import get_by_id
from base.models.proposal_learning_unit import find_by_learning_unit_year
from base.models.enums.learning_unit_year_periodicity import PERIODICITY_TYPES
from base.business.learning_units.xls_comparison import LEARNING_UNIT_TITLES,  \
    DATA, CELLS_TOP_BORDER, CELLS_MODIFIED_NO_BORDER, extract_xls_data_from_learning_unit, \
    get_organization_from_learning_unit_year, _get_data, EMPTY_VALUE, translate_status, get_translation, \
    get_border_columns
from reference.models.language import find_by_id as find_language_by_id
from openpyxl.utils import get_column_letter
from base.models.enums.learning_unit_year_periodicity import PERIODICITY_TYPES
from base.models.enums.learning_container_year_types import LEARNING_CONTAINER_YEAR_TYPES

WORKSHEET_TITLE = _('Proposals')
XLS_FILENAME = _('Proposals')
XLS_DESCRIPTION = _("List proposals")


PROPOSAL_TITLES = [str(_('Req. Entity')), str(_('Code')), str(_('Title')), str(_('Type')),
                   str(_('Proposal type')), str(_('Proposal status')), str(_('Folder num.')),
                   str(_('Decision')), str(_('Periodicity')), str(_('Credits')),
                   str(_('Alloc. Ent.')), str(_('Proposals date'))]

COMPARISON_WORKSHEET_TITLE=_("Proposals comparison")
XLS_COMPARISON_FILENAME = _('Proposals_comparison')
XLS_DESCRIPTION_COMPARISON = _("List of comparison between proposals and UE")


def prepare_xls_content(proposals):
    return [extract_xls_data_from_proposal(proposal) for proposal in proposals]


def extract_xls_data_from_proposal(luy):
    proposal = find_by_learning_unit_year(luy)
    return [luy.entity_requirement,
            luy.acronym,
            luy.complete_title,
            luy.learning_container_year.get_container_type_display(),
            proposal.get_type_display(),
            proposal.get_state_display(),
            proposal.folder,
            luy.learning_container_year.get_type_declaration_vacant_display(),
            dict(PERIODICITY_TYPES)[luy.periodicity],
            luy.credits,
            luy.entity_allocation,
            proposal.date.strftime('%d-%m-%Y')]


def prepare_xls_parameters_list(user, working_sheets_data):
    return {xls_build.LIST_DESCRIPTION_KEY: _(XLS_DESCRIPTION),
            xls_build.FILENAME_KEY: _(XLS_FILENAME),
            xls_build.USER_KEY: get_name_or_username(user),
            xls_build.WORKSHEETS_DATA:
                [{xls_build.CONTENT_KEY: working_sheets_data,
                  xls_build.HEADER_TITLES_KEY: PROPOSAL_TITLES,
                  xls_build.WORKSHEET_TITLE_KEY: _(WORKSHEET_TITLE),
                  }
                 ]}


def create_xls(user, proposals, filters):
    ws_data = xls_build.prepare_xls_parameters_list(prepare_xls_content(proposals), configure_parameters(user))
    return xls_build.generate_xls(ws_data, filters)


def configure_parameters(user):
    return {xls_build.DESCRIPTION: XLS_DESCRIPTION,
            xls_build.USER: get_name_or_username(user),
            xls_build.FILENAME: XLS_FILENAME,
            xls_build.HEADER_TITLES: PROPOSAL_TITLES,
            xls_build.WS_TITLE: WORKSHEET_TITLE}


def create_xls_proposal_comparison(user, learning_units_with_proposal, filters):
    data = prepare_xls_content_for_comparison(learning_units_with_proposal)

    working_sheets_data = data.get('data')
    cells_modified_with_green_font = data.get(CELLS_MODIFIED_NO_BORDER)
    cells_with_top_border = data.get(CELLS_TOP_BORDER)
    parameters = {
        xls_build.DESCRIPTION: XLS_DESCRIPTION_COMPARISON,
        xls_build.USER: get_name_or_username(user),
        xls_build.FILENAME: XLS_COMPARISON_FILENAME,
        xls_build.HEADER_TITLES: [''] + LEARNING_UNIT_TITLES,
        xls_build.WS_TITLE: COMPARISON_WORKSHEET_TITLE,
    }
    dict_styled_cells = {}
    if cells_modified_with_green_font:
        dict_styled_cells.update({xls_build.STYLE_MODIFIED: cells_modified_with_green_font})

    if cells_with_top_border:
        dict_styled_cells.update({xls_build.STYLE_BORDER_TOP: cells_with_top_border})
    if dict_styled_cells:
        parameters.update({xls_build.STYLED_CELLS: dict_styled_cells})
    return xls_build.generate_xls(xls_build.prepare_xls_parameters_list(working_sheets_data, parameters), filters)


def extract_xls_data_from_proposal_initial_data(learning_unit_year):
    proposal = find_by_learning_unit_year(learning_unit_year)
    return _get_data_from_initial_data(proposal.initial_data)


def prepare_xls_content_for_comparison(luy_with_proposals):
    line_index = 1
    data = []
    top_border = []
    modified_cells_no_border = []
    for luy_with_proposal in luy_with_proposals:
        top_border.extend(get_border_columns(line_index + 1))

        data_proposal = [_('Proposal')] + _get_data(luy_with_proposal, False, None)
        data.append(data_proposal)
        proposal = find_by_learning_unit_year(luy_with_proposal)
        initial_luy_data = proposal.initial_data

        if initial_luy_data:
            initial_data = extract_xls_data_from_proposal_initial_data(luy_with_proposal)
            data.append(initial_data)
        else:
            initial_data = []

        modified_cells_no_border.extend(
            _check_changes(initial_data,
                           data_proposal,
                           line_index + 2))
        line_index = line_index +2

    return {
        DATA: data,
        CELLS_TOP_BORDER: top_border or None,
        CELLS_MODIFIED_NO_BORDER: modified_cells_no_border or None,
    }


def _get_data_from_initial_data(initial_data):
    # {'entities': {'ALLOCATION_ENTITY': 2982, 'REQUIREMENT_ENTITY': 2982, 'ADDITIONAL_REQUIREMENT_ENTITY_1': None, 'ADDITIONAL_REQUIREMENT_ENTITY_2': None},
    # 'learning_unit': {'id': 201573, 'end_year': None},
    # 'learning_unit_year': {'id': 13409241, 'campus': 3, 'acronym': 'LECON2011', 'credits': 5.0, 'language': 4, 'periodicity': 'ANNUAL', 'specific_title': None, 'internship_subtype': None},
    # 'learning_container_year': {'id': 13398194, 'acronym': 'LECON2011', 'in_charge': True, 'common_title': 'Interdependencies and Strategic Behavior', 'container_type': 'COURSE'}}
    learning_unit_yr = get_by_id(initial_data.get('learning_unit_year')['id'])
    requirement_entity = find_by_id(initial_data.get('entities')['REQUIREMENT_ENTITY'])
    allocation_entity = find_by_id(initial_data.get('entities')['ALLOCATION_ENTITY'])
    add1_requirement_entity = find_by_id(initial_data.get('entities')['ADDITIONAL_REQUIREMENT_ENTITY_1'])
    add2_requirement_entity = find_by_id(initial_data.get('entities')['ADDITIONAL_REQUIREMENT_ENTITY_2'])
    campus = find_campus_by_id(initial_data.get('learning_unit_year')['campus'])

    organization = get_organization_from_learning_unit_year(learning_unit_yr)
    language = find_language_by_id(initial_data.get('learning_unit_year')['language'])

    return [
        str(_('Learning unit')),
        initial_data.get('learning_unit_year')['acronym'],
        learning_unit_yr.academic_year.name,  # pas dans initial
        dict(LEARNING_CONTAINER_YEAR_TYPES)[initial_data.get('learning_container_year')['container_type']] if
        initial_data.get('learning_container_year')['container_type'] else '-',
        translate_status(learning_unit_yr.status),  # pas dans initial
        learning_unit_yr.get_subtype_display(),  # pas dans initial
        get_translation(initial_data.get('learning_unit_year')['internship_subtype']),
        initial_data.get('learning_unit_year')['credits'],
        language.name if language else EMPTY_VALUE,
        dict(PERIODICITY_TYPES)[initial_data.get('learning_unit_year')['periodicity']] if initial_data.get('learning_unit_year')['periodicity'] else EMPTY_VALUE,
        get_translation(learning_unit_yr.quadrimester),  # pas dans initial
        get_translation(learning_unit_yr.session),  # pas dans initial
        initial_data.get('learning_container_year')['common_title'],
        initial_data.get('learning_unit_year')['specific_title'],
        learning_unit_yr.learning_container_year.common_title_english,  # pas dans initial
        learning_unit_yr.specific_title_english,  # pas dans initial
        requirement_entity.most_recent_acronym if requirement_entity else EMPTY_VALUE,
        allocation_entity.most_recent_acronym if allocation_entity else EMPTY_VALUE,
        add1_requirement_entity.most_recent_acronym if add1_requirement_entity else EMPTY_VALUE,
        add2_requirement_entity.most_recent_acronym if add2_requirement_entity else EMPTY_VALUE,
        xls_build.translate(learning_unit_yr.professional_integration),  # pas dans initial
        organization.name if organization else EMPTY_VALUE,
        campus if campus else EMPTY_VALUE,
    ]


def _check_changes(initial_data, proposal_data, line_index):
    modifications = []
    for col_index, obj in enumerate(initial_data):
        if col_index > 1:
            if obj != proposal_data[col_index] :
                modifications.append('{}{}'.format(get_column_letter(col_index + 1), line_index))
    return modifications
