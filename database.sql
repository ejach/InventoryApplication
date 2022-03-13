-- Used for the parts database
create table parts
(
    id          int auto_increment
        primary key,
    name        varchar(255)             null,
    amount      int          default 0   not null,
    part_number varchar(255) default '0' null,
    van_number  varchar(255)             null,
    low_thresh  int                      null,
    type        varchar(255)             null,
    unit        varchar(20)              null,
    constraint parts_part_type_type_name_fk
        foreign key (type) references part_type (type_name)
            on update cascade on delete cascade,
    constraint parts_part_type_type_unit_fk
        foreign key (unit) references part_type (type_unit)
            on update cascade on delete cascade
);

create index parts_amount_index
    on parts (amount);

create index parts_name_index
    on parts (name);

create index parts_part_number_index
    on parts (part_number);

create index parts_type_index
    on parts (type);

create index parts_unit_index
    on parts (unit);

create index van_number
    on parts (van_number);



-- Table for the vans
create table vans
(
    id         int auto_increment
        primary key,
    van_number varchar(255) null
);

create index van_number
    on vans (van_number);


-- Table for accounts
create table accounts
(
    id           int auto_increment
        primary key,
    username     text          null,
    password     text          null,
    is_admin     int default 0 null,
    is_confirmed int default 0 null
);

-- Table for jobs
create table jobs
(
    job_id     int auto_increment
        primary key,
    username   varchar(255) null,
    time       varchar(255) null,
    van_number varchar(255) null,
    parts_used int          null,
    constraint jobs_vans_van_number_fk
        foreign key (van_number) references vans (van_number)
            on update cascade on delete cascade
);

create index jobs_van_number_index
    on jobs (van_number);

-- Table for part_type
create table part_type
(
    id        int auto_increment
        primary key,
    type_name varchar(255) null,
    type_unit varchar(255) null
);

create index part_type_type_name_index
    on part_type (type_name);

create index part_type_type_unit_index
    on part_type (type_unit);
