from p03_1_db_classes import Stylist, Appointment


def show_unsatisfied_appointments():
    appointments = (
        Appointment
        .select()
        .where(Appointment.a_satisfied == False)
        .order_by(Appointment.a_date_time.desc())
        .limit(5)
    )

    for appointment in appointments:
        print(appointment.get_appointment_info())


def delete_stylist():
    stylists = Stylist.select().order_by(Stylist.s_id)

    for stylist in stylists:
        print(f"{stylist.s_id}: {stylist.s_first_name} {stylist.s_last_name}")

    print()
    stylist_id = int(input("Enter the ID of a stylist to delete: "))
    stylist_to_delete = Stylist.get_by_id(stylist_id)

    first_name = stylist_to_delete.s_first_name
    last_name = stylist_to_delete.s_last_name

    stylist_to_delete.delete_instance()
    print(f"{first_name} {last_name} was deleted from the database.")


def main():
    while True:
        print("\nWelcome to Manager Tools. Choose an option below: ")
        print("1. See the 5 most recent appointments that weren't satisfied")
        print("2. Delete a stylist from the database")
        print("3. Exit")
        choice = input("Enter an option: ")

        if choice == '1':
            print()
            show_unsatisfied_appointments()
        elif choice == '2':
            delete_stylist()
        elif choice == '3':
            print("Thank you for using the program.")
            break
        else:
            print("Invalid selection. Try Again.")


if __name__ == '__main__':
    main()