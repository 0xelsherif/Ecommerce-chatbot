# src/session_management.py

def is_user_logged_in(session):
    return 'user_id' in session

def get_user_info(session):
    if not is_user_logged_in(session):
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        session['first_name'] = first_name
        session['last_name'] = last_name
        
    else:
        print(f"Welcome back, {session['first_name']} {session['last_name']}!")
