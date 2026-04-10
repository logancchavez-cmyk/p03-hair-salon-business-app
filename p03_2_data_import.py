#importing the stuff I need
import pandas as pd
import sqlite3
from p03_1_db_classes import start_from_scratch


#reading in the initial data into a df
combined_df = pd.read_excel("starting_hair_salon_data.xlsx")
print("STARTING DATA:\n", combined_df.head(), "\n")

#taking out the hyphens in the phone numbers
combined_df['c_phone_number'] = combined_df['c_phone_number'].str.replace('-', '')

#making customer and stylist dataframes and removing duplicates
c_df = combined_df[['c_first_name', 'c_last_name', 'c_phone_number', 'c_gender']]
c_df = c_df.drop_duplicates()
c_df = c_df.reset_index(drop=True)

s_df = combined_df[['s_first_name', 's_last_name', 's_gender', 's_hire_date']]
s_df = s_df.drop_duplicates()
s_df = s_df.reset_index(drop=True)

#making id columns
c_df['c_id'] = c_df.index
s_df['s_id'] = s_df.index

#adding foreign keys into the appointment dataframe
a_df = combined_df.merge(
    c_df,
    on=['c_first_name', 'c_last_name', 'c_phone_number', 'c_gender']
)

a_df = a_df.merge(
    s_df,
    on=['s_first_name', 's_last_name', 's_gender', 's_hire_date']
)

#dropping extra columns we do not need anymore
a_df = a_df.drop(
    [
        'c_first_name',
        'c_last_name',
        'c_phone_number',
        'c_gender',
        's_first_name',
        's_last_name',
        's_hire_date',
        's_gender'
    ],
    axis=1
)

#making appointment id column
a_df['a_id'] = a_df.index

#displaying the results
print("CUSTOMER DATA:\n", c_df.head(), "\n")
print("STYLIST DATA:\n", s_df.head(), "\n")
print("APPOINTMENT DATA:\n", a_df.head(), "\n")

#recreating the db starting from scratch
start_from_scratch()

#connecting to the database
db = sqlite3.connect('hair_salon.db')

#exporting the dataframes into sqlite
c_df.to_sql('customer', db, if_exists='append', index=False)
s_df.to_sql('stylist', db, if_exists='append', index=False)
a_df.to_sql('appointment', db, if_exists='append', index=False)

db.close()

print("Exported cleaned and separated data to SQLite database")