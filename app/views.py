from datetime import datetime
from os import environ
from bleach import clean
from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_wtf import CSRFProtect
from werkzeug.exceptions import HTTPException, abort
from flask_talisman import Talisman

from app.Forms.LoginForm import LoginForm
from app.Forms.RegisterForm import RegisterForm
from app.Forms.PartsForm import PartsForm
from app.Forms.UpdateVanForm import UpdateVanForm
from app.Forms.VanForm import VanForm
from app.Forms.UpdatePartsForm import UpdatePartsForm
from app.csp import csp

from app.Database.DatabaseConnector import DatabaseConnector
from app.Database.DatabaseManipulator import DatabaseManipulator, check_input, get_difference

# Initialize the app
app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')

# Initialize Cross-Site Request Forgery protection
csrf = CSRFProtect()
csrf.init_app(app)

# Only trigger SSLify if the app is running on Heroku
if 'DYNO' in environ:
    Talisman(app, content_security_policy=csp)

# Instantiate the DatabaseManipulator
dbm = DatabaseManipulator()
# Instantiate the DatabaseConnector
dbc = DatabaseConnector()


# Handle the 401 error
@app.errorhandler(401)
def custom_401(e):
    if not session:
        return redirect(url_for('login'))
    else:
        return Response(e, 401, {'error': '401: Unauthorized'})


# Handle the 404 error
@app.errorhandler(404)
def not_found(e):
    if not session:
        return redirect(url_for('login'))
    else:
        return render_template('error.html', e=e)


# Handle the 409 error
@app.errorhandler(409)
def custom_401(e):
    if not session:
        return redirect(url_for('login'))
    else:
        return Response(e, 409, {'error': '409: Conflict'})


# Handle the 500 error
@app.errorhandler(500)
def internal_error(e):
    if not session:
        return redirect(url_for('login'))
    else:
        return render_template('error.html', e=e)


# Main index.html route
@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    else:
        try:
            username = session['username']
            session['is_admin'] = dbm.check_admin(username)
            return render_template('index.html', username=username)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# app route for /login
@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if request.method == 'POST':
            username = clean(form.username.data)
            password = clean(form.password.data)
            my_login = dbm.login(username=username, password=password)
            if my_login:
                session['logged_in'] = True
                session['username'] = username
            # If the login is incorrect, throw 401 Unauthorized
            else:
                return render_template('login.html', form=form), 401
        if 'logged_in' not in session:
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('index'))
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# app route for /register
@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm()
        if request.method == 'POST':
            username = clean(form.username.data)
            password = clean(form.password.data)
            conf_password = clean(form.confPass.data)
            register_user = dbm.register(username, password, conf_password)
            if register_user:
                return redirect(url_for('login'))
            else:
                return render_template('register.html', form=form), 409
        elif 'logged_in' not in session:
            return render_template('register.html', form=form)
        else:
            return redirect(url_for('index'))
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# App route for /logout
@app.route('/logout', strict_slashes=False, methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', default=None)
    session.pop('username', default=None)
    session.pop('is_admin', default=None)
    return redirect(url_for('index'))


# Parts.html route
@app.route('/parts', strict_slashes=False, methods=['GET', 'POST'])
def parts():
    if not session:
        return redirect(url_for('login'))
    else:
        results = dbm.fetchall()
        webui_host = dbc.get_webui_host()
        van_nums = dbm.get_van_nums()
        form = PartsForm()
        update_form = UpdatePartsForm()
        if request.method == 'POST':
            # Sanitizes the input using bleach
            part_name = clean(form.partName.data)
            part_amount = clean(str(form.partAmount.data))
            part_number = clean(form.partNumber.data)
            van_number = clean(form.van.data)
            # Insert into the database
            dbm.insert(part_name=part_name, part_amount=part_amount, part_number=part_number, van_number=van_number)
        try:
            # Populate the van choices for the insert/update part select statements
            form.van.choices = dbm.get_selections()
            update_form.newVan.choices = dbm.get_selections()
            return render_template('parts.html', results=results, webui_host=webui_host, van_nums=van_nums, form=form,
                                   update_form=update_form)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# Displays the table code in parts_table.html, so it can be refreshed dynamically without reloading the page
@app.route('/table/<table_name>/<van_number>', strict_slashes=False, methods=['GET', 'POST'])
def table(table_name, van_number):
    # Requirements to return the results for a van by its number
    if table_name == 'vans' and van_number != 'all':
        form = PartsForm()
        update_form = UpdatePartsForm()
        results = dbm.get_vans(van_number)
        check_exist = dbm.check_if_exists(van_number)
        return render_template('load/van_table.html', results=results, check_exist=check_exist, form=form,
                               update_form=update_form)
    # Requirements to return the list of accounts
    elif table_name == 'users' and van_number != 'all':
        results = dbm.get_users(username=session['username'])
        return render_template('load/accounts_table.html', users=results)
    # Requirements to return the job list of parts
    elif table_name == 'jobs' and van_number != 'all':
        select_parts = dbm.get_parts_by_van(van_number)
        return render_template('load/jobs_table.html', van_parts=select_parts)
    # Requirements to return the full job list of parts
    elif table_name == 'jobs' and van_number == 'all':
        job_parts = dbm.get_jobs()
        return render_template('load/display_jobs_table.html', jobs=job_parts)
    # Requirements to return the master list of parts
    elif table_name == 'main' and van_number == 'all':
        form = PartsForm()
        update_form = UpdatePartsForm()
        results = dbm.fetchall()
        van_nums = dbm.get_van_nums()
        # Set the choices for selecting a new van
        update_form.newVan.choices = dbm.get_selections()
        return render_template('load/parts_table.html', results=results, van_nums=van_nums, form=form,
                               update_form=update_form)
    # if table_name is vans_list, and van_number is all, return the following
    elif table_name == 'vans_list' and van_number == 'all':
        update_form = UpdateVanForm()
        van_nums = dbm.get_van_nums()
        return render_template('load/vans_list.html', van_numbers=van_nums, update_form=update_form)
    # If the url is attempted to be accessed, redirect to index
    else:
        return redirect(url_for('index'))


# Route for the delete method
@app.route('/delete/<id_type>', strict_slashes=False, methods=['POST', 'GET'])
def delete(id_type):
    # If the id_type is part, delete the part
    if request.method == 'POST' and id_type == 'part':
        part_id = request.form.get('Delete')
        dbm.delete(part_id)
    # If the id_type is a van, delete the van
    elif request.method == 'POST' and id_type == 'van':
        van_id = request.form.get('Delete')
        dbm.delete_van(van_id)
    # If the id_type is a user, delete the user
    elif request.method == 'POST' and id_type == 'user':
        user_id = request.form.get('user_id')
        dbm.delete_account(user_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('index'))


# Route to edit table rows using the update method
@app.route('/update/<id_type>', strict_slashes=False, methods=['POST', 'GET'])
def update(id_type):
    try:
        # Route to update a part by the ID
        if request.method == 'POST' and id_type == 'part':
            form = UpdatePartsForm()
            part_id = clean(form.id.data)
            part_name = clean(form.partName.data)
            part_amount = clean(str(form.newPartAmount.data))
            part_number = clean(form.partNumber.data)
            van_number = clean(form.newVan.data)
            if check_input(part_id) and check_input(part_name) and check_input(part_amount) \
                    and check_input(part_number) and check_input(van_number):
                dbm.update(part_id, part_name, part_amount, part_number, van_number)
        # Route to update a van by the ID
        elif request.method == 'POST' and id_type == 'van':
            form = UpdateVanForm()
            van_id = clean(form.id.data)
            van_number = clean(form.vanNumber.data)
            if check_input(van_id) and check_input(van_number):
                dbm.update_van(van_id, van_number)
        # Route to update an account by the ID to grant admin attribute
        elif request.method == 'POST' and id_type == 'user':
            user_id = request.form.get('user_id')
            value = request.form.get('value')
            dbm.modify_admin(user_id, value)
        # If the /update route is accessed, re-route to index
        return redirect(url_for('index'))
    except TypeError as e:
        print(str(e) + '\n' + 'Blank input detected, database not manipulated.')


# Route for /vans
@app.route('/vans', strict_slashes=False, methods=['GET', 'POST'])
def vans():
    if not session:
        return redirect(url_for('login'))
    else:
        form = VanForm()
        update_form = UpdateVanForm()
        van_numbers = dbm.get_van_nums()
        if request.method == 'POST':
            van_number = clean(form.van_number.data)
            dbm.insert_van(van_number)
        try:
            return render_template('vans.html', van_numbers=van_numbers, form=form, update_form=update_form)
        except IndexError:
            abort(404), 404
        except HTTPException:
            abort(500)


# Route for /vans that consumes the van_id
@app.route('/vans/<van_id>', strict_slashes=False)
def van_num(van_id=0):
    form = PartsForm()
    update_form = UpdatePartsForm()
    if not session:
        return redirect(url_for('login'))
    else:
        results = dbm.get_vans(van_id)
        check_exist = dbm.check_if_exists(van_id)
        # If there are no results in the van database, but it exists, execute the following
        if results is None and check_exist:
            return render_template('display_van.html', results=None, check_exist=check_exist, form=form,
                                   update_form=update_form)
        # If the results are not None, return the following
        elif results is not None:
            return render_template('display_van.html', results=results, form=form, update_form=update_form)
        # Otherwise, redirect to the main /vans page
        else:
            return redirect(url_for('vans'))


# Allows admins to manage the users that have access to the system
@app.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def users():
    username = session['username']
    get_users = dbm.get_users(username)
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    elif dbm.check_admin(username) == 0:
        return redirect(url_for('index'))
    elif request.method == 'POST':
        user_id = clean(request.form.get('user_id'))
        dbm.confirm_account(user_id)
    else:
        return render_template('users.html', users=get_users)
    # If the route is accessed, re-route to index
    return redirect(url_for('index'))


# Route for jobs/
@app.route('/jobs/', methods=['GET'])
def _jobs():
    if not session or not session['is_admin']:
        redirect(url_for('index'))
    else:
        all_jobs = dbm.get_jobs()
        return render_template('display_jobs.html', jobs=all_jobs)


# Route for jobs/<van_id>
@app.route('/jobs/<van_id>', methods=['GET', 'POST'])
def jobs(van_id):
    if not session:
        redirect(url_for('index'))
    else:
        van_amount = dbm.get_total_parts_by_van(van_id)
        select_parts = dbm.get_parts_by_van(van_id)
        check_exist = dbm.check_if_exists(van_id)
        # If the van does not exist or does not contain at least one part, redirect to index
        if not check_exist or not select_parts:
            return redirect(url_for('index'))
        elif request.method == 'POST' and request.is_json and select_parts:
            content = request.get_json()
            # The list of values to be added
            lst = []
            for i in content:
                for key, val in i.items():
                    lst.append(val)
            # Zip values into the format [(value, value), (value, value), ...]
            values = [*zip(lst[::2], lst[1::2])]
            # Values to get difference of
            res = [int(i) for i in lst[::2]]
            parts_used = sum(res)
            # Get the difference of the two values
            difference = get_difference(int(van_amount), int(parts_used))
            dbm.update_multiple_parts_by_van(values)
            # Record job in the database if there is at least 1 part changed
            if difference > 0:
                dbm.record_job(session['username'], str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')), van_id,
                               difference)
        return render_template('jobs.html', van_parts=select_parts)
