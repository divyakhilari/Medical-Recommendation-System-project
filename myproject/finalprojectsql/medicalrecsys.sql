CREATE DATABASE patientdb;
USE patientdb;
CREATE TABLE patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    birth_date DATE NOT NULL,
    age INT NOT NULL,
    blood_group VARCHAR(10) NOT NULL,
    address VARCHAR(200) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    location VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL
);
CREATE TABLE recommendation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    disease VARCHAR(120) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);
CREATE TABLE description (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    detail TEXT NOT NULL,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(id)
);
CREATE TABLE precaution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    precaution TEXT NOT NULL,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(id)
);
CREATE TABLE medication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    medication TEXT NOT NULL,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(id)
);
CREATE TABLE workout (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    workout TEXT NOT NULL,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(id)
);
CREATE TABLE diet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    diet TEXT NOT NULL,
    FOREIGN KEY (recommendation_id) REFERENCES recommendation(id)
);
INSERT INTO patient (name, gender, birth_date, age, blood_group, address, phone, location, email, password_hash)
VALUES ('Divya', 'Female', '2002-05-10', 23, 'B+', 'Pune, Maharashtra', '9876543210', 'Pune', 'divya@example.com', 'hashedpassword123');
INSERT INTO recommendation (patient_id, disease)
VALUES (1, 'Diabetes');
INSERT INTO description (recommendation_id, detail)
VALUES (1, 'Diabetes is a condition with high blood sugar levels.');

INSERT INTO precaution (recommendation_id, precaution)
VALUES (1, 'Avoid sugary foods'), (1, 'Exercise regularly');

INSERT INTO medication (recommendation_id, medication)
VALUES (1, 'Metformin (general info)'), (1, 'Insulin (general info)');

INSERT INTO workout (recommendation_id, workout)
VALUES (1, 'Walking 30 minutes daily');

INSERT INTO diet (recommendation_id, diet)
VALUES (1, 'High fiber foods'), (1, 'Low sugar diet');
SELECT p.name, r.disease, d.detail, pr.precaution, m.medication, w.workout, di.diet
FROM patient p
JOIN recommendation r ON p.id = r.patient_id
JOIN description d ON r.id = d.recommendation_id
JOIN precaution pr ON r.id = pr.recommendation_id
JOIN medication m ON r.id = m.recommendation_id
JOIN workout w ON r.id = w.recommendation_id
JOIN diet di ON r.id = di.recommendation_id;

SHOW DATABASES;
USE patientdb;
SHOW TABLES;
SELECT id FROM recommendation WHERE patient_id = 1;
SELECT * FROM recommendation;
DELETE FROM description WHERE recommendation_id = 1;
DELETE FROM precaution WHERE recommendation_id = 1;
DELETE FROM medication WHERE recommendation_id = 1;
DELETE FROM workout WHERE recommendation_id = 1;
DELETE FROM diet WHERE recommendation_id = 1;
DELETE FROM recommendation WHERE id = 1;
DELETE FROM patient WHERE id = 1;
SELECT * FROM description;
SELECT * FROM recommendation;
SELECT * FROM patient;
DELETE FROM patient WHERE id = 12;


ALTER TABLE description ADD COLUMN content VARCHAR(500) NOT NULL;
ALTER TABLE precaution ADD COLUMN content VARCHAR(200) NOT NULL;
ALTER TABLE medication ADD COLUMN content VARCHAR(200) NOT NULL;
ALTER TABLE diet ADD COLUMN content VARCHAR(200) NOT NULL;
ALTER TABLE workout ADD COLUMN content VARCHAR(200) NOT NULL;

ALTER TABLE description DROP COLUMN content;
ALTER TABLE precaution DROP COLUMN content;
ALTER TABLE medication DROP COLUMN content;
ALTER TABLE diet DROP COLUMN content;
ALTER TABLE workout DROP COLUMN content;


ALTER TABLE precaution ADD COLUMN detail TEXT NOT NULL;

DESCRIBE description;
DESCRIBE precaution;
DESCRIBE medication;
DESCRIBE diet;
DESCRIBE workout;



DROP TABLE IF EXISTS description;
DROP TABLE IF EXISTS precaution;
DROP TABLE IF EXISTS medication;
DROP TABLE IF EXISTS diet;
DROP TABLE IF EXISTS workout;

CREATE TABLE description (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    detail TEXT NOT NULL
);

CREATE TABLE precaution (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    precaution TEXT NOT NULL
);

CREATE TABLE medication (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    medication TEXT NOT NULL
);

CREATE TABLE diet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    diet TEXT NOT NULL
);

CREATE TABLE workout (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recommendation_id INT NOT NULL,
    workout TEXT NOT NULL
);


