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
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView

from base import models as mdl
from base.forms.organization import OrganizationFilter
from base.models.organization import Organization
from reference import models as mdlref


class OrganizationSearch(PermissionRequiredMixin, FilterView):
    model = Organization
    paginate_by = 20
    template_name = "organization/organizations.html"

    filterset_class = OrganizationFilter
    permission_required = 'base.can_access_organization'
    raise_exception = True


class DetailOrganization(PermissionRequiredMixin, DetailView):
    model = Organization
    template_name = "organization/organization.html"

    permission_required = 'base.can_access_organization'
    raise_exception = True

    pk_url_kwarg = "organization_id"


class UpdateOrganization(PermissionRequiredMixin, UpdateView):
    model = Organization
    fields = ("acronym", "name", "website", "prefix", "start_date", "end_date", "logo")
    template_name = "organization/organization_form.html"
    pk_url_kwarg = "organization_id"

    permission_required = 'base.can_access_organization'
    raise_exception = True


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_read(request, organization_address_id):
    organization_address = mdl.organization_address.find_by_id(organization_address_id)
    organization_id = organization_address.organization.id
    return render(
        request, "organization/organization_address.html",
        {
            'organization_address': organization_address,
            'organization_id': organization_id
        }
    )


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_edit(request, organization_address_id):
    organization_address = mdl.organization_address.find_by_id(organization_address_id)
    organization_id = organization_address.organization.id
    countries = mdlref.country.find_all()
    return render(request, "organization/organization_address_form.html",
                  {'organization_address': organization_address,
                   'organization_id': organization_id,
                   'countries': countries})


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_save(request, organization_address_id):
    if organization_address_id:
        organization_address = mdl.organization_address.find_by_id(organization_address_id)
    else:
        organization_address = mdl.organization_address.OrganizationAddress()

    organization_address.label = request.POST.get('organization_address_label')
    organization_address.location = request.POST.get('organization_address_location')
    organization_address.postal_code = request.POST.get('organization_address_postal_code')
    organization_address.city = request.POST.get('organization_address_city')

    country = request.POST.get('country')
    if country is not None:
        organization_address.country = mdlref.country.find_by_id(int(country))

    organization_id = request.POST.get('organization_id')
    if organization_id is not None:
        organization_address.organization = mdl.organization.find_by_id(int(organization_id))

    organization_address.save()

    return HttpResponseRedirect(
        reverse("organization_address_read", args=[organization_address.pk])
    )


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_new(request):
    try:
        return organization_address_save(request, None)
    except IntegrityError:
        messages.error(request, _("organization_address_save_error"))
        return redirect('organizations')


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_create(request, organization_address_id):
    organization_address = mdl.organization_address.OrganizationAddress()
    organization = mdl.organization.find_by_id(organization_address_id)
    countries = mdlref.country.find_all()
    return render(request, "organization/organization_address_form.html",
                  {'organization_address': organization_address,
                   'organization_id': organization.id,
                   'countries': countries})


@login_required
@permission_required('base.can_access_organization', raise_exception=True)
def organization_address_delete(request, organization_address_id):
    organization_address = mdl.organization_address.find_by_id(organization_address_id)
    organization_address.delete()
    return HttpResponseRedirect(
        reverse("organization_read", args=[organization_address.organization.latest_version.pk])
    )
