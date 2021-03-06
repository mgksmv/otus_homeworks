import locale
from datetime import datetime
from calendar import HTMLCalendar

from .models import Schedule


class EventCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, day=None):
        super().__init__()
        try:
            self.locale = locale.getdefaultlocale()
        except:
            pass
        self.year = year
        self.month = month
        self.day = day

    def formatday(self, day, events):
        data = ''

        for event in events:
            if event.start_date.day == day:
                data += f'<li class="pb-2">{event.get_html_course_url}</li>'

        today = day == datetime.now().day and self.month == datetime.now().month and self.year == datetime.now().year

        if today:
            return f'<td id="day-{day}" class="today" onmouseover="changeBackgroundColorOver({day})" ' \
                   f'onmouseleave="changeBackgroundColorOutToday({day})"><span class="date"><b>{day}</b> ' \
                   f'Сегодня</span><ul>{data}</ul></td>'
        elif day == self.day:
            return f'<td id="day-{day}" class="marked" onmouseover="changeBackgroundColorOver({day})" ' \
                   f'onmouseleave="changeBackgroundColorOutMarked({day})"><span class="date"><b>{day}</b></span> ' \
                   f'<span class="text-danger"><i class="fa-solid fa-thumbtack"></i></span><ul>{data}</ul></td>'
        elif day != 0:
            if len(data) > 0:
                return f'<td id="day-{day}" class="marked-event" onmouseover="changeBackgroundColorOver({day})" ' \
                       f'onmouseleave="changeBackgroundColorOutMarkedEvent({day})"><span class="date">' \
                       f'<b>{day}</b></span><ul>{data}</ul></td>'
            return f'<td id="day-{day}" class="existing-days" onmouseover="changeBackgroundColorOver({day})" ' \
                   f'onmouseleave="changeBackgroundColorOut({day})"><span class="date">{day}</span><ul>{data}</ul></td>'

        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for day, weekday in theweek:
            week += self.formatday(day, events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, withyear=True):
        events = Schedule.objects.filter(start_date__month=self.month, start_date__year=self.year) \
            .select_related('course') \
            .prefetch_related('students')

        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += '</table>'
        return cal
