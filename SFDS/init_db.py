from sqlite3 import IntegrityError

from apps.config.db.conn import db_session
from apps.core.models import Role, Organization


def init_data():
    roles = ['STUDENT', 'INSTRUCTOR', 'CSR', "ADMIN"]

    with db_session() as db:
        try:
            for role in roles:
                db_item = Role(name=role)
                db.add(db_item)

            db.commit()
            print("Roles are inserted successfully.")
        except IntegrityError as e:
            print(f"Exception: {str(e)}")
            pass


    organizations = ["SFDS"]
    with db_session() as db:
        try:
            for organization in organizations:
                obj = Organization(name=organization)
                db.add(obj)
            db.commit()
            print("Organizations are inserted successfully.")
        except IntegrityError as e:
            print(f"Exception: {str(e)}")


if __name__ == "__main__":
    init_data()