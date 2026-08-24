import copy
import random
import json

"""
Note on why we used None instead of try-except for most functions:

Without None, you would have had to write custom exceptions
and multiple try-except blocks in every single banking function.
So we want to avoid Messy, deeply nested code.

Also using None allows the program to handle it gracefully.



"""
# -------------- Global Variables & File Persistence --------------

def save_users(users_list):
    """
    Save the list of users to users.json.
    json.dump serializes the Python list/dict structures into formatted JSON text.
    We use "with open(...)" and also explicitly call f.close().
    By setting indent=4, the JSON file is easy to read.
    
    """
    try:
        with open("users.json", "w") as f:
            json.dump(users_list, f, indent=4)
            f.close()
    except Exception as e:
        print(f"Error saving user data to JSON: {e}")


def load_users():
    """
    Load the list of users from users.json.
    If the file does not exist or fails to load, returns an empty list.
    Why do we return an empty list you say?
    Because if we didn't, the program would crash if the file didn't exist. Also you can't really have a bank with no users.

    """
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
            f.close()
            return data
    except:
        return []


# List to store all users - loaded from JSON file
users = load_users()

# Dictionary to store exchange rates
EXCHANGE_RATES = {
    "EGP": 1.0,
    "USD": 47.39,
    "SAR": 12.64
}

# Set to keep track of users who have failed to login (initialized from loaded data)
failed_login_users = set()
for u in users:
    if u.get("failed_login", False):
        failed_login_users.add(u["ID"])

# 4x4 matrix to represent ATM availability
atm_matrix = []

# Initialize ATM Matrix with random values (0 or 1)
for i in range(4):
    row = []
    for j in range(4):
        row.append(random.randint(0, 1))
    atm_matrix.append(row)

# -------------- Functions --------------

def home_menu(): # used in the main function
    """
    Display the home menu for the SIC Smart Bank System.
    This function presents the initial options to the user: login, register, or exit.
    """
    print("****************** SIC SMART BANK SYSTEM ******************")
    print("If you already have an account, enter login")
    print("If you do not have an account, enter register")
    print("To close the system, enter exit")


def get_safe_int(): # used in many functions so the program dosent crash if the user enters a non-integer value
    """
    Safely get an integer input from the user.
    This function prompts the user to enter an ID, validates that the input is a digit,
    and returns the integer value if valid. Returns None if the input is not a digit.
    What None does is that it tells the program to exit the current function and return back to the menu function.
    """
    user_input = input("Please enter your ID: ").strip()
    if user_input.isdigit():
        return int(user_input)
    return None


def parse_amount_and_currency(): # parse_amount_and_currency is used in multiple functions to parse the amount and currency input from the user.
    """
    Parse means to break down something into smaller parts, in this case we break down the input into smaller parts 
    The function below parses the amount and currency input from the user.
    This function prompts the user to enter an amount and currency ("20 USD"),
    validates the format, currency, and amount value, and returns a tuple of
    (amount, currency, amount_in_egp). Returns None if the input is invalid.
    """
    user_input = input("Enter amount and currency, example: 20 USD\n> ").strip()
    parts = user_input.split()

    if len(parts) != 2: # checks if the user entered two values, one for amount and one for currency
        print("Invalid format. Please enter amount followed by currency (e.g., 20 USD).\n")
        return None

    amount_str, currency = parts[0], parts[1].upper() # puts the amount in a variable called amount_str and the currency in a variable called currency.

    if currency not in EXCHANGE_RATES: # checks if the currency is in the dictionary of EXCHANGE_RATES.
        print(f"Unsupported currency '{currency}'. Accepted currencies are: EGP, USD, SAR.\n")
        return None

    try:
        amount = float(amount_str) # converts the amount_str to a float
        if amount <= 0: # checks if the amount is greater than 0
            print("Amount must be a positive number greater than 0.\n")
            return None
    except ValueError: # if the amount is not a number, it will print an error message and return None
        print("Invalid amount entered. Please enter a valid positive number.\n")
        return None

    amount_in_egp = amount * EXCHANGE_RATES[currency] # converts the amount to EGP by multiplying it by the exchange rate
    return amount, currency, amount_in_egp # returns the amount, currency, and amount in EGP


def register_user(users_list): # used in the main function to register a new user. it takes users_list as an argument and returns a new user if successful.
    """
    This function is used to register a new user. 
    It prompts the user to enter their name, password, phone number, email, gender, age, city, and account type.
    It then checks if the phone number or email already exists.
    If the phone number or email does not exist, it creates a new user and adds it to the users list.
    If the phone number or email already exists, it prints an error message and returns None.
    """
    print("  --- User Registration ---")
    
    name = input("Please enter your name: ").strip()
    password = input("Please enter your password: ").strip()
    phone = input("Please enter your phone number: ").strip()
    email = input("Please enter your email: ").strip()
    gender = input("Please enter your gender: ").strip()
    age = input("Please enter your age: ").strip()
    city = input("Please enter your city: ").strip()
    account_type = input("Please enter your account type (Standard / VIP / Admin): ").strip()

    for user in users_list:
        if user["profile"]["phone"] == phone or user["profile"]["email"] == email: # checks if the phone or email already exists
            print("\n This phone or email already exists. Please enter another one. \n")
            return

    if len(users_list) == 0: # checks if the users list is empty, if it is, it will set the new_id to 1
        new_id = 1
    else:
        new_id = len(users_list) + 1 # otherwise, it will set the new_id to the length of the users list plus 1
        
    is_vip = account_type.lower() == "vip" # checks if the account type is vip
    is_admin = account_type.lower() == "admin" or new_id == 1 # checks if the account type is admin or if the new_id is 1

    # We've also made the account type to become admin by default if the new_id is 1

    """
    MUST READ !!!!

    How dict.fromkeys work: It is used to create a dictionary with keys from an iterable and values set to a specified value. 
    Example: dict.fromkeys(["a", "b", "c"], 1) will create a dictionary {"a": 1, "b": 1, "c": 1}
    In our case, we are creating a dictionary with keys "sms_alerts", "email_notifications", and "paperless_statements" and values set to True.

    """ 
    new_user = {
        "ID": new_id,
        "profile": {
            "name": name,
            "password": password,
            "phone": phone,
            "email": email,
            "gender": gender,
            "age": age,
            "city": city,
            "account_type": account_type
        },
        "wallet": {
            "balance": 0.0,
            "currency": "EGP"
        },
        # Using dict.fromkeys to initialize default account notification settings
        "settings": dict.fromkeys(["sms_alerts", "email_notifications", "paperless_statements"], True),
        "active": True, # checks if the account is active
        "vip": is_vip, # checks if the account is vip
        "admin": is_admin, # checks if the account is admin
        "failed_login": False, # checks if the account has failed login attempts
        "transactions": [] # list to store transactions
    }

    users_list.append(new_user) # adding the new user to the users list
    save_users(users_list) # automatically persists new user data to JSON file
    print(f"\nSign up successful. Your ID is {new_id}\n") # printing the new user's ID


def login_user(users_list, failed_login_set): # used in the main function to login a user.
    """
    This function logs a user in.  
    It prompts the user to enter their ID and password. 
    If the ID and password are correct, it will log the user in. 
    If the ID or password are incorrect, it will print an error message and return None.
    and also if the login fails three times, it will add the user to the failed_login_set.
    
    """
    print("\n  --- User Login ---")
    max_attempts = 3

    for attempt in range(1, max_attempts + 1): # loop for the number of attempts
        user_id = get_safe_int() # gets the user's ID
        password = input("Please enter your password: ").strip() # gets the user's password

        if user_id is not None: # checks if the user's ID is valid
            for user in users_list: # loops through the users list to find the user with the matching ID
                if user["ID"] == user_id: # checks if the user's ID matches the ID entered by the user
                    if user["profile"]["password"] == password: # checks if the user's password matches the password entered by the user
                        print(f"\n Login successful. Welcome back, {user['profile']['name']}!\n") # prints a success message with the user's name
                        return user
                    else:
                        user["failed_login"] = True # sets the failed_login attribute to True
                        failed_login_set.add(user_id) # adds the user's ID to the failed_login_set
                        save_users(users_list) # persist failed login status to JSON

        remaining_attempts = max_attempts - attempt # calculates the remaining attempts
        if remaining_attempts > 0: # checks if there are remaining attempts
            print(f"Please check your ID/password and try again. ({remaining_attempts} attempt(s) left)\n")
        else:
            print("\n Maximum login attempts reached. Returning to main menu. \n")

    return None


def deposit_money(current_user, all_users=None): # used after logging in and entering ID and password correctly.
    """
    This function is used to deposit money into the user's account.
    It prompts the user to enter the amount and currency of the money to be deposited.
    It then adds the amount to the user's balance and prints a success message.
    """
    print("\n  --- Deposit ---")
    parsed = parse_amount_and_currency() # parses the amount and currency using the parse_amount_and_currency function
    if parsed is None: # checks if the amount and currency are valid
        return

    amount, currency, amount_in_egp = parsed # unpacks the parsed amount and currency
    current_user["wallet"]["balance"] += amount_in_egp # adds the amount to the user's balance

    record = f"Deposit: +{amount:g} {currency} ({amount_in_egp:.2f} EGP)" # creates a record of the transaction
    current_user["transactions"].append(record) # appends the record to the transactions list
    save_users(all_users if all_users is not None else users) # persist updated balance and history to JSON

    print(f"\n Deposit successful! Added {amount:g} {currency} ({amount_in_egp:.2f} EGP). \n") # prints a success message
    print(f"Current Balance: {current_user['wallet']['balance']:.2f} EGP\n") # prints the current balance


def withdraw_money(current_user, all_users=None): # used after logging in and entering ID and password correctly.
    """
    This function is used to withdraw money from the user's account.
    It prompts the user to enter the amount and currency of the money to be withdrawn.
    It then subtracts the amount from the user's balance and prints a success message.
    Any returns in this function are used to exit the function if the amount and currency are invalid or if the user's balance is insufficient.
    """
    print("\n  --- Withdraw ---")
    parsed = parse_amount_and_currency() # parses the amount and currency using the parse_amount_and_currency function
    if parsed is None: # checks if the amount and currency are valid
        return

    amount, currency, amount_in_egp = parsed # unpacks the parsed amount and currency
    if current_user["wallet"]["balance"] < amount_in_egp: # checks if the user's balance is sufficient for the withdrawal
        print(f"\n Insufficient balance. Available: {current_user['wallet']['balance']:.2f} EGP, Requested: {amount_in_egp:.2f} EGP ({amount:g} {currency}).\n")
        return

    current_user["wallet"]["balance"] -= amount_in_egp # subtracts the amount from the user's balance
    record = f"Withdrawal: -{amount:g} {currency} ({amount_in_egp:.2f} EGP)" # creates a record of the transaction
    current_user["transactions"].append(record) # appends the record to the transactions list
    save_users(all_users if all_users is not None else users) # persist updated balance and history to JSON

    print(f"\nWithdrawal successful! Deducted {amount:g} {currency} ({amount_in_egp:.2f} EGP).") # prints a success message
    print(f"Current Balance: {current_user['wallet']['balance']:.2f} EGP\n") # prints the current balance


def transfer_money(current_user, all_users): # used after logging in and entering ID and password correctly.
    """
    This function is used to transfer money from the user's account to another user's account.
    It prompts the user to enter the receiver's ID, the amount, and the currency of the money to be transferred.
    It then subtracts the amount from the user's balance and adds it to the receiver's balance and prints a success message.
    Any returns in this function are used to exit the function if the amount and currency are invalid or if the user's balance is insufficient.
    """
    print("\n  --- Transfer ---")
    receiver_input = input("Please enter receiver ID: ").strip()
    if not receiver_input.isdigit(): # checks if the receiver's ID is a digit
        print("\n Invalid ID entered.\n") # prints an error message if the receiver's ID is not a digit
        return

    receiver_id = int(receiver_input) # converts the receiver's ID to an integer

    if receiver_id == current_user["ID"]: # checks if the receiver's ID is the same as the current user's ID
        print("\n You cannot transfer money to your own account.\n") # prints an error message if the receiver's ID is the same as the current user's ID
        return

    receiver_user = None # sets the receiver user to None
    for user in all_users: # loops through the users list to find the user with the matching ID
        if user["ID"] == receiver_id: # checks if the user's ID matches the ID entered by the user
            receiver_user = user
            break # exits the loop if the user with the matching ID is found

    if receiver_user is None: # checks if the receiver user is None by using the is keyword for NoneType objects
        print(f"Receiver with ID {receiver_id} was not found.\n") # prints an error message if the receiver user is not found
        return

    parsed = parse_amount_and_currency() # parses the amount and currency using the parse_amount_and_currency function
    if parsed is None: # checks if the amount and currency are valid
        return

    amount, currency, amount_in_egp = parsed # unpacks the parsed amount and currency
    if current_user["wallet"]["balance"] < amount_in_egp: # checks if the user's balance is sufficient for the withdrawal
        print(f"\n Insufficient balance. Available: {current_user['wallet']['balance']:.2f} EGP, Requested: {amount_in_egp:.2f} EGP. \n")
        return

    current_user["wallet"]["balance"] -= amount_in_egp # subtracts the amount from the user's balance
    receiver_user["wallet"]["balance"] += amount_in_egp # adds the amount to the receiver's balance

    sender_record = f"Transfer Sent: -{amount:g} {currency} ({amount_in_egp:.2f} EGP) to {receiver_user['profile']['name']} (ID: {receiver_id})" # creates a record of the transaction
    receiver_record = f"Transfer Received: +{amount_in_egp:.2f} EGP from {current_user['profile']['name']} (ID: {current_user['ID']})" # creates a record of the transaction

    current_user["transactions"].append(sender_record) # appends the record to the transactions list
    receiver_user["transactions"].append(receiver_record) # appends the record to the transactions list
    save_users(all_users) # persist transfers to JSON file

    print(f"\n Transfer successful! Sent {amount:g} {currency} ({amount_in_egp:.2f} EGP) to {receiver_user['profile']['name']} (ID: {receiver_id}). \n") # prints a success message
    print(f"Current Balance: {current_user['wallet']['balance']:.2f} EGP\n") # prints the current balance


def view_transaction_history(current_user): # used after logging in and entering ID and password correctly.
    """
    This function is used to view the transaction history of the user.
    It prompts the user to enter the receiver's ID, the amount, and the currency of the money to be transferred.
    It then subtracts the amount from the user's balance and adds it to the receiver's balance and prints a success message.
    Any returns in this function are used to exit the function if the amount and currency are invalid or if the user's balance is insufficient.
    """
    history = current_user["transactions"] # gets the user's transactions

    print(f"\n  ****************** TRANSACTION HISTORY ****************** \n") 
    print(f"Account Holder: {current_user['profile']['name']} (ID: {current_user['ID']})") # prints the account holder's name and ID
    print(f"Current Balance: {current_user['wallet']['balance']:.2f} EGP") # prints the current balance
    print(f"Total Transactions: {len(history)}") # prints the total number of transactions
    print("**********************************************************\n") 

    if len(history) == 0: # checks if the user has any transactions
        print("No transactions recorded yet.\n") # prints an error message if the user has no transactions
        return

    while True: # loops through the transaction history
        print("\nChoose an option to view history:") # prints the options
        print("[0] View All Operations") 
        print("[1] View First Operation (Using index [0])")
        print("[2] View Last Operation (Using index [-1])")
        print("[3] View Last 5 Operations (Using slice [-5:])")
        print("[4] Back to User Menu")

        sub_choice = input("> ").strip()

        if sub_choice == "0": # checks if the user wants to view all transactions
            print("\n* All Transactions *")
            for i in range(len(history)): # loops through the transaction history
                print(f"{i + 1}. {history[i]}") # prints the transaction history by accessing the index i in the history list

        elif sub_choice == "1": # checks if the user wants to view the first transaction
            print("\n* First Operation *")
            print(f"First: {history[0]}") # prints the first transaction by accessing the index 0 in the history list

        elif sub_choice == "2": # checks if the user wants to view the last transaction
            print("\n* Last Operation *")
            print(f"Last: {history[-1]}") # prints the last transaction by accessing the index -1 in the history list

        elif sub_choice == "3": # checks if the user wants to view the last 5 transactions
            print("\n* Last 5 Operations *")
            last_5 = history[-5:]
            for i in range(len(last_5)): # loops through the last 5 transactions
                print(f"{i + 1}. {last_5[i]}")

        elif sub_choice == "4": # checks if the user wants to go back to the user menu
            print("\n* Back to User Menu *") # prints a message indicating that the user is going back to the user menu
            break # exits the loop

        else: # checks if the user entered an invalid choice
            print("Invalid choice. Please enter a number from [0] to [4].") # prints an error message if the user entered an invalid choice


def admin_reports(all_users, failed_login_set, current_user): 
    """
    admin_reports takes in all_users, failed_login_set, and current_user as parameters for example all_users = [{"ID":"001", "profile":{"name":"John", "email":"[EMAIL_ADDRESS]", "phone":"1234567890"}, "admin":True}, {...}, {...}]
    failed_login_set = {"001", "002", "003"}
    current_user = {"ID":"001", "profile":{"name":"John", "email":"[EMAIL_ADDRESS]", "phone":"1234567890"}, "admin":True}

    The function itself is used to view reports that can only be seen by admins, such as transaction frequency report, 
    user segment report, VIP vs active users analysis, list all user IDs and account names,
    and duplicate phone/email check. 
    """
    if current_user["admin"] != True: # checks if the current user is an admin
        print("\nAccess denied: Admin privileges required to view reports.\n") # prints an error message if the current user is not an admin
        return

    print("\n**************** Admin Reports ****************")
    if len(all_users) == 0: # checks if there are any users in the system
        print("No registered users in the system yet.\n") # prints an error message if there are no users in the system
        return # exits the function

    while True: # loops through the reports
        print("\nChoose a report:")
        print("[0] Duplicate phone/email check")
        print("[1] Transaction frequency report")
        print("[2] User segment report")
        print("[3] VIP vs active users analysis")
        print("[4] List all user IDs and account names")
        print("[5] Back to User Menu")

        choice = input("> ").strip()

        active_users = set() # set for active users  
        vip_users = set() # set for vip users
        failed_login_users = set(failed_login_set) # set for failed login users
        transfer_users = set() # set for transfer users

        for u in all_users: # loops through all users
            u_id = u["ID"] # gets the user ID
            if u.get("active", True): # checks if the user is active
                active_users.add(u_id) # adds the user ID to the set of active users
            if u.get("vip", False) or u["profile"].get("account_type", "").lower() == "vip": # checks if the user is a vip
                vip_users.add(u_id) # adds the user ID to the set of vip users
            if u.get("failed_login", False): # checks if the user has failed logins
                failed_login_users.add(u_id) # adds the user ID to the set of failed login users
            for t in u["transactions"]: # loops through the transactions
                if "Transfer" in t or "transfer" in t.lower(): # checks if the transaction is a transfer
                    transfer_users.add(u_id) # adds the user ID to the set of transfer users
                    break 

        if choice == "0":  # checks if the user wants to check for duplicate phone/email
            phones = []
            emails = []
            for u in all_users: # loops through all users
                phones.append(u["profile"]["phone"]) # appends the phone number to the list of phone numbers
                emails.append(u["profile"]["email"]) # appends the email to the list of emails

            found_dup_phone = False
            for p in phones: # loops through the phone numbers
                if phones.count(p) > 1:
                    print("Duplicate phone number detected:", p)
                    found_dup_phone = True
                    break
            if not found_dup_phone:  # checks if there are no duplicate phone numbers
                print("No duplicate phone numbers found.")

            found_dup_email = False
            for e in emails: # loops through the emails
                if emails.count(e) > 1: # checks if the email is a duplicate
                    print("Duplicate email detected:", e)
                    found_dup_email = True
                    break
            if not found_dup_email: # checks if there are no duplicate emails
                print("No duplicate emails found.")

        elif choice == "1": # checks if the user wants to view the transaction frequency report
            # Using dict.fromkeys to initialize transaction category counters
            category_counts = dict.fromkeys(["deposit", "withdraw", "transfer"], 0) # creates a dictionary to store the transaction counts

            for u in all_users: # loops through all users
                for t in u["transactions"]: # loops through the transactions
                    t_lower = t.lower() # converts the transaction to lowercase
                    if "deposit" in t_lower: # checks if the transaction is a deposit
                        category_counts["deposit"] += 1 # increments the deposit count
                    elif "withdraw" in t_lower: # checks if the transaction is a withdraw
                        category_counts["withdraw"] += 1
                    elif "transfer" in t_lower: # checks if the transaction is a transfer
                        category_counts["transfer"] += 1

            print("\nTransaction Frequency Report:") # prints the transaction frequency report
            print("Deposits:", category_counts["deposit"]) # prints the deposit count
            print("Withdraws:", category_counts["withdraw"]) # prints the withdraw count
            print("Transfers:", category_counts["transfer"]) # prints the transfer count

        elif choice == "2": 
            target_input = input("Enter User ID: ").strip()
            if not target_input.isdigit(): # checks if the user ID is a digit
                print("Invalid User ID entered.\n")
                continue # skips the rest of the code and goes back to the beginning of the loop

            target_id = int(target_input)
            target_user = None # initialize the target user to None
            for u in all_users: # loops through all users
                if u["ID"] == target_id: # checks if the user ID is equal to the target ID
                    target_user = u
                    break

            if target_user is None: # checks if the user ID is not found
                print(f"User with ID {target_id} not found.\n")
            else:
                u_deposits = 0
                u_withdraws = 0
                u_transfers = 0

                for t in target_user["transactions"]: # loops through the transactions
                    t_lower = t.lower() # converts the transaction to lowercase
                    if "deposit" in t_lower: # checks if the transaction is a deposit
                        u_deposits += 1
                    elif "withdraw" in t_lower: # checks if the transaction is a withdraw
                        u_withdraws += 1
                    elif "transfer" in t_lower: # checks if the transaction is a transfer
                        u_transfers += 1

                print(f"User has deposited {u_deposits} times.") # prints the deposit count
                print(f"User has withdrawn {u_withdraws} times.") # prints the withdraw count
                print(f"User has transferred {u_transfers} times.") # prints the transfer count

                print("\nCheck Segment:") # prints the segment choices
                print("[1] VIP")
                print("[2] Active")
                print("[3] Failed login")
                print("[4] Has transfers")

                seg_choice = input("Enter segment choice: ").strip() # takes the segment choice from the user
                if seg_choice == "1": # checks if the user wants to view the VIP segment
                    print("User is a VIP." if target_id in vip_users else "User is not a VIP.")
                elif seg_choice == "2": # checks if the user wants to view the Active segment
                    print("User is Active." if target_id in active_users else "User is not Active.")
                elif seg_choice == "3": # checks if the user wants to view the Failed login segment
                    print("User is a failed login." if target_id in failed_login_users else "User is not a failed login.")
                elif seg_choice == "4": # checks if the user wants to view the Transfer segment
                    print("User has transfers." if target_id in transfer_users else "User has no transfers.")
                else: # checks if the segment choice is invalid
                    print("Invalid segment choice.")

        elif choice == "3":
            print("\nVIP vs Active Users Analysis:")
            print("Active users:", active_users)
            print("VIP users:", vip_users)
            print("Active VIP users (Active AND VIP):", active_users & vip_users)
            print("Active but not VIP:", active_users - vip_users)
            print("Active OR VIP:", active_users | vip_users)
            print("Only one of Active/VIP:", active_users ^ vip_users)

        elif choice == "4": # CUSTOM OPTION - View all registered users
            print("\nAll Registered Users:")
            for u in all_users:
                print(f"ID: {u['ID']} | Name: {u['profile'].get('name', 'N/A')} | Email: {u['profile'].get('email', 'N/A')}")

        elif choice == "5": # Return to User Menu
            print("\nReturning to User Menu...")
            break
        else:
            print("Invalid choice. Please select [0] to [5].")


def branch_atm_status(atm_matrix, current_user=None):  # branch_atm_status function takes two parameters atm_matrix and current_user, the current_user = none is the default value so it can be called without a current user
    """
    As for branch_atm_status function, it prints the ATM availability status.
    
    Parameters:
    - atm_matrix: A 2D list representing ATM matrix with 1s as available and 0s as unavailable.
    - current_user: The current user (optional).
    """
    print("\n**************** ATM Availability ****************\n")
    if not atm_matrix:
        print("No ATM data available.\n")
        return

    # Handle jagged lists by finding the maximum column length
    max_cols = 0
    for row in atm_matrix: # iterates through the rows of the ATM matrix
        if len(row) > max_cols: # checks if the current row has more columns than the maximum column length
            max_cols = len(row) 

    col_headers = ""
    for c in range(max_cols):
        col_headers += f"C{c}  " # appends the column headers
    print(" " * 10 + col_headers) # prints the column headers with spaces in between each column header: C0 C1 C2 C3

    available_atms = 0
    unavailable_atms = 0
    rowcount = 0

    for row in atm_matrix: # iterates through the rows of the ATM matrix
        print(f"Row {rowcount}" + " " * 5, end=" ") # prints the row headers with spaces in between each row header
        rowcount += 1
        for col in row: # iterates through the columns of the ATM matrix
            if col == 1: # checks if the current column is available
                available_atms += 1
            else: # checks if the current column is unavailable
                unavailable_atms += 1
            print(f"{col:<4}", end="") # prints the column with 4 spaces after each column
        print() 

    print(f"\nAvailable ATMs: {available_atms}")
    print(f"Out of service: {unavailable_atms}\n")

    if current_user["admin"] == True:
        decision = input("Update ATM? (y/n): ").strip().lower()
        while decision not in ["y", "n"]:
            decision = input("Please only enter y (Yes) or n (No): ").strip().lower()

        if decision == "y": # checks if the user wants to update an ATM
            row_num = int(input("Enter row number: ")) # gets the row number
            col_num = int(input("Enter column number: ")) # gets the column number
            new_status = int(input("Enter status (0 for Out of service, 1 for Available): ")) # gets the new status

            atm_matrix[row_num][col_num] = new_status # updates the ATM status in the matrix
            print("\nStatus successfully updated!") 
        else:
            print("Update cancelled.") 


def update_personal_info(current_user, all_users):
    """
    This function updates the personal information of the current user.
    It first creates a deepcopy of the current user's information to prevent
    unintended changes.
    Then it enters a loop to allow the user to update their information.
    """
    # copy.deepcopy creates an independent, fully isolated clone of the nested user dictionary (profile, wallet, settings).
    # This ensures modifications can be safely made, and previous field values can be retrieved/restored from snapshot.
    snapshot = copy.deepcopy(current_user)

    while True:
        print("\n***** Update Personal Information *****")
        print("[0] Change city")
        print("[1] Change phone number")
        print("[2] Change password")
        print("[3] Change email")
        print("[4] Add emergency contact") # CUSTOM OPTION - adds optional field
        print("[5] Remove optional field") # CUSTOM OPTION - removes optional field
        print("[6] Retrieve optional field from snapshot") # CUSTOM OPTION - retrieves lost field value
        print("[7] View profile details (keys, values, items)") # CUSTOM OPTION - views profile details
        print("[8] Back to User Menu")

        choice = input("> ").strip()

        if choice == "0":
            new_city = input("Enter the name of the new city: ").strip()
            current_user["profile"].update({"city": new_city}) # updates the city in the profile
            save_users(all_users)
            print("New city updated successfully.")

        elif choice == "1":
            new_phone = input("Enter the new phone number: ").strip()
            current_user["profile"].update({"phone": new_phone}) # updates the phone number in the profile
            save_users(all_users)
            print("New phone number updated successfully.")

        elif choice == "2":
            new_password = input("Enter the new password: ").strip()
            current_user["profile"].update({"password": new_password}) # updates the password in the profile
            save_users(all_users)
            print("New password updated successfully.")

        elif choice == "3":
            new_email = input("Enter the new email: ").strip()
            current_user["profile"].update({"email": new_email}) # updates the email in the profile
            save_users(all_users)
            print("New email updated successfully.")

        elif choice == "4":
            key = input("Enter field name (e.g. emergency_contact): ").strip()
            value = input("Enter field value: ").strip()
            current_user["profile"].update({key: value}) # updates the profile with the new field and value
            save_users(all_users)
            print(f"'{key}' added successfully.")

        elif choice == "5":
            data_choice = input("What optional field do you want to remove? ").strip()
            if data_choice in ["name", "password", "phone", "email"]: # checks if the data choice is a mandatory core field
                print(f"Cannot remove mandatory core field '{data_choice}'.")
            elif data_choice in current_user["profile"]: # checks if the data choice is in the profile
                current_user["profile"].pop(data_choice, None) # removes the data choice from the profile, none here prevents an error if the data choice is not found
                save_users(all_users)
                print(f"'{data_choice}' removed successfully.")
            else:
                print(f"Field '{data_choice}' not found in profile.")

        elif choice == "6":
            data_choice = input("What field do you want to retrieve from snapshot? ").strip()
            value = snapshot["profile"].get(data_choice) # gets the value from the snapshot
            if value is not None: # checks if the value is not None meaning the field exists in the snapshot
                current_user["profile"].update({data_choice: value}) # updates the profile with the value from the snapshot
                save_users(all_users)
                print(f"'{data_choice}' restored successfully from snapshot: {value}")
            else:
                print(f"No saved value found for '{data_choice}' in the snapshot.")

        elif choice == "7":
            print("\n--- Profile Keys ---")
            for k in current_user["profile"].keys(): # iterates through the keys of the profile
                print(k, end=" | ") # prints the keys with spaces in between each key
            print("\n\n--- Profile Values ---")
            for v in current_user["profile"].values(): # iterates through the values of the profile
                print(v, end=" | ") # prints the values with spaces in between each value
            print("\n\n--- Profile Items ---") # prints the profile items
            for k, v in current_user["profile"].items(): # iterates through the items of the profile
                print(f"{k}: {v}") # prints the items in the format of key: value
            print()

        elif choice == "8":
            print("\nReturning to user menu...") 
            break

        else:
            print("Invalid choice. Please select an option from [0] to [8].")


def display_user_menu(user):
    """
    Last but not least, the display_user_menu function. 
    This function is used to display the menu of the user.
    It takes the user as an argument and prints the menu.
    
    """
    print(f"****************** Welcome back {user['profile']['name']} ******************")
    print("[0] Deposit")
    print("[1] Withdraw")
    print("[2] Transfer")
    print("[3] Transaction history")
    print("[4] Reports")
    print("[5] Branch/ATM status")
    print("[6] Update personal info")
    print("[7] Exit")


def user_dashboard(current_user, all_users, atm_matrix, failed_login_set):
    """
    And as the cherry on top, we have the user_dashboard function. 
    This function is used to display the menu of the user.
    It takes the user as an argument and prints the menu.
    It binds all the user functions together in one place.
    It basically acts as a controller for the user side of the application.
    """
    while True:
        display_user_menu(current_user)
        choice = input("> ").strip()

        if choice == "0":
            deposit_money(current_user, all_users)

        elif choice == "1":
            withdraw_money(current_user, all_users)

        elif choice == "2":
            transfer_money(current_user, all_users)

        elif choice == "3":
            view_transaction_history(current_user)

        elif choice == "4":
            admin_reports(all_users, failed_login_set, current_user)

        elif choice == "5":
            branch_atm_status(atm_matrix, current_user)

        elif choice == "6":
            update_personal_info(current_user, all_users)

        elif choice == "7":
            print(f"\nLogging out {current_user['profile']['name']}. Returning to home menu.\n")
            break

        else:
            print("\nInvalid choice. Please select an option from [0] to [7].\n")


# Main part of the program

while True:
    home_menu()
    
    choice = input("> ").strip().lower()

    if choice == "register":
        register_user(users)

    elif choice == "login":
        logged_in_user = login_user(users, failed_login_users) 
        
        if logged_in_user:
            user_dashboard(logged_in_user, users, atm_matrix, failed_login_users)

    elif choice == "exit":
        save_users(users) # ensure all data is saved on exit
        print("\nThank you for using SIC Smart Bank System. Goodbye and be sure to use our SIC Bank services more often!")
        break

    else:
        print("Invalid choice. Please enter 'login', 'register' or 'exit'.")
