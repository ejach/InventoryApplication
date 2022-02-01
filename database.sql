-- Used for the parts database
create table parts
(
    id          int auto_increment
        primary key,
    name        varchar(255)             null,
    amount      int          default 0   not null,
    part_number varchar(255) default '0' null,
    van_number  varchar(255)             null,
    constraint parts_vans_van_number_fk
        foreign key (van_number) references vans (van_number)
            on update cascade on delete cascade
);

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

