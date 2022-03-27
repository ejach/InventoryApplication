### Unit Tests
#### Test Environment
```bash
PYTHONUNBUFFERED=1
host=xxx
webui_host=localhost
webui_port=5000
username=xxx
password=xxx
db=xxx
# Existing phone number used in unit testing
TEST_PHONE=xxx
```
#### Expected Output

```
Process finished with exit code 0
test_add_part_amount() TEST
insert() part amount TRUE test -> PASSED
insert() part amount FALSE test -> PASSED
test_add_van() TEST
insert_van() test -> PASSED
insert_van() FALSE test -> PASSED
test_check_duplicates() TEST
check_duplicates() duplicate van FALSE test -> PASSED
check_duplicates() duplicate van TRUE test -> PASSED
test_check_input() TEST
check_input() TRUE test -> PASSED
check_input() Empty Input test -> PASSED
check_input() Space Input test -> PASSED
test_check_password() TEST
check_password() False input test -> PASSED
check_password_hash() False input test -> PASSED
test_create_job() TEST
create job FALSE TEST -> PASSED
create job TRUE TEST -> PASSED
test_create_job() TEST -> PASSED
test_delete_van() TEST
delete_van() test -> PASSED
test_enter_low_threshold() TEST
insert part TEST -> PASSED
update threshold TEST -> PASSED
test_enter_low_threshold() TEST -> PASSED
test_false_part_amount() TEST
insert() part amount invalid input test -> PASSED
test_get_selections() TEST
get_selections TEST -> PASSED
check_if_van_exist() TEST -> PASSED
test_invalid_low_threshold() TEST
insert part TEST -> PASSED
update threshold INVALID TEST -> PASSED
test_enter_invalid_threshold() TEST -> PASSED
test_job_part_difference() TEST
record_job FALSE TEST -> PASSED
record_job TRUE TEST -> PASSED
test_job_part_difference() TEST -> PASSED
test_login_confirmation() TEST
CREATE ACCOUNT TEST -> PASSED
LOGIN ACCOUNT UNCONFIRMED TEST -> PASSED
LOGIN ACCOUNT CONFIRMED TEST -> PASSED
DELETE ACCOUNT TEST -> PASSED
test_login_deny() TEST
CREATE DENIED ACCOUNT TEST -> PASSED
DELETE DENIED ACCOUNT TEST -> PASSED
FAIL LOGIN ACCOUNT TEST -> PASSED
test_parts_delete() TEST
insert() TRUE test -> PASSED
delete() test -> PASSED
test_parts_update() TEST
update() test -> PASSED
test_toggle_admin() TEST
MAKE ADMIN TEST -> PASSED
REMOVE ADMIN TEST -> PASSED
REMOVE ACCOUNT TEST -> PASSED
test_type_duplicate_insertion() TEST
Insert Type TEST -> PASSED
Type Duplicate TEST -> PASSED
test_type_duplicate_insertion() TEST -> PASSED
test_type_insertion() TEST
Type Insertion TEST -> PASSED
Insert Part TEST -> PASSED
Check Part Type TEST -> PASSED
test_type_insertion() TEST -> PASSED
test_type_update() TEST
Insert Type TEST -> PASSED
Update Type TEST -> PASSED
test_type_update() TEST -> PASSED
test_update_part_amount() TEST
insert() part amount update insert test -> PASSED
insert() part amount update test -> PASSED
test_update_parts() TEST
insert_van TEST -> PASSED
update TEST -> PASSED
test_update_parts() TEST -> PASSED
test_update_van() TEST
update_van() TypeError test -> PASSED
update_van() test -> PASSED
```
