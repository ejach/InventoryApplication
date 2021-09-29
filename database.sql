create table parts
(
	id integer
		constraint parts_pk
			primary key autoincrement,
	name text,
	part_number integer
);