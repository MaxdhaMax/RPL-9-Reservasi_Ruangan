from WebApp import db, create_app, bcrypt
from WebApp.model import Room, User, Person_In_Charge, Booked
from mock_data import RoomList, EventList, UserList, PersonInCharge
from mock_data.utils import random_date
from datetime import datetime
import random
import json


def drop_database(app):
    with app.app_context():
        db.drop_all()


def drop_everything(app):
    print("[+] Dropping all current database")
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    with app.app_context():
        con = db.engine.connect()
        trans = con.begin()
        inspector = Inspector.from_engine(db.engine)

        # We need to re-create a minimal metadata with only the required things to
        # successfully emit drop constraints and tables commands for postgres (based
        # on the actual schema of the running instance)
        meta = MetaData()
        tables = []
        all_fkeys = []

        for table_name in inspector.get_table_names():
            fkeys = []

            for fkey in inspector.get_foreign_keys(table_name):
                if not fkey["name"]:
                    continue

                fkeys.append(db.ForeignKeyConstraint(
                    (), (), name=fkey["name"]))

            tables.append(Table(table_name, meta, *fkeys))
            all_fkeys.extend(fkeys)

        for fkey in all_fkeys:
            con.execute(DropConstraint(fkey))

        for table in tables:
            con.execute(DropTable(table))

        trans.commit()


def create_database(app):
    with app.app_context():
        print("[+] Creating all current database")
        db.create_all()


def create_mockData(app):
    with app.app_context():
        username = "admin"
        password = "Admin"
        email = "admin@gmail.com"
        hashedPassword = bcrypt.generate_password_hash(
            "Admin").decode('utf-8')
        user = User(username=username,
                    email=email, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        print(f"[+] Generate admin user")
        print(f"    [>] username = {username}")
        print(f"    [>] email = {email}")
        print(f"    [>] password = {password}")

        for i, user_data in enumerate(UserList):
            print(f"[+] Generating user {i}")
            username = user_data["username"]
            password = user_data["password"]
            email = user_data["email"]
            user = User(username=username,
                        email=email, password=password)
            db.session.add(user)
            db.session.commit()

        for i, (roomdat, pic) in enumerate(zip(RoomList, PersonInCharge)):
            print(f"[+] Creating Room {i}")
            name = roomdat["name"]
            location = roomdat["location"]
            room_type = roomdat["room_type"]
            information = roomdat["information"]
            pic_name = pic["name"]
            pic_number = pic["number"]
            list_person_in_charge = []
            person_in_charge = Person_In_Charge(
                name=pic_name, number=pic_number)
            list_person_in_charge.append(person_in_charge)
            room = Room(name=name, location=location,
                        room_type=room_type, information=information,
                        capacity=random.randint(100, 150), price=random.randint(100000, 300000),
                        person_in_charge=list_person_in_charge)
            db.session.add(room)
            db.session.commit()

        for i in range(1, len(RoomList) + 1):
            print(f"[+] Booking room {i}")
            for event in EventList:
                user = User.query.filter_by(id=random.randint(1, 149)).first()
                room = Room.query.filter_by(id=i).first()
                daterand = datetime.strptime(random_date(
                    "2021/1/1", "2021/12/31", random.random()),
                    "%Y/%m/%d").date()
                isBooked = Booked.query.filter_by(
                    room_booked=room, date=daterand).first()
                if(isBooked):
                    continue
                booked = Booked(
                    booked_by=user, room_booked=room,
                    date=daterand, event=event["event"],
                    organization=event["organization"],
                    phone=event['phone'], email=event['email'],
                    name=event["name"])
                db.session.add(booked)
                db.session.commit()

        print(f"[+] To login as admin, use the following credential")
        print(f"    [>] email = admin@gmail.com")
        print(f"    [>] password = Admin")


if __name__ == "__main__":
    app = create_app()
    drop_everything(app)
    create_database(app)
    create_mockData(app)
