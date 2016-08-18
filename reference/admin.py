##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.contrib import admin
from reference.models import *

admin.site.register(assimilation_criteria.AssimilationCriteria,
                    assimilation_criteria.AssimilationCriteriaAdmin)

admin.site.register(continent.Continent,
                    continent.ContinentAdmin)

admin.site.register(currency.Currency,
                    currency.CurrencyAdmin)

admin.site.register(country.Country,
                    country.CountryAdmin)

admin.site.register(decree.Decree,
                    decree.DecreeAdmin)

admin.site.register(domain.Domain,
                    domain.DomainAdmin)

admin.site.register(education_institution.EducationInstitution,
                    education_institution.EducationInstitutionAdmin)

admin.site.register(education_type.EducationType,
                    education_type.EducationTypeAdmin)

admin.site.register(language.Language,
                    language.LanguageAdmin)

admin.site.register(offer_year_domain.OfferYearDomain,
                    offer_year_domain.OfferYearDomainAdmin)
