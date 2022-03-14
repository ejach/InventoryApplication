from importlib import import_module
from os import path, remove
from getpass import getpass
from select import select

import wget as wget
from requests import get
from bcrypt import gensalt, hashpw
from sqlalchemy import create_engine, insert, func, select, update
from sqlalchemy.orm import Session

# Create the database schema and create an admin account based on user input


# Import a module by URL and return it
def import_file(uri, name=None):
    # Download the file
    wget.download(uri)
    if not name:
        name = path.basename(uri).rstrip('.py')

    r = get(uri)
    r.raise_for_status()

    code_obj = compile(r.content, uri, 'exec')
    module = import_module(name)
    exec(code_obj, module.__dict__)
    return module


# Get database address.
db_addr = input('DB ip address: ')
# Get username of the database.
db_user = input(f'Username of {db_addr}: ')
# Get password.
db_pass = getpass(f'Password of {db_user}@{db_addr}: ')
# Get the database name.
db_name = input('Database name to connect: ')
# join the inputs into a complete database url.
url = f'mysql+pymysql://{db_user}:{db_pass}@{db_addr}/{db_name}'

# Get admin user credentials to be added

print('Database info recorded, prompting for Admin account.')

admin_user = input('Enter a username for the Admin account: ')

admin_pass = getpass('Enter a password for the Admin account: ')

conf_admin_pass = getpass('Confirm password for the Admin account: ')

# Create an engine object.
engine = create_engine(url, echo=True)

session = Session(engine)

# Import the module from GitHub
dbm = import_file('https://raw.githubusercontent.com/ejach/InventoryApplication/dev/app/Database/DatabaseTables.py')

if admin_pass and admin_user and conf_admin_pass:

    def create_password_hash(password):
        salt = gensalt()
        hashed = hashpw(password.encode('utf-8'), salt)
        return hashed


    def get_last_id(*args):
        with session as conn:
            for arg in args:
                get_id = (select(func.max(arg.id)))
                results = conn.execute(get_id).fetchone()
                return results


    dbm.metadata.create_all(engine)

    print('You have successfully connected to the database and tables have been created.' +
          '\n' + 'Creating admin account.')

    if admin_pass == conf_admin_pass:
        try:
            with session as connection:
                hashed_pw = create_password_hash(admin_pass)
                _insert_account = (insert(dbm.Account).values(username=admin_user, password=hashed_pw))
                session.execute(_insert_account)
                session.commit()
                _user_id = get_last_id(dbm.Account)[0]
                _make_admin = (update(dbm.Account).values(is_admin=1).where(dbm.Account.id == _user_id))
                session.execute(_make_admin)
                session.commit()
                _confirm_account = (update(dbm.Account).values({'is_confirmed': 1}).where(dbm.Account.id == _user_id))
                session.execute(_confirm_account)
                session.commit()
            print('Admin account created.')
            session.close()
        except TypeError as e:
            print(str(e))
        finally:
            remove('DatabaseTables.py')
    else:
        exit('The admin passwords did not match, please try again.')
