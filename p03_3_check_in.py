#importing the stuff I need
import random
from datetime import datetime
from p03_1_db_classes import Customer, Stylist, Appointment


hairstyles_dict = {
    "Undercut": 22.0,
    "Mullet": 18.0,
    "Fade": 20.0,
    "Buzz Cut": 15.0,
    "Pixie Cut": 30.0,
    "Bob": 28.0,
    "Pompadour": 40.0,
    "Layered Cut": 25.0,
    "Crew Cut": 16.0,
    "Shag": 35.0
}

#getting rid of hyphens and spaces in phone numbers
def clean_phone_number(phone_input):
    phone_input = phone_input.replace("-", "")
    phone_input = phone_input.replace(" ", "")
    return phone_input


#loop to keep asking until the phone number is valid
def get_valid_phone_number():
    valid_phone = False

    while valid_phone == False:
        phone_input = input("Hello! Welcome to Incredible Cuts. Please enter your phone number to check in: ")
        cleaned_number = clean_phone_number(phone_input)

        if cleaned_number.isdigit() and len(cleaned_number) == 10:
            valid_phone = True
            return cleaned_number
        else:
            print("That wasn't a 10 digit phone number. Please try again.")


#check if customer already exists, if not create one
def get_or_create_customer(phone_number):
    customer = Customer.get_or_none(Customer.c_phone_number == phone_number)

    if customer != None:
        return customer, False
    else:
        print("\nThanks for joining us! Enter the following information:")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        gender = input("Enter your gender (M or F): ")
        gender = gender.upper()

        customer = Customer.create(
            c_first_name=first_name,
            c_last_name=last_name,
            c_phone_number=phone_number,
            c_gender=gender
        )

        return customer, True


#lets user choose a haircut
def choose_hairstyle():
    print("These are the available hairstyles: ")

    hairstyle_list = list(hairstyles_dict.keys())

    number = 1
    for hairstyle in hairstyle_list:
        print(f"{number}: {hairstyle}")
        number += 1

    choice = int(input("Enter the number of the hairstyle you want: "))
    chosen_hairstyle = hairstyle_list[choice - 1]

    return chosen_hairstyle


#lets user choose a stylist
def choose_stylist(customer):
    option = input("To get the first available stylist regardless of gender, enter 1. If you want your stylist to be the same gender as you, enter 2: ")

    all_stylists = list(Stylist.select())

    if option == "1":
        stylist = random.choice(all_stylists)
        return stylist

    elif option == "2":
        matching_stylists = []

        for stylist in all_stylists:
            if stylist.s_gender == customer.c_gender:
                matching_stylists.append(stylist)

        if len(matching_stylists) > 0:
            stylist = random.choice(matching_stylists)
            return stylist
        else:
            stylist = random.choice(all_stylists)
            return stylist


#main function that runs the check in process
def main():
    phone_number = get_valid_phone_number()
    customer, is_new_customer = get_or_create_customer(phone_number)

    hairstyle = ""
    stylist = None

    #returning customer
    if is_new_customer == False:
        most_recent_appointment = customer.returning_customer_message()

        if most_recent_appointment != None:
            reuse_options = input("Do you want to continue with these same options? Enter 'Y' if so, otherwise enter 'N': ")

            if reuse_options.upper() == "Y":
                hairstyle = most_recent_appointment.a_haircut_type
                stylist = most_recent_appointment.s_id

    #new customer or returning customer who wants new options
    if hairstyle == "" or stylist == None:
        hairstyle = choose_hairstyle()
        stylist = choose_stylist(customer)

    print(f"{stylist.s_first_name} {stylist.s_last_name} gave you a {hairstyle} haircut today!")

    satisfied_input = input("Are you satisfied? Enter Y or N: ")

    if satisfied_input.upper() == "Y":
        satisfied = True
    else:
        satisfied = False

    Appointment.create(
        a_haircut_type=hairstyle,
        a_date_time=datetime.today(),
        a_payment=hairstyles_dict[hairstyle],
        a_satisfied=satisfied,
        c_id=customer,
        s_id=stylist
    )

    print("\nThank you for choosing Incredible Cuts! We hope to see you again soon.")


if __name__ == '__main__':
    main()