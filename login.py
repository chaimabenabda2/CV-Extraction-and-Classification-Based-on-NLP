from home import acceuil
import streamlit as st
import hashlib
import json

# Define the login page
def login():
    # Prompt the user for their username and password
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    # When the user submits their login information, validate their credentials
    if st.button('Login'):
        if check_credentials(username, password):
            # Store the user's credentials in a session variable
            session_id = username + password
            st.session_state['session_id'] = session_id

            # Redirect the user to the main application page
            st.experimental_rerun()
        else:
            # If the user is not authenticated, display an error message and prompt them to try again
            st.warning('Incorrect username or password. Please try again.')

            # Add a link to the signup page
            st.write('Don\'t have an account yet? [Sign up](signup)')

# Define the signup page
def signup():
    # Prompt the user for their desired username and password
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')

    # When the user submits their signup information, check if the username is already taken
    if st.button('Sign Up'):
        if check_username_available(new_username):
            # Hash the password and store the user's credentials in a database or a file
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            store_credentials(new_username, hashed_password)

            # Redirect the user to the login page
            st.experimental_rerun()
        else:
            # If the username is already taken, display an error message and prompt the user to try again
            st.warning('Username already taken. Please choose a different username.')

            # Add a link to the login page
            st.write('Already have an account? [Log in](login)')

# Define a function to check if the user's credentials are valid
def check_credentials(username, password):
    # Retrieve the stored hashed password for the username
    stored_password = retrieve_password(username)
    # Hash the entered password and compare it to the stored hashed password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return stored_password == hashed_password

# Define a function to check if a username is available
def check_username_available(username):
    # Check if the username is already in the database or file
    return username not in retrieve_all_usernames()

# Define a function to store the user's credentials
def store_credentials(username, hashed_password):
    # Load the existing credentials from the JSON file
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
    # Add the new username and hashed password to the credentials dictionary
    credentials[username] = hashed_password
    # Write the updated credentials dictionary to the JSON file
    with open('credentials.json', 'w') as f:
        json.dump(credentials, f)

# Define a function to retrieve the stored hashed password for a username
def retrieve_password(username):
    # Load the credentials from the JSON file
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    # Return the hashed password for the given username
    return credentials.get(username)

# Define a function to retrieve all usernames in the database or file
def retrieve_all_usernames():
    # Load the credentials from the JSON file
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    # Return a list of all the usernames in the credentials dictionary
    return list(credentials.keys())

# Define the main application page
# def app():
#     # Check if the user is authenticated before displaying the page content
#     if 'session_id' not in st.session_state:
#         login()
#     else:
#         st.write('Welcome to the main application page!')
#         acceuil()
#
# # Run the application
# if __name__ == '__main__':
#     app()


def app():
    # Use a radio widget to allow the user to switch between login and signup pages
    option = st.radio('Select an option', ('Login', 'Sign Up'))

    if option == 'Login':
        # If the user selects the login option, display the login page
        login()
        st.write('Don\'t have an account? [Sign up](signup)')
    else:
        # If the user selects the signup option, display the signup page
        signup()
        st.write('Already have an account? [Log in](login)')

    # Check if the user is authenticated before displaying the page content
    if 'session_id' in st.session_state:
        # If the user is authenticated, display the main application page
        acceuil()

# Run the app
app()

