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
import json
import logging
from threading import Thread

import requests
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from base.business.education_groups.general_information_sections import COMMON_GENERAL_INFO_SECTIONS
from base.models.group_element_year import find_learning_unit_formations


logger = logging.getLogger(settings.DEFAULT_LOGGER)


def publish(education_group_year):
    if not all([settings.ESB_API_URL, settings.ESB_AUTHORIZATION, settings.ESB_REFRESH_PEDAGOGY_ENDPOINT,
                settings.URL_TO_PORTAL_UCL]):
        raise ImproperlyConfigured('ESB_API_URL / ESB_AUTHORIZATION / ESB_REFRESH_PEDAGOGY_ENDPOINT / '
                                   'URL_TO_PORTAL_UCL / must be set in configuration')

    trainings = find_learning_unit_formations([education_group_year], parents_as_instances=True)

    education_groups_to_publish = [education_group_year] + trainings.get(education_group_year.pk, [])
    t = Thread(target=_bulk_publish, args=(education_groups_to_publish,))
    t.start()
    return _get_portal_url(education_group_year)


def get_relevant_sections(education_group_year):
    if not all([settings.URL_TO_PORTAL_UCL, settings.GET_SECTION_PARAM]):
        raise ImproperlyConfigured('URL_TO_PORTAL_UCL / GET_SECTION_PARAM must be set in configuration')

    if education_group_year.is_common:
        return COMMON_GENERAL_INFO_SECTIONS

    relevant_sections_url = _get_portal_url(education_group_year) + "?" + settings.GET_SECTION_PARAM
    try:
        response = requests.get(relevant_sections_url, timeout=settings.REQUESTS_TIMEOUT).json()
    except (json.JSONDecodeError, requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        raise RelevantSectionException(_("Unable to retrieve appropriate sections for this programs"))
    return response.get('sections') or []


def _bulk_publish(education_group_years):
    return [_publish(education_group_year) for education_group_year in education_group_years]


def _publish(education_group_year):
    publish_url = _get_url_to_publish(education_group_year)
    try:
        response = requests.get(
            publish_url,
            headers={"Authorization": settings.ESB_AUTHORIZATION},
            timeout=settings.REQUESTS_TIMEOUT
        )
        if response.status_code != HttpResponse.status_code:
            logger.info(
                "The program {acronym} has no page to publish on it".format(acronym=education_group_year.acronym)
            )
            return False
        return True
    except Exception:
        raise PublishException("Unable to publish sections for the program {acronym}".format(
            acronym=education_group_year.acronym)
        )


def _get_url_to_publish(education_group_year):
    code = _get_code_according_type(education_group_year)
    endpoint = settings.ESB_REFRESH_PEDAGOGY_ENDPOINT.format(
        year=education_group_year.academic_year.year,
        code=code
    )
    return "{esb_api}/{endpoint}".format(esb_api=settings.ESB_API_URL, endpoint=endpoint)


def _get_portal_url(education_group_year):
    code = _get_code_according_type(education_group_year)
    return settings.URL_TO_PORTAL_UCL.format(
        year=education_group_year.academic_year.year,
        code=code
    )


def _get_code_according_type(education_group_year):
    if education_group_year.is_minor:
        return "min-{}".format(education_group_year.partial_acronym)
    elif education_group_year.is_deepening:
        return "app-{}".format(education_group_year.partial_acronym)
    return education_group_year.acronym


class PublishException(Exception):
    """Some kind of problem with a publish to ESB. """
    pass


class RelevantSectionException(Exception):
    """Some kind of problem with get relevant section from ESB. """
    pass
