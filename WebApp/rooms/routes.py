from flask import Blueprint

rooms = Blueprint('rooms', __name__)


@rooms.route("/room")
def room():
