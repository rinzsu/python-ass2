"""
this program helps the user to manage a reminder, it loads reminders from csv files, 
displays active reminders, and allows the user to interact with them

the features this reminder has are:
- viewing active reminders
- adding reminders (now or later)
- viewing past or future reminders
- closing (dismissing) reminders
- renewing old reminders for future activation
- saving the current database reminder to a file
- exiting the program

each reminder consists of:
- an unique identifier (reminder_id)
- a reminder text (e.g: "buy milk")
- an active time: stored in 'reminders_active_database'
- a dismissed time: stored in 'reminders_dismissed_database' if the reminder has been dismissed

reminders can appear multiple times in the active or dismissed databases, 
allowing recurring tasks to be scheduled without duplicating the reminder text

april 7, 2025, 10:00 represents the current date and time for the program

the reminders are organized into three logistic tables:
- 'reminders_database': stores the reminder text and unique ID
- 'reminders_active_database': stores the reminder ID and its activation time
- 'reminders_dismissed_database': stores the reminder ID and its dismissal time

a reminder is considered:
- 'active': if it has an entry in 'reminders_active_database' with an activation time ≤ now, 
  and no corresponding entry in 'reminders_dismissed_database' for the same reminder
- 'past': if it was dismissed (dismissed_at ≤ now)
- 'future': if its 'active_from' time is after now

commands:
- 'future reminders': shows upcoming reminders
- 'past reminders': shows past/dismissed reminders
- 'dismiss <X>': dismisses an active reminder (X is the number shown in the active list)
- 'remind now <TEXT>': adds a new reminder that becomes active immediately
- 'remind at '<TIME>' <TEXT>': adds a new reminder that becomes active at the given future time
- 'renew <X> at <TIME>': reactivates a previously added reminder to become active at a new time
- 'dump to <FILENAME>': saves the current state of all databases to a CSV file
- 'db': shows raw database content (for debugging)
- 'quit': exits the program

the system supports repeatable reminders and tracks all creation and dismissal events
"""

import data
import datetime

# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    """
    main program entry point
    load_database("test_data.csv", "test_active.csv", "test_dismissed.csv")
    loads reminder data from the given csv files into their respective databases:
    - test_data.csv: general reminder entries
    - test_active.csv: reminders currently active
    - test_dismissed.csv: dismissed (past) reminders
    """
    # program state setup
    program_counter = 1
    # load the reminder data from csv into the global reminders database
    data.load_database("test_data.csv", "test_active.csv", "test_dismissed.csv")

    # set up references for all types of reminders
    db = data.reminders_database
    db_active = data.reminders_active_database
    db_inactive = data.reminders_dismissed_database

    # simulate the current datetime for all logic
    now = datetime.datetime(2025, 4, 7, 10)

    # input loop
    user_input = ""

    # display current active reminders
    print("ACTIVE REMINDERS")
    active_reminders = data.get_active_reminders()
    data.print_reminders_by_index(active_reminders)

    while (user_input != "quit"):
        # get user command
        user_input = input("> ")

        # show future reminders (not active yet)
        if (user_input == "future reminders"):
            future_reminders = data.get_future_reminders()
            print("FUTURE REMINDERS")
            
            # show future reminders sorted by activation time
            sorted_data = sorted(future_reminders, key=lambda x: x[1])
            data.print_reminders(sorted_data)

        # show the past reminders (dismissed after being active)
        elif (user_input == "past reminders"):
            past_reminders = data.get_past_reminders()
            print("PAST REMINDERS")
            data.print_reminders_by_index(past_reminders, "-")

        # dismiss a reminder
        elif ("dismiss" in user_input):
            _, reminder_to_dismiss = user_input.split()
            all_active = data.get_active_reminders()

            # make sure the index matches an active reminder
            if (int(reminder_to_dismiss) > len(all_active)):
                print(f"{reminder_to_dismiss} is not a valid item from the menu.")
            else:
                reminder_id_to_dismiss = all_active[int(reminder_to_dismiss)-1][1]

                # only dismiss if the ID exists
                if (data.check_reminder_id_exist(reminder_id_to_dismiss)):
                    data.dismiss_reminder(reminder_id_to_dismiss)

                    # update and show active reminders after one dismiss
                    print("ACTIVE REMINDERS")
                    active_reminders = data.get_active_reminders()
                    data.print_reminders_by_index(active_reminders)

        # add a new reminder either for now or a future time
        elif ("remind" in user_input):
            # add a reminder that will active immediately
            if ("now" in user_input):
                _, reminder_text = user_input.split(" now ")
                data.set_reminder(reminder_text, now)
                
                # show active reminders after adding a new reminder
                print("ACTIVE REMINDERS")
                active_reminders = data.get_active_reminders()
                data.print_reminders_by_index(active_reminders)

            # future reminder
            elif ("at" in user_input):
                _, reminder_info = user_input.split(" at ")
                reminder_datetime, reminder_text = reminder_info.split("' ")
                reminder_datetime = reminder_datetime.strip()[1:]  # remove starting quote
                reminder_text = reminder_text.strip()

                data.set_reminder(reminder_text, data.convert_date_to_datetime(reminder_datetime))

                # update and show active reminders
                print("ACTIVE REMINDERS")
                active_reminders = data.get_active_reminders()
                data.print_reminders_by_index(active_reminders)

        # renew a previously dismissed reminder or scheduled one
        elif ("renew" in user_input):
            renew_id_text, renew_datetime = user_input.split(" at ")
            _, renew_id = renew_id_text.split()

            past_reminders = data.get_past_reminders()
            active_reminders = data.get_active_reminders()
            future_reminders = data.get_future_reminders()

            renewed_id = 0

            # invalid renew ID refers to past or future reminders
            if (int(renew_id) < 0):
                my_arr = (past_reminders, future_reminders)
                renew_id = str(int(renew_id) * -1)
                renewed_id = my_arr[int(renew_id) - len(active_reminders) - 1][0][1]

            # valid renew ID refers to currently active or future reminder
            else:
                my_arr = (active_reminders, future_reminders)
                if (int(renew_id) > len(my_arr)):
                    print(f"{renew_id} is not a valid item from the menu.")
                    continue
                renewed_id = my_arr[int(renew_id) - len(active_reminders)][0][1]

            # renew the reminder by updating its start time
            if (renewed_id != 0):
                data.renew_reminder(renewed_id, data.convert_date_to_datetime(renew_datetime))
            else:
                data.renew_reminder(renew_id, data.convert_date_to_datetime(renew_datetime))

            print("ACTIVE REMINDERS")
            active_reminders = data.get_active_reminders()
            data.print_reminders_by_index(active_reminders)

        # quit the program
        elif (user_input == "quit"):
            print("goodbye")
            break

        # show full database (for debug)
        elif (user_input == "db"):
            print("DB       : ", db)
            print("ACTIVE   : ", db_active)
            print("INACTIVE : ", db_inactive)

        else:
            continue
