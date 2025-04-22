"""
this program helps the user to manage a reminder, it loads reminders from a csv file, displays active reminders, and allows the user to interact with them

the features this reminder has are:
- viewing active reminders
- adding reminders (now or later)
- viewing past or future reminders
- closing reminders
- exiting the program

each reminder has:
- identifier
- reminder text
- start time (when active)
- close time (set to 01-01-1970 10:00:00 if not closed)


april 7, 2025, 10:00 represents the current date and time for the program


commands:
- 'future reminders': shows upcoming reminders
- 'previous reminders': shows past reminders
- 'close <X>': closes active reminders
- 'remind me now <TEXT>': adds current active reminders
- 'remind at '<TIME>' <TEXT>`: adds a reminder for later
- 'exit': exits the program
"""

import data
import datetime


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    """
    main program entry point
    perform the initial setup such as:
    - program start counter (for tracking or future use)
    - load reminders from 'test_data.csv' into the global database
    - store references to loaded reminders (for debugging)
    """
    # program state setup
    program_counter = 1
    # load the reminder data from csv into the global reminders database
    data.load_database('test_data.csv')

    # open the database (for debugging)
    db = data.reminders_database
    # define the set up time
    now = datetime.datetime(2025, 4, 7, 10)

    # input loop
    user_input = ""
    # display the current active reminders
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

            data.print_reminders(future_reminders)
        # show the past reminders (dismissed after being active)
        elif (user_input == "past reminders"):
            past_reminders = data.get_past_reminders()
            print("PAST REMINDERS")

            data.print_reminders_by_index(past_reminders,"-")
        # dismiss a reminder
        elif ("dismiss" in user_input):
            _,reminder_to_dismiss = user_input.split()
            
    
            all_active = data.get_active_reminders()
            
            # make sure the index matches an active reminder
            if (int(reminder_to_dismiss) > len(all_active)):
                print(f"{reminder_to_dismiss} is not a valid item from the menu.")
            else:
                reminder_id_to_dismiss = all_active[int(reminder_to_dismiss)-1][0]

                # only dismiss if the ID exists
                if (data.check_reminder_id_exist(reminder_id_to_dismiss)):
                    data.dismiss_reminder(reminder_id_to_dismiss)

                    # update and show active reminders after one is dismissed
                    print("ACTIVE REMINDERS")
                    active_reminders = data.get_active_reminders()
                    data.print_reminders_by_index(active_reminders)


        # add a new reminder either for now or a future time
        elif ("remind" in user_input):
            # add a reminder that will active immediately
            if ("now" in user_input):
                _, reminder_text = user_input.split(" now ") 

                data.set_reminder(reminder_text, now)
                print("ACTIVE REMINDERS")
                active_reminders = data.get_active_reminders()
                data.print_reminders_by_index(active_reminders)

            # future reminder
            elif ("at" in user_input):
                _, reminder_info = user_input.split(" at ") 
                reminder_datetime, reminder_text = reminder_info.split('\' ')
                reminder_datetime = reminder_datetime.strip()[1:]
                reminder_text = reminder_text.strip()
                data.set_reminder(reminder_text, data.convert_date_to_datetime(reminder_datetime))
                
                # update and show active reminders
                print("ACTIVE REMINDERS")
                active_reminders = data.get_active_reminders()
                data.print_reminders_by_index(active_reminders)

        # quit the program
        elif (user_input == "quit"):
            print("goodbye")
            break
        
        # show full database (for debug)
        elif (user_input == "db"):
            print(db)
        
        else:
            continue