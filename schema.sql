DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS records;

CREATE TABLE patient (
        id INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        hash TEXT NOT NULL, 
        full_name TEXT NOT NULL, 
        gender TEXT NOT NULL, 
        dob DATE NOT NULL, 
        contact NUMERIC NOT NULL, 
        email TEXT NOT NULL, 
        address TEXT NOT NULL, 
        emergency_contact NUMERIC NOT NULL, 
        medical_history TEXT, 
        created DATETIME NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (email)
);
CREATE INDEX ix_patient_id ON patient (id);
CREATE UNIQUE INDEX ix_patient_username ON patient (username);
CREATE TABLE doctor (
        id INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        full_name TEXT NOT NULL, 
        gender TEXT NOT NULL, 
        dob DATE NOT NULL, 
        contact NUMERIC NOT NULL, 
        email TEXT NOT NULL, 
        specialities TEXT, 
        reg_no INTEGER NOT NULL, 
        hash TEXT NOT NULL, 
        created DATETIME NOT NULL, 
        validated DATETIME NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (email), 
        UNIQUE (reg_no)
);
CREATE INDEX ix_doctor_id ON doctor (id);
CREATE UNIQUE INDEX ix_doctor_username ON doctor (username);
CREATE TABLE doctor_pre_val (
        id INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        full_name TEXT NOT NULL, 
        gender TEXT NOT NULL, 
        dob DATE NOT NULL, 
        contact NUMERIC NOT NULL, 
        email TEXT NOT NULL, 
        specialities TEXT, 
        reg_no INTEGER NOT NULL, 
        hash TEXT NOT NULL, 
        created DATETIME NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email), 
        UNIQUE (reg_no)
);
CREATE TABLE admin (
        id INTEGER NOT NULL, 
        identification_no INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        hash TEXT NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (username)
);
CREATE INDEX ix_admin_id ON admin (id);
CREATE TABLE alembic_version (
        version_num VARCHAR(32) NOT NULL, 
        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE hospital (
        id INTEGER NOT NULL, 
        name TEXT NOT NULL, 
        address TEXT NOT NULL, 
        contact NUMERIC NOT NULL, email TEXT NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE INDEX ix_hospital_id ON hospital (id);
CREATE TABLE IF NOT EXISTS "log" (
        id INTEGER NOT NULL, 
        created DATETIME NOT NULL, 
        remarks TEXT NOT NULL, user TEXT, 
        PRIMARY KEY (id)
);
CREATE INDEX ix_log_id ON log (id);
CREATE TABLE doc_session (
        id INTEGER NOT NULL, 
        date DATE NOT NULL, 
        start_t TIME NOT NULL, 
        end_t TIME NOT NULL, 
        doc_id INTEGER NOT NULL, 
        hl_id INTEGER NOT NULL, 
        total_apmts INTEGER NOT NULL, 
        apmt_count INTEGER NOT NULL DEFAULT 0, 
        PRIMARY KEY (id), 
        FOREIGN KEY(doc_id) REFERENCES doctor (id), 
        FOREIGN KEY(hl_id) REFERENCES hospital (id)
);
CREATE INDEX ix_doc_session_id ON doc_session (id);
CREATE TABLE appointment (
        id INTEGER NOT NULL, 
        datetime DATETIME NOT NULL, 
        doc_id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        hl_id INTEGER NOT NULL,
        s_id INTEGER NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (datetime), 
        FOREIGN KEY(doc_id) REFERENCES doctor (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id), 
        FOREIGN KEY(hl_id) REFERENCES hospital (id),
        FOREIGN KEY(s_id) REFERENCES doc_session (id)
);
CREATE INDEX ix_appointment_id ON appointment (id);