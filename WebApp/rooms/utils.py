from datetime import date, timedelta
from WebApp import ma


class BookedSchema(ma.Schema):
    class Meta:
        fields = ('date', 'event', 'organization', 'name',
                  'booked_by.username', 'room_booked.name')


def ListBetweenTwoDates(first_date: date, second_date: date):
    delta = second_date - first_date
    dateBetween = []
    for i in range(delta.days + 1):
        day = first_date + timedelta(days=i)
        daystr = day.strftime("%Y-%m-%d")
        dateBetween.append(daystr)
    return dateBetween
