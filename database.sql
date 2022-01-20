# Used for the parts database
create table parts
(
	id int auto_increment,
	name text null,
	amount int default 0 null,
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
    id           int auto_increment
        primary key,
    username     text          null,
    password     text          null,
    is_admin     int default 0 null,
    is_confirmed int default 0 null
);

