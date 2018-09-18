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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

from django.test import TestCase

from django.utils.translation import ugettext_lazy as _

from base.tests.factories.learning_unit_year import LearningUnitYearFactory
from base.tests.factories.proposal_learning_unit import ProposalLearningUnitFactory
from base.tests.factories.person import PersonFactory
from base.business.learning_unit_xls import DEFAULT_LEGEND_STYLES, SPACES, PROPOSAL_LINE_STYLES, _update_volumes_data, \
    _get_significant_volume, _initialize_component_data, _prepare_legend_ws_data, _get_wrapped_cells, _get_colored_rows, \
    _get_attribution_line, _get_col_letter, _get_formations_by_educ_group_year, _add_training_data
from base.models.enums import proposal_type, proposal_state
from base.tests.factories.academic_year import create_current_academic_year
from base.tests.factories.learning_container_year import LearningContainerYearFactory
from base.tests.factories.learning_component_year import LearningComponentYearFactory
from base.tests.factories.education_group_year import EducationGroupYearFactory
from base.tests.factories.group_element_year import GroupElementYearFactory
from base.models.enums import learning_component_year_type
from osis_common.document import xls_build
from base.models.enums import education_group_categories
from base.tests.factories.education_group_type import EducationGroupTypeFactory

COL_TEACHERS_LETTER = 'L'
COL_PROGRAMS_LETTER = 'Z'
PARENT_PARTIAL_ACRONYM = 'LDROI'
PARENT_ACRONYM='LBIR'
PARENT_TITLE='TITLE 1'
ROOT_ACRONYM='DRTI'


class TestLearningUnitXls(TestCase):

    def setUp(self):
        self.current_academic_year = create_current_academic_year()
        self.learning_container_yr = LearningContainerYearFactory(academic_year=self.current_academic_year)
        self.learning_unit_yr_1 = LearningUnitYearFactory(academic_year=self.current_academic_year,
                                                          learning_container_year=self.learning_container_yr,
                                                          credits=50)
        self.learning_unit_yr_2 = LearningUnitYearFactory()

        self.proposal_creation_1 = ProposalLearningUnitFactory(
            state=proposal_state.ProposalState.ACCEPTED.name,
            type=proposal_type.ProposalType.CREATION.name,
        )
        self.proposal_creation_2 = ProposalLearningUnitFactory(
            state=proposal_state.ProposalState.ACCEPTED.name,
            type=proposal_type.ProposalType.CREATION.name,
        )
        direct_parent_type = EducationGroupTypeFactory(name='Bachelor', category=education_group_categories.TRAINING)

        self.an_education_group_parent = EducationGroupYearFactory(academic_year=self.current_academic_year,
                                                                   education_group_type=direct_parent_type,
                                                                   acronym=ROOT_ACRONYM)
        self.group_element_child = GroupElementYearFactory(
            parent=self.an_education_group_parent,
            child_branch=None,
            child_leaf=self.learning_unit_yr_1
        )
        self.an_education_group = EducationGroupYearFactory(academic_year=self.current_academic_year,
                                                            acronym=PARENT_ACRONYM,
                                                            title=PARENT_TITLE,
                                                            partial_acronym=PARENT_PARTIAL_ACRONYM)

        GroupElementYearFactory(
            parent=self.an_education_group,
            child_branch=self.group_element_child.parent,
        )

    def test_get_wrapped_cells_with_teachers_and_programs(self):
        styles = _get_wrapped_cells([self.learning_unit_yr_1, self.learning_unit_yr_2],
                                    COL_TEACHERS_LETTER,
                                    COL_PROGRAMS_LETTER)
        self.assertCountEqual(styles, ['{}2'.format(COL_TEACHERS_LETTER),
                                       '{}2'.format(COL_PROGRAMS_LETTER),
                                       '{}3'.format(COL_TEACHERS_LETTER),
                                       '{}3'.format(COL_PROGRAMS_LETTER)])

    def test_get_wrapped_cells_with_teachers(self):
        styles = _get_wrapped_cells([self.learning_unit_yr_1, self.learning_unit_yr_2], COL_TEACHERS_LETTER, None)
        self.assertCountEqual(styles, ['{}2'.format(COL_TEACHERS_LETTER),
                                       '{}3'.format(COL_TEACHERS_LETTER)])

    def test_get_wrapped_cells_with_programs(self):
        styles = _get_wrapped_cells([self.learning_unit_yr_1, self.learning_unit_yr_2], None, COL_PROGRAMS_LETTER)
        self.assertCountEqual(styles, ['{}2'.format(COL_PROGRAMS_LETTER),
                                       '{}3'.format(COL_PROGRAMS_LETTER)])

    def test_get_col_letter(self):
        title_searched = 'title 2'
        titles = ['title 1', title_searched, 'title 3']
        self.assertEqual(_get_col_letter(titles, title_searched), 'B')
        self.assertIsNone(_get_col_letter(titles, 'whatever'))

    def test_get_colored_rows(self):
        self.assertEqual(_get_colored_rows([self.learning_unit_yr_1,
                                            self.learning_unit_yr_2,
                                            self.proposal_creation_1.learning_unit_year,
                                            self.proposal_creation_2.learning_unit_year]),
                         {PROPOSAL_LINE_STYLES.get(self.proposal_creation_1.type): [3, 4]})

    def test_get_attribution_line(self):
        a_person = PersonFactory(last_name="Smith", first_name='Aaron')
        attribution_dict = {
            'LECTURING': 10,
            'substitute': None,
            'duration': 3,
            'PRACTICAL_EXERCISES': 15,
            'person': a_person,
            'function': 'CO_HOLDER',
            'start_year': 2017
        }
        self.assertEqual(_get_attribution_line(attribution_dict),
                         "{} - {} : {} - {} : {} - {} : {} - {} : {} - {} : {} - {} : {} ".format(
                             'SMITH, Aaron',
                             _('function'),
                             _('CO_HOLDER'),
                             _('substitute'),
                             '',
                             _('Beg. of attribution'),
                             2017,
                             _('Attribution duration'),
                             3,
                             _('Attrib. vol1'),
                             10,
                             _('Attrib. vol2'),
                             15,)
                         )

    def test_get_significant_volume(self):
        self.assertEqual(_get_significant_volume(10), 10)
        self.assertEqual(_get_significant_volume(None), '')
        self.assertEqual(_get_significant_volume(0), '')

    def test_get_volumes(self):
        volumes = {
            learning_component_year_type.LECTURING: _initialize_component_data(),
            learning_component_year_type.PRACTICAL_EXERCISES: _initialize_component_data()
        }
        lecturing_data = {'PLANNED_CLASSES': 1, 'VOLUME_Q1': 10, 'VOLUME_TOTAL': 50, 'VOLUME_Q2': 40}
        compo = {
            'learning_component_year': LearningComponentYearFactory(learning_container_year=self.learning_container_yr,
                                                                    type=learning_component_year_type.LECTURING),
            'volumes': lecturing_data
        }
        volumes_updated = _update_volumes_data(compo, volumes)
        self.assertCountEqual(volumes_updated.get(learning_component_year_type.LECTURING),
                              lecturing_data)
        self.assertCountEqual(volumes_updated.get(learning_component_year_type.PRACTICAL_EXERCISES),
                              _initialize_component_data())

    def test_prepare_legend_ws_data(self):
        expected = {
            xls_build.HEADER_TITLES_KEY: [str(_('Legend'))],
            xls_build.CONTENT_KEY: [
                [SPACES, _('proposal_creation')],
                [SPACES, _('Proposal for modification')],
                [SPACES, _('Suppression proposal')],
                [SPACES, _('Transformation proposal')],
                [SPACES, _('Transformation/modification proposal')],
            ],
            xls_build.WORKSHEET_TITLE_KEY: _('Legend'),
            xls_build.STYLED_CELLS:
                DEFAULT_LEGEND_STYLES
        }
        self.assertEqual(_prepare_legend_ws_data(), expected)

    def test_get_formations_by_educ_group_year(self):

        formations = _get_formations_by_educ_group_year(self.learning_unit_yr_1)

        self.assertCountEqual(formations.get(self.group_element_child.id),
                              [self.an_education_group])

    def test_add_training_data(self):
        formations = _add_training_data(self.learning_unit_yr_1)

        expected = "{} {} {} {}".format(
            '',
            self.an_education_group_parent.partial_acronym,
            "({})".format(
                '{0:.2f}'.format(self.learning_unit_yr_1.credits)
            ),
            " {} - {} ".format(PARENT_ACRONYM, PARENT_TITLE)
        )

        self.assertEqual(formations, expected)
