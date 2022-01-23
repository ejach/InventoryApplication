### Expected Output
```python
***SETUP***
test_add_part_amount() TEST
insert() part amount TRUE test -> PASSED
insert() part amount FALSE test -> PASSED
***TEARDOWN***
***SETUP***
test_add_van() TEST
insert_van() test -> PASSED
insert_van() FALSE test -> PASSED
***TEARDOWN***
***SETUP***
test_check_duplicates() TEST
check_duplicates() duplicate van FALSE test -> PASSED
check_duplicates() duplicate van TRUE test -> PASSED
***TEARDOWN***
***SETUP***
test_check_input() TEST
check_input() TRUE test -> PASSED
check_input() Empty Input test -> PASSED
check_input() Space Input test -> PASSED
***TEARDOWN***
***SETUP***
test_check_password() TEST
check_password() False input test -> PASSED
check_password_hash() False input test -> PASSED
***TEARDOWN***
***SETUP***
test_delete_van() TEST
delete_van() test -> PASSED
***TEARDOWN***
***SETUP***
test_false_part_amount() TEST
insert() part amount invalid input test -> PASSED
***TEARDOWN***
***SETUP***
test_login_confirmation() TEST
CREATE ACCOUNT TEST -> PASSED
LOGIN ACCOUNT UNCONFIRMED TEST -> PASSED
LOGIN ACCOUNT CONFIRMED TEST -> PASSED
DELETE ACCOUNT TEST -> PASSED
***TEARDOWN***
***SETUP***
test_login_deny() TEST
CREATE DENIED ACCOUNT TEST -> PASSED
DELETE DENIED ACCOUNT TEST -> PASSED
FAIL LOGIN ACCOUNT TEST -> PASSED
***TEARDOWN***
***SETUP***
test_parts() TEST
insert() TRUE test -> PASSED
delete() test -> PASSED
update() test -> PASSED
***TEARDOWN***
***SETUP***
test_update_part_amount() TEST
insert() part amount update insert test -> PASSED
insert() part amount update test -> PASSED
***TEARDOWN***
***SETUP***
test_update_van() TEST
update_van() TypeError test -> PASSED
update_van() test -> PASSED
***TEARDOWN***
```
