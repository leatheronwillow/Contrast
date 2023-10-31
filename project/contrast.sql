CREATE TABLE people (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    mobile TEXT,
    email TEXT
);

CREATE TABLE users (
    people_id INTEGER PRIMARY KEY,
    username text NOT NULL UNIQUE,
    hash text NOT NULL UNIQUE,
)

CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    people_id INTEGER,
    category TEXT NOT NULL,
    balance_paisa INTEGER DEFAULT 0,
    FOREIGN KEY (people_id) REFERENCES people(id)
);

CREATE TABLE address (
    company_id INTEGER PRIMARY KEY,
    unit TEXT,
    block TEXT,
    street TEXT,
    city TEXT
    FOREIGN KEY (company_id)
);



