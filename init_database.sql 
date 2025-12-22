-- ============================================================
-- RESET DATABASE
-- ============================================================
DROP ALL OBJECTS;

-- ============================================================
-- TABLE: Patient
-- ============================================================
CREATE TABLE Patient (
    patient_id        VARCHAR(10) PRIMARY KEY,
    upi_number        VARCHAR(20),
    national_id       VARCHAR(20),
    first_name        VARCHAR(50),
    last_name         VARCHAR(50),
    gender            VARCHAR(10),
    age_years         INT,
    age_months        INT,
    phone_number      VARCHAR(20),
    country           VARCHAR(50),
    registration_date TIMESTAMP,
    patient_type      VARCHAR(20),
    created_by        VARCHAR(50)
);

-- ============================================================
-- TABLE: Visit
-- ============================================================
CREATE TABLE Visit (
    visit_id          VARCHAR(10) PRIMARY KEY,
    patient_id        VARCHAR(10),
    visit_date        DATE,
    visit_time        TIME,
    visit_type        VARCHAR(20),
    priority_status   VARCHAR(20),
    parent_visit_id   VARCHAR(10),
    current_status    VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

-- ============================================================
-- TABLE: Diagnosis
-- ============================================================
CREATE TABLE Diagnosis (
    diagnosis_id   INT AUTO_INCREMENT PRIMARY KEY,
    visit_id       VARCHAR(10),
    diagnosis_type VARCHAR(20),
    icd10_code     VARCHAR(10),
    description    VARCHAR(100),
    recorded_by    VARCHAR(50),
    recorded_at    TIMESTAMP,
    is_processed   BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (visit_id) REFERENCES Visit(visit_id)
);

-- ============================================================
-- INITIAL PATIENT DATA
-- ============================================================
INSERT INTO Patient VALUES
('P001','UPI001','NID001','Amina','Otieno','Female',28,3,'0712000001','Kenya',CURRENT_TIMESTAMP,'IDENTIFIED','system'),
('P002','UPI002','NID002','Grace','Njeri','Female',32,0,'0712000002','Somalia',CURRENT_TIMESTAMP,'UNIDENTIFIED','system'),
('P003','UPI003','NID003','Mary','Atieno','Female',24,8,'0712000003','Kenya',CURRENT_TIMESTAMP,'UNIDENTIFIED','system'),
('P004','UPI004','NID004','Elizabeth','Kamau','Female',35,1,'0712000004','Kenya',CURRENT_TIMESTAMP,'IDENTIFIED','system'),
('P005','UPI005','NID005','Joyce','Chebet','Female',29,5,'0712000005','Ethiopia',CURRENT_TIMESTAMP,'IDENTIFIED','system'),
('P006','UPI006','NID006','Purity','Muthoni','Female',22,9,'0712000006','Kenya',CURRENT_TIMESTAMP,'REFERRED','system'),
('P007','UPI007','NID007','Alice','Mutheu','Female',31,4,'0712000007','Sudan',CURRENT_TIMESTAMP,'REFERRED','system'),
('P008','UPI008','NID008','Cynthia','Wangari','Female',27,2,'0712000008','Tanzania',CURRENT_TIMESTAMP,'UNIDENTIFIED','system'),
('P009','UPI009','NID009','Sarah','Wafula','Female',30,6,'0712000009','Kenya',CURRENT_TIMESTAMP,'IDENTIFIED','system'),
('P010','UPI010','NID010','Ruth','Kiptoo','Female',26,11,'0712000010','Uganda',CURRENT_TIMESTAMP,'IDENTIFIED','system');

-- ============================================================
-- INITIAL VISITS
-- ============================================================
INSERT INTO Visit VALUES
('V001','P001',CURRENT_DATE,'09:00','ANC','ROUTINE',NULL,'Completed'),
('V002','P002',CURRENT_DATE,'09:20','IN-PATIENT','ROUTINE',NULL,'Completed'),
('V003','P003',CURRENT_DATE,'09:40','OUT-PATIENT','URGENT',NULL,'Completed'),
('V004','P004',CURRENT_DATE,'10:00','OUT-PATIENT','URGENT',NULL,'Completed'),
('V005','P005',CURRENT_DATE,'10:20','IN-PATIENT','ROUTINE',NULL,'Completed'),
('V006','P006',CURRENT_DATE,'10:40','OUT-PATIENT','EMERGENCY',NULL,'Completed'),
('V007','P007',CURRENT_DATE,'11:00','OUT-PATIENT','EMERGENCY',NULL,'Completed'),
('V008','P008',CURRENT_DATE,'11:20','EMERGENCY','ROUTINE',NULL,'Completed'),
('V009','P009',CURRENT_DATE,'11:40','EMERGENCY','ROUTINE',NULL,'Completed'),
('V010','P010',CURRENT_DATE,'12:00','OUT-PATIENT','ROUTINE',NULL,'Completed');

-- ============================================================
-- INITIAL DIAGNOSES (UNPROCESSED)
-- ============================================================
INSERT INTO Diagnosis
(visit_id, diagnosis_type, icd10_code, description, recorded_by, recorded_at, is_processed)
VALUES
('V001','FINAL','O24.0','Gestational_Type_1_diabetes_mellitus','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V002','WORKING','O24.4','Gestational_Type_2_diabetes_mellitus','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V003','FINAL','D64.9','Anemia','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V004','FINAL','O14.0','Preeclampsia','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V005','FINAL','B16.9','Hepatitis_B','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V006','WORKING','B20','HIV_infection','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V007','WORKING','B06.9','Rubella','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V008','WORKING','A53.9','Syphilis','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V009','FINAL','O24.4','Gestational_Type_2_diabetes_mellitus','nurse_mary',CURRENT_TIMESTAMP,FALSE),
('V010','FINAL','D64.9','Anemia','nurse_mary',CURRENT_TIMESTAMP,FALSE);

-- ============================================================
-- REAL-TIME SIMULATION: NEW PATIENTS
-- ============================================================
INSERT INTO Patient VALUES
('P011','UPI011','NID011','Jane','Kariuki','Female',27,6,'0712000011','Kenya',CURRENT_TIMESTAMP,'IDENTIFIED','system'),
('P012','UPI012','NID012','Faith','Mwangi','Female',30,2,'0712000012','Uganda',CURRENT_TIMESTAMP,'UNIDENTIFIED','system');

-- ============================================================
-- NEW VISITS (REAL-TIME DATA)
-- ============================================================
INSERT INTO Visit VALUES
('V011','P011',CURRENT_DATE,'09:30','ANC','ROUTINE',NULL,'Completed'),
('V012','P011',CURRENT_DATE,'10:00','OUT-PATIENT','URGENT',NULL,'Completed'),
('V013','P011',CURRENT_DATE,'10:30','IN-PATIENT','ROUTINE',NULL,'Completed'),
('V014','P012',CURRENT_DATE,'11:00','OUT-PATIENT','ROUTINE',NULL,'Completed'),
('V015','P012',CURRENT_DATE,'11:30','ANC','URGENT',NULL,'Completed'),
('V016','P012',CURRENT_DATE,'12:00','IN-PATIENT','ROUTINE',NULL,'Completed'),
('V017','P012',CURRENT_DATE,'12:30','EMERGENCY','EMERGENCY',NULL,'Completed');

-- ============================================================
-- DIAGNOSES FOR NEW VISITS (UNPROCESSED)
-- ============================================================
INSERT INTO Diagnosis
(visit_id, diagnosis_type, icd10_code, description, recorded_by, recorded_at, is_processed)
VALUES
('V011','FINAL','O99.0','Sample_diagnosis_V011','system',CURRENT_TIMESTAMP,FALSE),
('V012','FINAL','O99.1','Sample_diagnosis_V012','system',CURRENT_TIMESTAMP,FALSE),
('V013','FINAL','O99.2','Sample_diagnosis_V013','system',CURRENT_TIMESTAMP,FALSE),
('V014','FINAL','O99.3','Sample_diagnosis_V014','system',CURRENT_TIMESTAMP,FALSE),
('V015','FINAL','O99.4','Sample_diagnosis_V015','system',CURRENT_TIMESTAMP,FALSE),
('V016','FINAL','O99.5','Sample_diagnosis_V016','system',CURRENT_TIMESTAMP,FALSE),
('V017','FINAL','O99.6','Sample_diagnosis_V017','system',CURRENT_TIMESTAMP,FALSE);
