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
	id int auto_increment,
	van_number text null,
	constraint vans_pk
		primary key (id)
);

# Table for accounts
create table accounts
(
	id int auto_increment,
	username text null,
	password text null,
	constraint accounts_pk
		primary key (id)
);
