from flask_marshmallow import Marshmallow
from WebApp import ma


class BookedSchema(ma.Schema):
    class Meta:
        fields = ('date', 'event', 'organization', 'name',
                  'booked_by.username', 'room_booked.name')
