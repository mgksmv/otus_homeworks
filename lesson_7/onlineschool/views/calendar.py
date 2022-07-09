import calendar
from datetime import datetime, timedelta

from django.views.generic import ListView
from django.utils.safestring import mark_safe

from ..models import Schedule
from ..forms import DateForm
from ..utils import EventCalendar


def get_date(req_day):
    if req_day:
        try:
            year, month, day = (int(x) for x in req_day.split('-'))
            return datetime(year, month, day)
        except ValueError:
            year, month = (int(x) for x in req_day.split('-'))
            return datetime(year, month, day=1)
    return datetime.today()


def prev_month(current_date):
    first = current_date.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'date=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(current_date):
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    last = current_date.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'date=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class ScheduleCalendarView(ListView):
    model = Schedule
    template_name = 'onlineschool/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = get_date(self.request.GET.get('date', None))
        cal = EventCalendar(current_date.year, current_date.month, current_date.day)
        html_cal = cal.formatmonth(withyear=True)

        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(current_date)
        context['next_month'] = next_month(current_date)
        context['form'] = DateForm()

        return context