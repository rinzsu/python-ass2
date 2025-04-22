import csv
import datetime

# set a datetime to simulate the current date and time
now = datetime.datetime(2025, 4, 7, 10)

# lists of all reminder records from the csv file
# reminders_database: stores all reminders 
# reminders_active_database: stores currently active reminders
# reminders_dismissed_database: stores dismissed (past) reminders
reminders_database = []
reminders_active_database = []
reminders_dismissed_database = []

"""
load_database(reminders_file, active_file, dismissed_file)
loads reminders from csv files into their matching databases
"""
def load_database(reminders_file, active_file, dismissed_file):
    # load reminder database
    f = open(reminders_file,"r")
    reader = csv.reader(f,delimiter=",")
    for _, row in enumerate(reader):
        reminders_database.append(row)

    # load active reminder
    f = open(active_file,"r")
    reader = csv.reader(f,delimiter=",")
    for _, row in enumerate(reader):
        reminders_active_database.append(row)

    # load dismissed reminder
    f = open(dismissed_file,"r")
    reader = csv.reader(f,delimiter=",")
    for _, row in enumerate(reader):
        reminders_dismissed_database.append(row)

"""
convert_date_to_datetime(date)
converts a date string ('YYYY-MM-DD HH:MM:SS') to a datetime object

args:
- date (str): the date string to convert

returns:
- datetime: the corresponding datetime object
"""
def convert_date_to_datetime(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

"""
parse_datetime(date)
converts a datetime object to string format ('YYYY-MM-DD HH:MM:SS')
"""
def parse_datetime(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")
"""
check_compare_date(date1, comparison, date2)
compares two dates using a specified operator ('>', '>=', '<', '<=', '=')

args:
- date1 (str): the first date
- comparison (str): the comparison operator
- date2 (str): the second date

returns:
- bool: True if the comparison is valid, False otherwise
"""
def check_compare_date(date1, comparison, date2):
    parsed_1 = convert_date_to_datetime(date1)
    parsed_2 = convert_date_to_datetime(date2)

    # use match-case for comparison operators
    match (comparison):
        case ">":
            return parsed_1 > parsed_2
        case ">=":
            return parsed_1 >= parsed_2
        case "<":
            return parsed_1 < parsed_2
        case "<=":
            return parsed_1 <= parsed_2
        case "=":
            return parsed_1 == parsed_2
"""
print_key_exists(arr, mode="")
show reminders from the list that exist in the main database
"""
def print_key_exists(arr, mode=""):
    for elem in arr:
        if (check_reminder_id_exist(elem[1])):
            fetch_index = int(elem[1]) + 1
            fetch_data = reminders_database[fetch_index]
            print(f"{mode}{fetch_index}. {fetch_data[1]}")

"""
print_reminders_by_index(db,mode="")
print reminders with index numbers and an optional label

args:
- db: the list of reminders
- mode: optional string prefix
"""
def print_reminders_by_index(db,mode=""):
    index = 1
    for reminder in db[:]:
        name = (reminders_database[int(reminder[1])+1][1])
        print(f"{mode}{index}. {name}")
        index += 1

"""
print_reminders_by_index(db, mode="")
prints reminders from the given base data with an index and an optional prefix

args:
- db (list): list of reminders to display
- mode (str): prefix of choice for text reminders (default is "")
"""
def print_reminders(db, mode=""):
    index = len(get_active_reminders())
    used_name = []
    for reminder in db:
        name = (reminders_database[int(reminder[1])+1][1])
        if (name in used_name):
            continue
        else:
            used_name.append(name)
        print(f"{mode}{index + 1}. {name}")
        index += 1

"""
check_reminder_id_exist(reminder_id)
checks if a reminder with the given ID exists in the database

args:
- reminder_id (str): the ID of the reminder to be checked

returns:
bool: True if the reminder ID exists in the database, otherwise False
"""
def check_reminder_id_exist(reminder_id):
    for record in reminders_database[:]:
        if (record[0] == reminder_id):
            return True
    return False

"""
check_date_passed(date1)
checks if the given date has already passed

args:
- date1 (str): the date to check

returns:
- bool: True if the date has passed, False otherwise
"""
def check_date_passed(date1):
    parsed_1 = convert_date_to_datetime(date1)
    return parsed_1 <= now

"""
check_id_exist(findme, arr)
checks if the reminder ID is in the list
"""
def check_id_exist(findme, arr):
    for elem in arr[:]:
        if (elem[1] == findme):
            return True
    return False

"""
get_active_reminders()
returns a list of active reminders, that is, reminders that have been started but not yet closed

returns:
- list: list of active reminders
"""
def get_active_reminders():
    active_reminders = []
    pool_used = []
    for row in reminders_active_database[1:]:
        if (check_id_exist(row[1], reminders_dismissed_database) == False and row[1] not in pool_used):
            pool_used.append(row[1])
            active_reminders.append(row)

    return active_reminders

"""
get_past_reminders()
returns a list of past reminders, which are reminders that have been dismissed after being active

returns:
- list: a list of past reminders
"""
def get_past_reminders():
    past_reminders = []
    for row in reminders_dismissed_database[1:]:
        entry_id, reminder_id, active_from = row
        if (check_date_passed(active_from)):
            past_reminders.append(row)

    return past_reminders

"""
get reminders future()
returns a list of upcoming reminders (not yet been activated)
returns:
- list: List of upcoming reminders
"""
def get_future_reminders():
    future_reminders = []

    for row in reminders_active_database[1:]:
        entry_id, reminder_id, active_from = row

        if (check_date_passed(active_from) == False):
            future_reminders.append(row)

    return future_reminders 

"""
set_reminder(reminder_text, active_from)
adds a new reminder (with the given text and start time)

args:
- reminder_text (str): reminder text
- active_from (datetime): time when the reminder should become active
"""
def set_reminder(reminder_text, active_from):
    # generate a new reminder ID and append to database
    record_reminder_id = str(int(reminders_database[len(reminders_database)-1][0]) + 1)
    record_reminder_text = reminder_text
    record_active_from = parse_datetime(active_from)
    record_dismissed_at = parse_datetime(datetime.datetime.fromtimestamp(0)) 

    reminders_database.append([record_reminder_id, record_reminder_text])

    last_id_active_db = len(reminders_active_database)
    reminders_active_database.append([last_id_active_db, record_reminder_id, record_active_from])

"""
dismiss_reminder(reminder_id)
marks a reminder as completed based on its ID and updates the completion time

args:
- reminder_id (str): the ID of the reminder to dismiss
"""
def dismiss_reminder(reminder_id):
    global reminders_dismissed_database
    last_id_dismissed_db = str(len(reminders_dismissed_database))
    reminders_dismissed_database.append([last_id_dismissed_db, reminder_id, str(now)])

"""
renew_reminder(reminder_id, active_from)
sets a new time for a dismissed reminder to become active again
"""
def renew_reminder(reminder_id, active_from):
    record_reminder_id = reminder_id
    record_active_from = parse_datetime(active_from)

    if (check_reminder_id_exist(record_reminder_id)):
        if (check_date_passed(record_active_from) == False):
            last_id_active_db = str(len(reminders_active_database)-1)
            reminders_active_database.append([last_id_active_db, record_reminder_id, record_active_from])
