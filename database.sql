# Used for the parts database
create table parts
(
	id int auto_increment,
	name text null,
	part_number text null,
	van_number text null,
	constraint parts_pk
		primary key (id)
);

# Table for the vans
create table vans
(
	van_number text null
);

