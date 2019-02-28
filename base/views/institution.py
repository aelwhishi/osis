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

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.utils.translation import gettext
from mptt.templatetags.mptt_tags import cache_tree_children

from base.forms.entity import EntityVersionFilter
from base.forms.entity_calendar import EntityCalendarEducationalInformationForm
from base.models import entity_version as entity_version_mdl
from base.models.entity import Entity as OldEntity
from base.models.entity_manager import has_perm_entity_manager
from base.views.common import paginate_queryset, display_success_messages
from entity.models.entity_year import EntityYear


@login_required
@permission_required('base.is_institution_administrator', raise_exception=True)
def institution(request):
    return render(request, "institution.html", {'section': 'institution'})


@login_required
@permission_required('base.can_access_mandate', raise_exception=True)
def mandates(request):
    return render(request, "mandates.html", {'section': 'mandates'})


@login_required
@user_passes_test(has_perm_entity_manager)
def academic_actors(request):
    return render(request, "academic_actors.html", {})


@login_required
def get_entity_address(request, entity_version_id):
    version = entity_version_mdl.find_by_id(entity_version_id)
    entity = version.entity
    response = {
        'entity_version_exists_now': version.exists_now(),
        'recipient': '{} - {}'.format(version.acronym, version.title),
        'address': {}
    }
    if entity and entity.has_address():
        response['address'] = {
            'location': entity.location,
            'postal_code': entity.postal_code,
            'city': entity.city,
            'country_id': entity.country_id,
            'phone': entity.phone,
            'fax': entity.fax,
        }
    return JsonResponse(response)


@login_required
def entities_year(request, entity_version_id):
    entity_year = get_object_or_404(EntityYear, pk=entity_version_id)
    annualized_entities = entity_year.entity.entityyear_set.select_related("academic_year")
    return render(request, "entity/versions.html", {'obj': entity_year, 'entities_year': annualized_entities})


@login_required
def entity_read(request, entity_version_id):
    obj = get_object_or_404(EntityYear, pk=entity_version_id)
    old_entity = OldEntity.objects.get(external_id__endswith=obj.entity.esb_id)

    person = request.user.person
    can_user_post = person.is_faculty_manager and person.is_attached_entity(old_entity)

    form = EntityCalendarEducationalInformationForm(old_entity, request.POST or None)
    if can_user_post and form.is_valid():
        display_success_messages(request, gettext("Educational information submission dates updated"))
        form.save_entity_calendar(old_entity)

    return render(request, "entity/identification.html", {
        "obj": obj, "form": form, 'old_entity': old_entity, "can_user_post": can_user_post,
    })


@login_required
def entities_search(request):
    order_by = request.GET.get('order_by', 'acronym')
    qs_filter = EntityVersionFilter(request.GET or None)

    entities_version_list = qs_filter.qs.order_by(order_by)
    entities_version_list = paginate_queryset(entities_version_list, request.GET)

    return render(request, "entities.html", {'entities_version': entities_version_list, 'form': qs_filter.form})


def recursive_node_to_dict(node, limit=3):
    limit -= 1
    return {
        'id': node.pk,
        'acronym': node.acronym,
        'children': [recursive_node_to_dict(c, limit) for c in node.get_children() if limit > 0]
    }


@login_required
def entity_diagram(request, entity_version_id):
    obj = get_object_or_404(EntityYear, pk=entity_version_id)

    # Retrieve descendants of a node up to two levels below it
    tree = cache_tree_children(obj.get_descendants(include_self=True))[0]
    annualized_entities_as_json = json.dumps(recursive_node_to_dict(tree))
    return render(
        request, "entity/organogram.html",
        {
            "obj": obj,
            "entities_version_as_json": annualized_entities_as_json,
        }
    )
