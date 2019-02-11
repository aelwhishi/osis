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
import datetime

import factory
from factory.fuzzy import FuzzyInteger

from base.models.enums import entity_type
from reference.tests.factories.country import CountryFactory


class AcademicYearFactory(factory.DjangoModelFactory):
    class Meta:
        model = "reference.AcademicYear"
        django_get_or_create = ('year',)

    year = factory.fuzzy.FuzzyInteger(1950, datetime.datetime.now().year)
    start_date = factory.LazyAttribute(lambda obj: datetime.date(obj.year, 9, 15))
    end_date = factory.LazyAttribute(lambda obj: datetime.date(obj.year + 1, 9, 30))


class EntityFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'entity.Entity'
        django_get_or_create = ('esb_id',)

    location = factory.Faker('street_address')
    postal_code = factory.Faker('zipcode')
    city = factory.Faker('city')
    country = factory.SubFactory(CountryFactory)
    website = factory.Faker('url')
    phone = factory.Faker('phone_number')
    fax = factory.Faker('phone_number')
    esb_id = FuzzyInteger(12)


class EntityYearFactory(factory.DjangoModelFactory):
    class Meta:
        model = 'entity.EntityYear'

    entity = factory.SubFactory(EntityFactory)
    title = factory.Faker('text', max_nb_chars=255)
    acronym = factory.Faker('text', max_nb_chars=20)
    entity_type = factory.Iterator(entity_type.ENTITY_TYPES, getter=lambda c: c[0])
