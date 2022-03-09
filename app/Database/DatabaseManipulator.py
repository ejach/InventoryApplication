from inspect import getframeinfo, currentframe

from bcrypt import gensalt, hashpw, checkpw
from pymysql import Error
from sqlalchemy import insert, select, update, delete, func, distinct
from sqlalchemy.exc import SQLAlchemyError

from app.Database import DatabaseSession
from app.Database.DatabaseTables import Account, Van, Job, Part


# Prevent inputs that only contain spaces from being entered into the database
def check_input(test_input: str) -> bool:
    if test_input and not test_input.isspace() and '-' not in test_input:
        return True
    else:
        return False


# Create MD5 hash of password to insert into database
def create_password_hash(password: bytes) -> bytes:
    salt = gensalt()
    hashed = hashpw(password, salt)
    if check_password_hash(password, hashed):
        return hashed


# Check if the password is equal to each other
def check_password(password: str, conf_password: str) -> bool:
    if password == conf_password:
        return True
    else:
        return False


# Check if MD5 hash matches the password given
def check_password_hash(password: bytes, my_hash: bytes) -> bool:
    if checkpw(password, my_hash):
        return True
    else:
        return False


# get difference of two values
def get_difference(op1: int, op2: int) -> int:
    if op1 > op2:
        return op1 - op2
    elif op1 < op2:
        return op2 - op1
    elif op1 == op2:
        return op1 - op2


class DatabaseManipulator:
    def __init__(self) -> None:
        self.session = DatabaseSession()

    # Get all parts entries from database
    def fetchall(self) -> tuple:
        with self.session as connection:
            stmt = select(Part.id, Part.name, Part.amount, Part.part_number, Part.van_number)
            results = connection.execute(stmt).fetchall()
            return results

    # Checks to see if the van_number exists in the database already
    def check_duplicates(self, van_number: str) -> bool:
        with self.session as connection:
            try:
                stmt = (select(Van.van_number))
                results = connection.execute(stmt).fetchall()
                res = [i[0] for i in results]
                if res.count(van_number) > 0:
                    return False
                else:
                    return True
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get password by username
    def get_password_by_username(self, username: str) -> list:
        with self.session as connection:
            try:
                stmt = (select(Account.id, Account.username, Account.password, Account.is_admin, Account.is_confirmed)
                        .where(Account.username == username))
                username_res = connection.execute(stmt).fetchall()
                fin_res = [i[2] for i in username_res]
                return fin_res
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Check if account exists in the database
    def check_if_account_exists(self, username: str) -> bool:
        with self.session as connection:
            try:
                stmt = (select(Account.id, Account.username, Account.password, Account.is_admin, Account.is_confirmed)
                        .where(Account.username == username))
                get_username_results = connection.execute(stmt).fetchall()
                if not get_username_results:
                    return False
                else:
                    return True
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Check if the van exists and has a part within it from either the parts or vans DB
    def check_if_exists(self, van_number: str) -> bool:
        with self.session as connection:
            try:
                # Use the distinct select statement in the parts DB
                get_vans_dist = (select(distinct(Van.van_number)).order_by(Van.van_number))
                dist_results = connection.execute(get_vans_dist).fetchall()
                # List the results in an array
                fin_dist = [i[0] for i in dist_results]
                # Use the list of duplicates to see if the van exists in the vans DB
                get_duplicates = (select(Van.van_number))
                dupe_results = connection.execute(get_duplicates).fetchall()
                # List the results in an array
                fin_dupes = [i[0] for i in dupe_results]
                # If the van_number exists in either database, return True; otherwise return False
                if fin_dist.count(van_number) > 0 or van_number in fin_dupes:
                    return True
                else:
                    return False
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Insert van into the database
    def insert_van(self, van_number: str) -> None:
        with self.session as connection:
            try:
                # If the input is valid and the check_duplicates is valid, commit to DB
                if self.check_duplicates(van_number) and check_input(van_number):
                    stmt = (insert(Van).values(van_number=van_number))
                    connection.execute(stmt)
                    connection.commit()
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, row not inserted')
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get all vans by van number
    def get_vans(self, van_number: int) -> tuple or None:
        with self.session as connection:
            try:
                stmt = select(Part.id, Part.name, Part.amount, Part.part_number, Part.van_number) \
                    .where(Part.van_number == van_number)
                results = connection.execute(stmt).fetchall()
                # If the results are empty (i.e. the van_number doesn't exist) return None
                if not results:
                    return None
                # Else, return the following
                else:
                    return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get list of van numbers that exist in the database
    def get_van_nums(self) -> tuple:
        with self.session as connection:
            try:
                stmt = select(Van.id, Van.van_number).order_by(Van.van_number)
                results = connection.execute(stmt).fetchall()
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get the selections from the Vans that currently exist in the database
    def get_selections(self) -> list:
        results = self.get_van_nums()
        re = [(g[1], g[1]) for g in results]
        return re

    # Insert entries into database
    def insert(self, part_name: str, part_amount: str, part_number: str, van_number: str) -> None:
        with self.session as connection:
            try:
                if check_input(part_name) and check_input(part_amount) and part_amount.isnumeric() \
                        and check_input(part_number) and check_input(van_number):
                    stmt = (insert(Part).values(name=part_name, amount=part_amount, part_number=part_number,
                                                van_number=van_number))
                    connection.execute(stmt)
                    connection.commit()
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, row not inserted')
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get part information by part id
    def get_part_information(self, part_id: str) -> tuple:
        with self.session as connection:
            try:
                stmt = (select(Part.id, Part.name, Part.amount, Part.part_number, Part.van_number, Part.low_thresh)
                        .where(Part.id == part_id))
                results = connection.execute(stmt).fetchall()
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Delete entries from database by ID
    def delete(self, row_id: str) -> None:
        with self.session as connection:
            try:
                stmt = (delete(Part).where(Part.id == int(row_id)))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Update entries from database by ID
    def update(self, row_id: str, part_name: str, part_amount: str, part_number: str, van_number: str) -> None:
        with self.session as connection:
            try:
                stmt = (update(Part).values(name=part_name, amount=part_amount,
                                            part_number=part_number, van_number=van_number).where(Part.id == row_id))
                if check_input(part_name) and check_input(part_amount) and check_input(part_number) \
                        and check_input(van_number):
                    connection.execute(stmt)
                    connection.commit()
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, database not manipulated')
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Delete van by van_id
    def delete_van(self, van_id: str) -> None:
        with self.session as connection:
            try:
                stmt = (delete(Van).where(Van.id == van_id))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Update van by van_id
    def update_van(self, van_id: str, van_number: str) -> None:
        with self.session as connection:
            try:
                # Check for duplicates and validate input
                if check_input(van_number) and self.check_duplicates(van_number):
                    stmt = (update(Van).values(van_number=van_number).where(Van.id == van_id))
                    connection.execute(stmt)
                    connection.commit()
            except TypeError as e:
                print(str(e) + '\n' + 'Blank input detected, database not manipulated')
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Update part's threshold
    def update_threshold(self, thresh: int or str, part_id: int) -> None:
        with self.session as connection:
            try:
                stmt = (update(Part).values(low_thresh=thresh).where(Part.id == part_id))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get table of low parts
    def get_low_parts(self) -> tuple:
        with self.session as connection:
            try:
                stmt = (select(Part.id, Part.name, Part.amount, Part.part_number, Part.van_number, Part.low_thresh)
                        .where(Part.low_thresh > Part.amount))
                results = connection.execute(stmt).fetchall()
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Check if account is confirmed
    def check_if_confirmed(self, username: str) -> bool:
        with self.session as connection:
            try:
                stmt = (select(Account.is_confirmed).where(Account.username == func.lower(username)))
                results = connection.execute(stmt).fetchone()
                res = ''.join(map(str, str(results)))
                if int(res[1]) == 1:
                    return True
                else:
                    return False
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Confirm account by ID
    def confirm_account(self, user_id: str) -> None:
        with self.session as connection:
            try:
                stmt = (update(Account).values({'is_confirmed': 1}).where(Account.id == user_id))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Delete account by ID
    def delete_account(self, user_id: str) -> None:
        with self.session as connection:
            try:
                stmt = (delete(Account).where(Account.id == user_id))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Login by username and password
    def login(self, username: str, password: str) -> bool:
        try:
            hash_pw = self.get_password_by_username(username)
            if hash_pw and check_password_hash(password.encode('utf8'), hash_pw[0].encode('utf8')) \
                    and self.check_if_account_exists(username) and self.check_if_confirmed(username):
                return True
            else:
                return False
        except Error or SQLAlchemyError as e:
            print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Register by username, password, and conf_password
    def register(self, username: str, password: str, conf_password: str) -> bool:
        with self.session as connection:
            try:
                if check_password(password, conf_password) and check_input(password) and check_input(conf_password) \
                        and not self.check_if_account_exists(username):
                    hashed_pw = create_password_hash(password.encode('utf-8'))
                    if check_password_hash(password.encode('utf-8'), hashed_pw):
                        stmt = (insert(Account).values(username=username, password=hashed_pw))
                        connection.execute(stmt)
                        connection.commit()
                    return True
                else:
                    return False
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Check if user is an admin by username
    def check_admin(self, username: str) -> bool:
        with self.session as connection:
            try:
                stmt = (select(Account.is_admin).where(func.lower(Account.username) == username))
                results = connection.execute(stmt).fetchone()
                res = ''.join(map(str, str(results[0])))
                return True if int(res) == 1 else False
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Make / remove user from admin
    def modify_admin(self, user_id: str, value: str or int) -> None:
        with self.session as connection:
            try:
                stmt = (update(Account).values(is_admin=value).where(Account.id == user_id))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get users that exist in the DB excluding the current user's username
    def get_users(self, username: str) -> tuple:
        with self.session as connection:
            try:
                stmt = (select(Account.id, func.lower(Account.username), Account.is_admin, Account.is_confirmed).where(
                    Account.username != func.lower(username)
                ))
                results = connection.execute(stmt).fetchall()
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get parts by van number
    def get_parts_by_van(self, van_number: str) -> tuple:
        with self.session as connection:
            try:
                stmt = (select(Part.id, Part.name, Part.amount, Part.part_number)
                        .where(Part.van_number == van_number))
                results = connection.execute(stmt).fetchall()
                print(results)
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Update multiple parts according to the van number
    def update_multiple_parts_by_van(self, values: list) -> None:
        with self.session as connection:
            try:
                for item in values:
                    stmt = (update(Part).values(amount=item[0]).where(Part.id == item[1]))
                    connection.execute(stmt)
                    connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Record a new job in the database
    def record_job(self, username: str, time: str, van_number: str, parts_used: str or int) -> None:
        with self.session as connection:
            try:
                stmt = (insert(Job).values(username=func.lower(username), time=time, van_number=van_number,
                                           parts_used=parts_used))
                connection.execute(stmt)
                connection.commit()
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get all jobs from database
    def get_jobs(self) -> tuple:
        with self.session as connection:
            try:
                stmt = (select(Job.job_id, Job.username, Job.time, Job.van_number, Job.parts_used))
                results = connection.execute(stmt).fetchall()
                return results
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))

    # Get the total amount of parts by van
    def get_total_parts_by_van(self, van: int) -> int:
        with self.session as connection:
            try:
                stmt = (select(func.sum(Part.amount)).where(Part.van_number == van))
                results = connection.execute(stmt).fetchall()
                res = [i[0] for i in results]
                return res[0]
            except Error or SQLAlchemyError as e:
                print(str(getframeinfo(currentframe()).function) + '\n' + str(e))
