from datetime import datetime
from inspect import getframeinfo, currentframe
from os import environ
from urllib.parse import unquote

from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from werkzeug.exceptions import HTTPException, abort

from app.Database.DatabaseManipulator import DatabaseManipulator, check_input, get_difference
from app.Forms.AddTypeForm import AddTypeForm
from app.Forms.UpdateTypeForm import UpdateTypeForm
from app.decorators.flask_decorators import login_required, admin_login_required
from app.Forms.LoginForm import LoginForm
from app.Forms.PartsForm import PartsForm
from app.Forms.RegisterForm import RegisterForm
from app.Forms.UpdatePartsForm import UpdatePartsForm
from app.Forms.UpdateVanForm import UpdateVanForm
from app.Forms.UpdatePartThresh import UpdatePartThresh
from app.Forms.VanForm import VanForm
from app.csp import csp

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


# Handle the 401 error
@app.errorhandler(401)
@login_required
def custom_401(e):
    return Response(e, 401, {'error': '401: Unauthorized'})


# Handle the 404 error
@app.errorhandler(404)
@login_required
def not_found(e):
    return render_template('error.html', e=e)


# Handle the 409 error
@app.errorhandler(409)
@login_required
def custom_401(e):
    return Response(e, 409, {'error': '409: Conflict'})


# Handle the 500 error
@app.errorhandler(500)
@login_required
def internal_error(e):
    return render_template('error.html', e=e)


# Main index.html route
@app.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def index():
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
            username = form.username.data
            password = form.password.data
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
            username = form.username.data
            password = form.password.data
            conf_password = form.confPass.data
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
@login_required
def parts():
    part_results = dbm.fetchall()
    van_nums = dbm.get_van_nums()
    form = PartsForm()
    update_form = UpdatePartsForm()
    if request.method == 'POST':
        part_name = form.partName.data
        part_amount = str(form.partAmount.data)
        part_number = form.partNumber.data
        van_number = unquote(form.van.data)
        part_type = str(form.unit.data)
        # Insert into the database
        dbm.insert(part_name=part_name, part_amount=part_amount, part_number=part_number, van_number=van_number,
                   part_type=part_type)
    try:
        # Populate the van choices and type choices for the insert/update part select statements
        form.van.choices = dbm.get_selections()
        form.unit.choices = dbm.get_part_type_names()
        update_form.newVan.choices = dbm.get_selections()
        update_form.newUnit.choices = dbm.get_part_type_names()
        return render_template('parts.html', results=part_results, van_nums=van_nums, form=form,
                               update_form=update_form)
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# Route for the /parts/<part_number> route
@app.route('/parts/<part_id>', methods=['GET', 'POST'])
@login_required
def display_part(part_id):
    results = dbm.get_part_information(part_id)
    # If results exist, render template
    if results:
        form = UpdatePartThresh()
        return render_template('display_part.html', parts=results, form=form)
    # Else, redirect
    else:
        if 'vans' in str(request.referrer):
            return redirect(url_for('vans'))
        else:
            return redirect(url_for('parts'))


# Route for displaying low parts
@app.route('/parts/low', strict_slashes=False, methods=['GET'])
@login_required
def low_parts():
    results = dbm.get_low_parts()
    return render_template('low_parts.html', results=results)


# Route for displaying/adding the type of parts
@app.route('/parts/type', strict_slashes=False, methods=['GET', 'POST'])
def type_parts():
    add_type_form = AddTypeForm()
    update_type_form = UpdateTypeForm()
    results = dbm.get_part_types()
    if request.method == 'POST':
        type_name = add_type_form.typeName.data
        type_unit = add_type_form.typeUnit.data
        dbm.insert_part_type(str(type_name), str(type_unit))
    return render_template('type_parts.html', results=results, form=add_type_form, update_form=update_type_form)


# Route for displaying parts by Type ID
@app.route('/parts/type/<type_id>', strict_slashes=False, methods=['GET'])
def type_parts_id(type_id):
    results = dbm.get_part_type_by_name(type_id)
    update_form = UpdatePartsForm()
    update_form.newVan.choices = dbm.get_selections()
    update_form.newUnit.choices = dbm.get_part_type_names()
    # Make sure the part exists, if not redirect back to the /types route
    if dbm.check_if_type_exists(type_id):
        return render_template('display_type_part.html', results=results, update_form=update_form)
    else:
        return redirect(url_for('type_parts'))


# Displays the table code in parts_table.html, so it can be refreshed dynamically without reloading the page
@app.route('/table/<table_name>/<quantity_id>', strict_slashes=False, methods=['GET', 'POST'])
def table(table_name, quantity_id):
    # Requirements to return the results for a van by its number
    if table_name == 'vans' and quantity_id != 'all':
        form = PartsForm()
        update_form = UpdatePartsForm()
        results = dbm.get_vans(quantity_id)
        check_exist = dbm.check_if_exists(quantity_id)
        form.unit.choices = dbm.get_part_type_names()
        update_form.newUnit.choices = dbm.get_part_type_names()
        return render_template('load/van_table.html', results=results, check_exist=check_exist, form=form,
                               update_form=update_form)
    # Requirements to return the list of accounts
    elif table_name == 'users' and quantity_id != 'all':
        results = dbm.get_users(username=session['username'])
        return render_template('load/accounts_table.html', users=results)
    # Requirements to return the job list of parts
    elif table_name == 'jobs' and quantity_id != 'all':
        select_parts = dbm.get_parts_by_van(quantity_id)
        return render_template('load/jobs_table.html', van_parts=select_parts)
    # Requirements to return the full job list of parts
    elif table_name == 'jobs' and quantity_id == 'all':
        job_parts = dbm.get_jobs()
        return render_template('load/display_jobs_table.html', jobs=job_parts)
    # Requirements to return the master list of parts
    elif table_name == 'main' and quantity_id == 'all':
        form = PartsForm()
        update_form = UpdatePartsForm()
        results = dbm.fetchall()
        van_nums = dbm.get_van_nums()
        # Set the choices for selecting a new van
        update_form.newVan.choices = dbm.get_selections()
        update_form.newUnit.choices = dbm.get_part_type_names()
        return render_template('load/parts_table.html', results=results, van_nums=van_nums, form=form,
                               update_form=update_form)
    # Requirements for the individual attributes for a part
    elif table_name == 'display_part' and quantity_id != 'all':
        form = UpdatePartThresh()
        results = dbm.get_part_information(part_id=quantity_id)
        return render_template('load/display_part_table.html', parts=results, form=form)
    # if table_name is vans_list, and van_number is all, return the following
    elif table_name == 'vans_list' and quantity_id == 'all':
        update_form = UpdateVanForm()
        van_nums = dbm.get_van_nums()
        return render_template('load/vans_list.html', van_numbers=van_nums, update_form=update_form)
    elif table_name == 'part_type_list' and quantity_id != 'all':
        results = dbm.get_part_type_by_name(type_name=quantity_id)
        update_form = UpdatePartsForm()
        update_form.newVan.choices = dbm.get_selections()
        update_form.newUnit.choices = dbm.get_part_type_names()
        return render_template('load/display_part_type_table.html', results=results, update_form=update_form)
    elif table_name == 'part_type_list' and quantity_id == 'all':
        add_type_form = AddTypeForm()
        update_type_form = UpdateTypeForm()
        results = dbm.get_part_types()
        return render_template('load/type_table.html', results=results, form=add_type_form,
                               update_form=update_type_form)
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
    # If the id_type is a type, delete the type
    elif request.method == 'POST' and id_type == 'type':
        form = UpdateTypeForm()
        type_id = form.id.data
        dbm.delete_part_type(type_id)
    # If the /delete route is accessed, re-route to index
    return redirect(url_for('index'))


# Route to edit table rows using the update method
@app.route('/update/<id_type>', strict_slashes=False, methods=['POST', 'GET'])
def update(id_type):
    try:
        # Route to update a part by the ID
        if request.method == 'POST' and id_type == 'part':
            form = UpdatePartsForm()
            part_id = form.id.data
            part_name = form.partName.data
            part_amount = str(form.newPartAmount.data)
            part_number = form.partNumber.data
            van_number = unquote(form.newVan.data)
            part_type = form.newUnit.data
            if check_input(part_id) and check_input(part_name) and check_input(part_amount) \
                    and check_input(part_number) and check_input(van_number) and check_input(part_type):
                dbm.update(part_id, part_name, part_amount, part_number, van_number, part_type)
        # Update the threshold of a part by its ID
        if request.method == 'POST' and id_type == 'threshold':
            form = UpdatePartThresh()
            part_id = form.id.data
            thresh = form.newThresh.data
            if check_input(str(part_id)) and check_input(str(thresh)):
                dbm.update_threshold(thresh, part_id)
        # Route to update a van by the ID
        elif request.method == 'POST' and id_type == 'van':
            form = UpdateVanForm()
            van_id = form.id.data
            van_number = unquote(form.vanNumber.data)
            if check_input(van_id) and check_input(van_number):
                dbm.update_van(van_id, van_number)
        # Route to update an account by the ID to grant admin attribute
        elif request.method == 'POST' and id_type == 'user':
            user_id = request.form.get('user_id')
            value = request.form.get('value')
            dbm.modify_admin(user_id, value)
        elif request.method == 'POST' and id_type == 'type':
            update_type_form = UpdateTypeForm()
            type_id = update_type_form.id.data
            type_unit = update_type_form.newTypeUnit.data
            type_name = update_type_form.newTypeName.data
            dbm.update_part_type(type_id=type_id, type_unit=type_unit, type_name=type_name)
        # If the /update route is accessed, re-route to index
        return redirect(url_for('index'))
    except TypeError as e:
        print(str(getframeinfo(currentframe()).function) + '\n' + str(e) + '\n'
              + 'Blank input detected, database not manipulated.')


# Route for /vans
@app.route('/vans', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def vans():
    form = VanForm()
    update_form = UpdateVanForm()
    van_numbers = dbm.get_van_nums()
    if request.method == 'POST':
        van_number = unquote(form.van_number.data)
        dbm.insert_van(van_number)
    try:
        return render_template('vans.html', van_numbers=van_numbers, form=form, update_form=update_form)
    except IndexError:
        abort(404), 404
    except HTTPException:
        abort(500)


# Route for /vans that consumes the van_id
@app.route('/vans/<van_number>', strict_slashes=False)
@login_required
def van_num(van_number):
    insert_form = PartsForm()
    update_form = UpdatePartsForm()
    # Populate the insert form/update form select elements
    insert_form.unit.choices = dbm.get_part_type_names()
    update_form.newUnit.choices = dbm.get_part_type_names()
    results = dbm.get_vans(van_number)
    check_exist = dbm.check_if_exists(van_number)
    # If there are no results in the van database, but it exists, execute the following
    if results is None and check_exist:
        return render_template('display_van.html', results=None, check_exist=check_exist, form=insert_form,
                               update_form=update_form)
    # If the results are not None, return the following
    elif results is not None:
        return render_template('display_van.html', results=results, form=insert_form, update_form=update_form)
    # Otherwise, redirect to the main /vans page
    else:
        return redirect(url_for('vans'))


# Allows admins to manage the users that have access to the system
@app.route('/users', strict_slashes=False, methods=['GET', 'POST'])
@admin_login_required
def users():
    username = session['username']
    get_users = dbm.get_users(username)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        dbm.confirm_account(user_id)
    else:
        return render_template('users.html', users=get_users)
    # If the route is accessed, re-route to index
    return redirect(url_for('index'))


# Route for jobs/
@app.route('/jobs/', strict_slashes=False, methods=['GET'])
@admin_login_required
def _jobs():
    all_jobs = dbm.get_jobs()
    return render_template('display_jobs.html', jobs=all_jobs)


# Route for jobs/<van_id>
@app.route('/jobs/<van_id>', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def jobs(van_id):
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
