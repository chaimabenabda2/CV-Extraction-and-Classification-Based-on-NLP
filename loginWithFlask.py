# from flask import Flask, redirect, url_for, request
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
# import streamlit as st
# from home import acceuil
#
# app = Flask(__name__)
# app.secret_key = 'testpassword123'
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# class User(UserMixin):
#     pass
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     # Implement this function to load a user from a user ID
#     return User.get(user_id)
#
#
# @app.route('/')
# def index():
#     return redirect(url_for('login'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Implement your login logic here
#         username = request.form['username']
#         password = request.form['password']
#
#         # Check if the username and password are valid
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             # Log the user in
#             login_user(user)
#             return redirect(url_for('streamlit'))
#
#         # If the username or password is invalid, show an error message
#         st.warning('Invalid username or password')
#
#     # If the user is already logged in, redirect to the Streamlit app page
#     if User.is_authenticated:
#         return redirect(url_for('streamlit'))
#
#     # Show the login form
#     st.write('Please login:')
#     username = st.text_input('Username')
#     password = st.text_input('Password', type='password')
#     submit = st.button('Login')
#
#     if submit:
#         # Check if the username and password are valid
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             # Log the user in
#             login_user(user)
#             return redirect(url_for('streamlit'))
#
#         # If the username or password is invalid, show an error message
#         st.warning('Invalid username or password')
#
#
# @app.route('/streamlit')
# @login_required
# def streamlit():
#     # Render your Streamlit app page
#     st.write('Welcome to my Streamlit app!')
#     acceuil()
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     # Log the user out
#     logout_user()
#
#     # Redirect to the login page
#     return redirect(url_for('login'))
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

#
# import subprocess
# from flask import Flask, redirect, url_for, request
# from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
# import streamlit as st
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# class User(UserMixin):
#     pass
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     # Implement this function to load a user from a user ID
#     return User.get(user_id)
#
#
# @app.route('/')
# def index():
#     return redirect(url_for('login'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Implement your login logic here
#         username = request.form['username']
#         password = request.form['password']
#
#         # Check if the username and password are valid
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             # Log the user in
#             login_user(user)
#             return redirect(url_for('streamlit'))
#
#         # If the username or password is invalid, show an error message
#         st.warning('Invalid username or password')
#
#     # If the user is already logged in, redirect to the Streamlit app page
#     if User.is_authenticated:
#         return redirect(url_for('streamlit'))
#
#     # Show the login form
#     st.write('Please login:')
#     username = st.text_input('Username')
#     password = st.text_input('Password', type='password')
#     submit = st.button('Login')
#
#     if submit:
#         # Check if the username and password are valid
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             # Log the user in
#             login_user(user)
#             return redirect(url_for('streamlit'))
#
#         # If the username or password is invalid, show an error message
#         st.warning('Invalid username or password')
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     # Log the user out
#     logout_user()
#
#     # Redirect to the login page
#     return redirect(url_for('login'))
#
#
# def start_flask_app():
#     # Start the Flask app
#     app.run()
#
#
# def main():
#     # Start the Flask app in a separate process
#     flask_process = subprocess.Popen(['python', 'app.py'])
#
#     # Render your Streamlit app page
#     st.write('Welcome to my Streamlit app!')
#     # ...
#
#     # Implement your Streamlit app logic here
#     # ...
#
#     # Terminate the Flask app process when the Streamlit app is stopped
#     flask_process.terminate()
#
#
# if __name__ == '__main__':
#     # Run the Streamlit app
#     main()

import subprocess
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import streamlit as st

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    # Implement this function to load a user from a user ID
    return User.get(user_id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Implement your login logic here
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Log the user in
            login_user(user)
            return redirect(url_for('streamlit'))

        # If the username or password is invalid, show an error message
        st.warning('Invalid username or password')

    # If the user is already logged in, redirect to the Streamlit app page
    if User.is_authenticated:
        return redirect(url_for('streamlit'))

    # Show the login form
    st.write('Please login:')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submit = st.button('Login')

    if submit:
        # Check if the username and password are valid
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Log the user in
            login_user(user)
            return redirect(url_for('streamlit'))

        # If the username or password is invalid, show an error message
        st.warning('Invalid username or password')


@app.route('/logout')
@login_required
def logout():
    # Log the user out
    logout_user()

    # Redirect to the login page
    return redirect(url_for('login'))


@app.route('/streamlit')
@login_required
def streamlit():
    # This is the Streamlit app code
    st.write("Hello, world!")


def run_flask():
    app.run()

if __name__ == '__main__':
    subprocess.Popen(["streamlit", "run", "home.py"])
    run_flask()
