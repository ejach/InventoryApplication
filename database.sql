create table parts
(
	id int auto_increment,
	name text null,
	part_number text null,
	constraint parts_pk
		primary key (id)
);