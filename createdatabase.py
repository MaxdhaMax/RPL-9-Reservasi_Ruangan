from WebApp import db, create_app, bcrypt
from WebApp.model import Room, User
import random


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

        RoomList = [['Dicranodontium Moss', 'FMIPA', 'Auditorium', 'Universal exuding focus group'],
                    ['Colorado Four O''clock', 'FEMA', 'Auditorium',
                        'Customer-focused reciprocal groupware'],
                    ['Thurber''s Sandpaper Plant', 'FEM', 'Auditorium',
                        'Centralized homogeneous superstructure'],
                    ['Leadville Milkvetch', 'FEMA', 'Ruang Terbuka',
                        'Customer-focused mobile toolset'],
                    ['Rough Draba', 'SB', 'Ruang Terbuka',
                        'Multi-tiered homogeneous middleware'],
                    ['Acorn Buckwheat', 'FEM', 'Ruang Terbuka',
                    'Advanced contextually-based secured line'],
                    ['Sawleaf Bush Penstemon', 'REKTORAT', 'Ruang Kelas',
                    'Organized zero defect architecture'],
                    ['Guiana Brosimum', 'FEMA', 'Ruang Terbuka',
                    'Horizontal actuating architecture'],
                    ['Gregg''s Tube Tongue', 'FEMA', 'Ruang Terbuka',
                    'Expanded fresh-thinking synergy'],
                    ['Plantainleaf Dubautia', 'FMIPA', 'Ruang Terbuka',
                    'Enterprise-wide zero administration database'],
                    ['Canada Lily', 'FEMA', 'Ruang Kelas',
                        'Object-based analyzing emulation'],
                    ['Alyssumleaf Phlox', 'FEMA', 'Ruang Terbuka',
                    'Cloned multi-state conglomeration'],
                    ['Hybrid Oak', 'FEMA', 'Ruang Kelas',
                    'Realigned bandwidth-monitored focus group'],
                    ['Sparse-flowered Bog Orchid', 'FEMA', 'Auditorium',
                    'Horizontal responsive service-desk'],
                    ['Chamomile', 'FMIPA', 'Ruang Terbuka',
                        'Robust analyzing success'],
                    ['Common Starlily', 'FMIPA', 'Ruang Terbuka',
                    'Virtual 4th generation throughput'],
                    ['Southern Globethistle', 'FEMA', 'Ruang Kelas',
                    'Customizable content-based contingency'],
                    ['Hornwort', 'FAHUTAN', 'Ruang Terbuka',
                    'Cross-group needs-based open architecture'],
                    ['Panic Veldtgrass', 'SB', 'Ruang Terbuka',
                    'Multi-layered value-added middleware'],
                    ['Arctoparmelia Lichen', 'FEMA', 'Ruang Terbuka',
                    'Cross-group secondary intranet'],
                    ['Dicranoweisia Moss', 'REKTORAT', 'Ruang Kelas',
                    'Multi-layered client-driven policy'],
                    ['Alkanna', 'FEM', 'Auditorium',
                        'Vision-oriented zero tolerance internet solution'],
                    ['Vaupesia', 'FAHUTAN', 'Ruang Kelas',
                        'Grass-roots exuding encoding'],
                    ['Caloncoba', 'FMIPA', 'Ruang Terbuka',
                        'Multi-lateral maximized interface'],
                    ['Great Lakes Dewberry', 'FEM', 'Ruang Kelas',
                        'Phased high-level capability'],
                    ]

        for i in range(len(RoomList)):
            print(f"[+] Creating Room {i}")
            name = RoomList[i][0]
            location = RoomList[i][1]
            room_type = RoomList[i][2]
            information = RoomList[i][3]
            room = Room(name=name, location=location,
                        room_type=room_type, information=information, capacity=random.randint(100, 150))
            db.session.add(room)
            db.session.commit()

        print(f"[+] To login as admin the following credential")
        print(f"    [>] email = {email}")
        print(f"    [>] password = {password}")


if __name__ == "__main__":
    app = create_app()
    drop_everything(app)
    create_database(app)
    create_mockData(app)
