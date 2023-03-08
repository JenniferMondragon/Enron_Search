# Jennifer Mondragon
# Computer Forensics
# Feb 23rd 2023

# In order to clean data, I used the following links as guides
# https://towardsdatascience.com/how-to-show-all-columns-rows-of-a-pandas-dataframe-c49d4507fcf
# https://www.kaggle.com/code/ankur561999/data-cleaning-enron-email-dataset/notebook

import email.utils
import sys

import pandas as pd
import numpy as np
import time
import re

from collections import Counter

# This function is to split the emails in order to extract information easier
def filtering_email(filter, emails):
    col = []
    for message in emails:
        split = email.message_from_string(message)
        col.append(split.get(filter))
    return col

# This function is to pull the message sent with the email
def pull_message(messages):
    col = []
    for message in messages:
        pulled = email.message_from_string(message)
        col.append(pulled.get_payload())
    return col

# This function should print every instance of a term
# IGNORES DUPLICATES IN TERM
# NOT CASE-SENSITIVE
# TESTING LINE
# python main.py term_search rent a ski boat
def term_search(term):
    path = pd.read_csv(r"emails.csv")

    # setting the fields
    path['date'] = filtering_email("Date", path['message'])
    path['To'] = filtering_email("To", path['message'])
    path['body'] = pull_message(path['message'])

    # Removes Duplicate Words and Sets as lowercase
    term = term.lower()
    term = term.split(" ")
    uniques = Counter(term)
    term = " ".join(uniques.keys())
    print(term)

    # Convert to string
    path['body'] = path['body'].astype(str)

    # Makes new frame for emails containing the term
    contains_term = path[path['body'].str.contains(term)]

    # Drops any duplicate emails
    contains_term = contains_term.drop_duplicates(keep=False)

    # Re-arranges the index to start from 1
    contains_term.index = np.arange(1, len(contains_term) + 1)

    # Prints the Information (Name and Date)
    print(contains_term['To'] + " " + contains_term['date']);

    # Count instances
    print("Results Found: ", path['body'].str.contains(term).sum())

# This function should print every email exchanged between two users
# TESTING LINE
# python main.py interaction_search keith.holst@enron.com mike.grigsby@enron.com
def interaction_search(address_one, address_two):
    path = pd.read_csv(r"emails.csv")

    # setting the fields to know who sent the email and who received the email
    path['To'] = filtering_email("To", path['message'])
    path['From'] = filtering_email("From", path['message'] )

    path['To'] = path['To'].astype(str)
    path['From'] = path['From'].astype(str)

    checking = [(path['To'].str.contains(address_one) & path['From'].str.contains(address_two)), (path['To'].str.contains(address_two) & path['From'].str.contains(address_one))]
    columns = [path['To'], path['From']]

    interaction = np.select(checking, columns, default=np.nan)
    pd.set_option('display.max_rows', None)
    print(interaction)

# This function should print every email received and sent by a given person
# TESTING LINE
# python main.py address_search Holst Keith
def address_search(last_name, first_name):
    path = pd.read_csv(r"emails.csv")

    # setting the fields to know who sent the email and who received the email
    path['To'] = filtering_email("To", path['message'])

    # Convert to string
    path['email'] = path['To'].astype(str)

    # Extracts the Email
    path['email'] = path['email'].str.findall('(\S+@\S+)')

    # Drops duplicate names
    # path['email'].drop_duplicates(keep=False)

    # Normnal Filtering
    path['Employee Name'] = filtering_email("X-To", path['message'])

    # Converst to String
    path['Employee Name'] = path['Employee Name'].astype(str)

    # Drops and duplicates
    first_last = first_name + " " + last_name

    # Makes new frame for emails containing the term
    contains_term = path[path['Employee Name'].str.contains(first_last)]

    # Re-arranges the index to start from 1
    contains_term.index = np.arange(1, len(contains_term) + 1)

    # Prints the Information (Name and Date)
    print(contains_term['email'])

    # Count instances
    print("Results Found: ", path['Employee Name'].str.contains(first_last).sum())

if __name__ == "__main__":
    # starts execution time
    start = time.time()

    # to get the arguments passed
    args = sys.argv

    if args[0] != "main.py":
        print("File Calling Error...")

    if args[1] == "term_search":
        args[2] = ' '.join(args[2:])
        term_search(args[2])
    elif args[1] == "interaction_search":
        interaction_search(args[2], args[3])
    elif args[1] == "address_search":
        address_search(args[2], args[3])
    else:
        print("Function Calling Error...")

    # ends and prints execution time
    print("--- %s seconds ---" % (time.time()-start))
