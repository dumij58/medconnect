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
        created DATETIME NOT NULL, 
        details_added BOOLEAN NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (email)
);
CREATE UNIQUE INDEX ix_patient_username ON patient (username);
CREATE INDEX ix_patient_id ON patient (id);
CREATE TABLE doctor (
        id INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        full_name TEXT NOT NULL, 
        gender TEXT NOT NULL, 
        dob DATE NOT NULL, 
        contact NUMERIC NOT NULL, 
        email TEXT NOT NULL, 
        reg_no INTEGER NOT NULL, 
        hash TEXT NOT NULL, 
        created DATETIME NOT NULL, 
        validated DATETIME NOT NULL, specializations TEXT, 
        PRIMARY KEY (id), 
        UNIQUE (email), 
        UNIQUE (reg_no)
);
CREATE INDEX ix_doctor_id ON doctor (id);
CREATE UNIQUE INDEX ix_doctor_username ON doctor (username);
CREATE TABLE hospital (
        id INTEGER NOT NULL, 
        name TEXT NOT NULL, 
        address TEXT NOT NULL, 
        email TEXT NOT NULL, 
        contact NUMERIC NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);
CREATE INDEX ix_hospital_id ON hospital (id);
CREATE TABLE admin (
        id INTEGER NOT NULL, 
        identification_no INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        hash TEXT NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (username)
);
CREATE INDEX ix_admin_id ON admin (id);
CREATE TABLE log (
        id INTEGER NOT NULL, 
        created DATETIME NOT NULL, 
        user TEXT, 
        remarks TEXT NOT NULL, 
        PRIMARY KEY (id)
);
CREATE INDEX ix_log_id ON log (id);
CREATE TABLE medical_history (
        id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        medical_condition TEXT, 
        diagnosis_date DATE, 
        treatment TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE TABLE medication (
        id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        medication_name TEXT, 
        dosage TEXT, 
        frequency TEXT, 
        start_date DATE, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE TABLE surgery (
        id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        surgery_name TEXT, 
        date DATE, 
        notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE TABLE vaccination (
        id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        vaccine_name TEXT, 
        administration_date DATE, 
        notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE TABLE family_history (
        id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        relationship TEXT, 
        medical_condition TEXT, 
        notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE TABLE doc_session (
        id INTEGER NOT NULL, 
        date DATE NOT NULL, 
        start_t TIME NOT NULL, 
        end_t TIME NOT NULL, 
        doc_id INTEGER NOT NULL, 
        hl_id INTEGER NOT NULL, 
        total_apmts INTEGER NOT NULL, 
        apmt_count INTEGER NOT NULL, 
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
        status TEXT NOT NULL, 
        PRIMARY KEY (id), 
        UNIQUE (datetime), 
        FOREIGN KEY(doc_id) REFERENCES doctor (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id), 
        FOREIGN KEY(hl_id) REFERENCES hospital (id), 
        FOREIGN KEY(s_id) REFERENCES doc_session (id)
);
CREATE INDEX ix_appointment_id ON appointment (id);
CREATE TABLE vital_sign (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        sign TEXT NOT NULL, 
        value TEXT NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id)
);
CREATE INDEX ix_vital_sign_id ON vital_sign (id);
CREATE TABLE examination_note (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        title TEXT, 
        notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id)
);
CREATE INDEX ix_examination_note_id ON examination_note (id);
CREATE TABLE treatment_medications (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        medication_name TEXT, 
        dosage TEXT, 
        frequency TEXT, 
        start_date DATE, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id)
);
CREATE TABLE treatment_other (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        title TEXT, 
        notes TEXT NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id)
);
CREATE INDEX ix_treatment_other_id ON treatment_other (id);
CREATE TABLE referral (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        created DATETIME NOT NULL, 
        doc_id INTEGER, 
        external_doc_name TEXT, 
        external_doc_specialization TEXT, 
        reason TEXT NOT NULL, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id), 
        FOREIGN KEY(doc_id) REFERENCES doctor (id)
);
CREATE INDEX ix_referral_id ON referral (id);
CREATE TABLE alembic_version (
        version_num VARCHAR(32) NOT NULL, 
        CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
CREATE TABLE IF NOT EXISTS "doctor_pre_val" (
        id INTEGER NOT NULL, 
        username TEXT NOT NULL, 
        full_name TEXT NOT NULL, 
        gender TEXT NOT NULL, 
        dob DATE NOT NULL, 
        contact NUMERIC NOT NULL, 
        email TEXT NOT NULL, 
        reg_no INTEGER NOT NULL, 
        hash TEXT NOT NULL, 
        created DATETIME NOT NULL, 
        specializations TEXT, 
        PRIMARY KEY (id), 
        UNIQUE (username), 
        UNIQUE (email), 
        UNIQUE (reg_no)
);
CREATE TABLE medical_record (
        id INTEGER NOT NULL, 
        created DATETIME NOT NULL, 
        doc_id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        hl_id INTEGER NOT NULL,
        apmt_id INTEGER NOT NULL,
        chief_complaint TEXT, 
        diagnosis TEXT, 
        follow_up_date DATETIME, 
        follow_up_notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(doc_id) REFERENCES doctor (id), 
        FOREIGN KEY(pt_id) REFERENCES patient (id), 
        FOREIGN KEY(hl_id) REFERENCES hospital (id),
        FOREIGN KEY(apmt_id) REFERENCES appointment (id)
);
CREATE INDEX ix_mediical_record_id ON medical_record (id);
CREATE TABLE order_test (
        id INTEGER NOT NULL, 
        mr_id INTEGER NOT NULL, 
        pt_id INTEGER NOT NULL, 
        test_name TEXT NOT NULL, 
        test_date DATE NOT NULL, 
        additional_notes TEXT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(mr_id) REFERENCES medical_record (id),
        FOREIGN KEY(pt_id) REFERENCES patient (id)
);
CREATE INDEX ix_order_test_id ON order_test (id);