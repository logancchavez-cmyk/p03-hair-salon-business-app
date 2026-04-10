# create your peewee models and the hair_salon.db database here
# Logan Chavez IS303

from peewee import *

# creating the database
db = SqliteDatabase('hair_salon.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


# making customer class
class Customer(BaseModel):
    c_id = AutoField(primary_key=True)
    c_first_name = CharField()
    c_last_name = CharField()
    c_phone_number = CharField()
    c_gender = CharField()

    def returning_customer_message(self):
        appointment_count = self.appointments.count()
        print(f"Welcome! You've had {appointment_count} appointments with us!")

        if appointment_count == 0:
            return None
        else:
            all_appointments = self.appointments.order_by(Appointment.a_date_time.desc())
            most_recent_appointment = all_appointments.get()

            print(
                f"At your last haircut on {most_recent_appointment.a_date_time} "
                f"you got a {most_recent_appointment.a_haircut_type} haircut "
                f"with {most_recent_appointment.s_id.s_first_name} as your stylist."
            )

            return most_recent_appointment


# making stylist class
class Stylist(BaseModel):
    s_id = AutoField(primary_key=True)
    s_first_name = CharField()
    s_last_name = CharField()
    s_hire_date = DateField()
    s_gender = CharField()


# making appointment class
class Appointment(BaseModel):
    a_id = AutoField(primary_key=True)
    a_haircut_type = CharField()
    a_date_time = DateTimeField()
    a_payment = FloatField()
    a_satisfied = BooleanField()
    c_id = ForeignKeyField(Customer, backref='appointments', on_delete='CASCADE')
    s_id = ForeignKeyField(Stylist, backref='appointments', on_delete='CASCADE')

    def get_appointment_info(self):
        if self.a_satisfied == True:
            message = (
                f"Appointment {self.a_id} on {self.a_date_time}: "
                f"{self.c_id.c_first_name} {self.c_id.c_last_name} got a "
                f"{self.a_haircut_type} from "
                f"{self.s_id.s_first_name} {self.s_id.s_last_name}. "
                f"{self.c_id.c_first_name} was satisified."
            )
        else:
            message = (
                f"Appointment {self.a_id} on {self.a_date_time}: "
                f"{self.c_id.c_first_name} {self.c_id.c_last_name} got a "
                f"{self.a_haircut_type} from "
                f"{self.s_id.s_first_name} {self.s_id.s_last_name}. "
                f"{self.c_id.c_first_name} was not satisified."
            )

        return message


def start_from_scratch(db_to_restart=db):
    db_to_restart.connect()

    tables_to_drop = ['appointment', 'stylist', 'customer']

    with db_to_restart.atomic():
        for table in tables_to_drop:
            db.execute_sql(f"DROP TABLE IF EXISTS {table};")

    db_to_restart.create_tables([Customer, Stylist, Appointment])
    db_to_restart.close()

    print("Recreated database structure from scratch")


if __name__ == '__main__':
    start_from_scratch(db)