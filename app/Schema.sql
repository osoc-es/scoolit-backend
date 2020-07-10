CREATE DATABASE IF NOT EXISTS scoolit;


DROP TABLE IF EXISTS User;

CREATE TABLE User (
    id varchar NOT NULL,
    username varchar NOT NULL,
    password varchar NOT NULL,
    email varchar NOT NULL,
    logic_deleted boolean DEFAULT FALSE,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS Message;
CREATE TABLE Message (
    id varchar NOT NULL,
    send_date date NOT NULL,
    content varchar NOT NULL,
    transmitter varchar NOT NULL,
    receiver varchar NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (transmitter) references User(id),
    FOREIGN KEY (receiver) references User(id)
);

DROP TABLE IF EXISTS Book;

CREATE TABLE Book (
    title varchar NOT NULL,
    edition varchar NOT NULL,
    editorial varchar NOT NULL,
    isbn varchar NOT NULL,
    subject varchar NOT NULL,
    entry_date date NOT NULL,
    total_quantity int,
    available_quantity int,
    PRIMARY KEY (isbn)
);