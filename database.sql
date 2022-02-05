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

-- Table for jobs
create table jobs
(
    job_id      int auto_increment,
    job_name    varchar(255) not null,
    van_number  varchar(255) not null,
    part_amount int          not null,
    part_number varchar(255) not null,
    part_name   varchar(255) not null,
    primary key (job_id, van_number),
    constraint jobs_job_id_uindex
        unique (job_id),
    constraint jobs_part_name_uindex
        unique (part_name),
    constraint jobs_part_number_uindex
        unique (part_number),
    constraint jobs_van_number_uindex
        unique (van_number),
    constraint jobs_parts_amount_fk
        foreign key (part_amount) references parts (amount)
            on update cascade,
    constraint jobs_parts_number_fk
        foreign key (part_number) references parts (part_number),
    constraint jobs_vans_van_number_fk
        foreign key (van_number) references vans (van_number)
);

