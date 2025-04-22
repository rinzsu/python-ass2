import csv
import datetime

# set a datetime to simulate the current date and time
now = datetime.datetime(2025, 4, 7, 10)

# lists of all reminder records from the csv file
reminders_database = [] # -> store all db
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
load_database(reminder_file)

loads reminder data from a csv file into the global reminder database
each line in the csv file must contain [ID, reminder text, active_from, disassemble_at]

args:
- reminder_file(str): path to the csv file
"""
def load_database(reminders_file): # input path to load into our reminders db var
    f = open(reminders_file,"r")
    reader = csv.reader(f,delimiter=",")
    # read rows from the csv and add to the reminders database
    for _, row in enumerate(reader):
      reminders_database.append(row)
    
"""
get_active_reminders()
returns a list of active reminders, that is, reminders that have been started but not yet closed

returns:
- list: list of active reminders
"""
def get_active_reminders():
    active_reminders = []
    # loop through reminders and check if the reminder still active
    for row in reminders_database[1:]:
        _, _, active_from, dismissed_at = row
        if (check_compare_date(dismissed_at,"<",active_from) and check_date_passed(active_from)):
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
    for row in reminders_database[1:]:
        _, _, active_from, dismissed_at = row
        # reminder is past if active_from <= dismissed_at, and both dates have passed
        if (
            check_compare_date(active_from,"<=",dismissed_at) and 
            check_date_passed(active_from) and 
            check_date_passed(dismissed_at)
            ):

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
    # future reminders are those that haven't reached the time yet
    index_start = len(get_active_reminders())
    for i in range(1, len(reminders_database)):
        row = reminders_database[i][:]

        row[0] = index_start

        if (
            check_date_passed(row[2]) == False
            ):
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

    reminders_database.append([record_reminder_id, record_reminder_text, record_active_from, record_dismissed_at])

"""
dismiss_reminder(reminder_id)
marks a reminder as completed based on its ID and updates the completion time

args:
- reminder_id (str): the ID of the reminder to dismiss
"""
def dismiss_reminder(reminder_id):
    db = reminders_database
    for i in range (len(db)):
        record_reminder_id, _,_,_ = db[i]
        if (record_reminder_id == reminder_id):
            if (reminders_database[i] not in get_past_reminders()):
                reminders_database[i][3] = str(now)
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
        print(f"{mode}{index}. {reminder[1]}")
        index += 1

"""
print_reminders_by_index(db, mode="")
prints reminders from the given base data with an index and an optional prefix

args:
- db (list): list of reminders to display
- mode (str): prefix of choice for text reminders (default is "")
"""
def print_reminders(db, mode=""):
    index = 1
    for reminder in db[:]:
        print(f"{mode}{int(reminder[0])+ 1}. {reminder[1]}")
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
    for record in reminders_database[1:]:
        if (record[0] == reminder_id): 
            return True
    return False

# load_database("test_data.csv")

# for row in reminders_database[1:]:
#     print(
#         convert_date_to_datetime(row[2]),
#         convert_date_to_datetime(row[3]), 
#         "|", now, " = ", 
#         check_date_passed(row[2]),  
#         check_date_passed(row[3]), 
#         check_compare_date(row[2],">",row[3]))

# set_reminder("BOI",123)
# dismiss_reminder("1")
# dismiss_reminder("0")

# set_reminder("MAKAN", '2025-04-07 11:00:00')

# print(get_active_reminders())


# print(reminders_database)
# dismiss_reminder("1")
# dismiss_reminder("2")

# print(reminders_database)