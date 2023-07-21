DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS records;

CREATE TABLE doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_id INTEGER NOT NULL,
    username TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    contact NUMERIC NOT NULL,
    email TEXT NOT NULL,
    spec TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    dob NUMERIC NOT NULL,
    contact NUMERIC NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pt_age INTEGER NOT NULL,
    remarks TEXT NOT NULL,
    ref INTEGER,
    doctor_id INTEGER NOT NULL,
    patient_id INTEGER NOT NULL,
    datetime TIMESTAMP NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctor (id),
    FOREIGN KEY (patient_id) REFERENCES patient (id),
    FOREIGN KEY (ref) REFERENCES doctor (id)
);