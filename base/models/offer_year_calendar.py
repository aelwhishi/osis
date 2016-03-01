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

from django.db import models
from django.utils import timezone
from django.contrib import admin
from base.enums import EVENT_TYPE
from base.models import academic_calendar, offer_year


class OfferYearCalendarAdmin(admin.ModelAdmin):
    list_display = ('academic_calendar', 'offer_year', 'event_type', 'start_date', 'end_date', 'changed')
    list_filter = ('event_type',)
    fieldsets = ((None, {'fields': ('offer_year', 'academic_calendar', 'event_type', 'start_date', 'end_date')}),)
    raw_id_fields = ('offer_year',)
    search_fields = ['event_type']


class OfferYearCalendar(models.Model):
    external_id       = models.CharField(max_length=100, blank=True, null=True)
    changed           = models.DateTimeField(null=True)
    academic_calendar = models.ForeignKey(academic_calendar.AcademicCalendar)
    offer_year        = models.ForeignKey(offer_year.OfferYear)
    event_type        = models.CharField(max_length=50, choices=EVENT_TYPE)
    start_date        = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date          = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    customized        = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s - %s" % (self.academic_calendar, self.offer_year, self.event_type)


def save(acad_calendar):
    academic_yr = acad_calendar.academic_year

    offer_year_list = offer_year.find_offer_years_by_academic_year(academic_yr.id)
    for offer_yr in offer_year_list:
        offer_yr_calendar = OfferYearCalendar()
        offer_yr_calendar.academic_calendar = acad_calendar
        offer_yr_calendar.offer_year = offer_yr
        offer_yr_calendar.start_date = acad_calendar.start_date
        offer_yr_calendar.end_date = acad_calendar.end_date
        offer_yr_calendar.save()


def offer_year_calendar_by_current_session_exam():
    return OfferYearCalendar.objects.filter(event_type__startswith='EXAM_SCORES_SUBMISSION_SESS_') \
                                    .filter(start_date__lte=timezone.now()) \
                                    .filter(end_date__gte=timezone.now()).first()


def find_offer_years_by_academic_calendar(academic_cal):
    return OfferYearCalendar.objects.filter(academic_calendar=int(academic_cal.id))


def find_offer_year_calendar(offer_yr):
    return OfferYearCalendar.objects.filter(offer_year=offer_yr,
                                            start_date__isnull=False,
                                            end_date__isnull=False).order_by('start_date',
                                                                             'academic_calendar__title')