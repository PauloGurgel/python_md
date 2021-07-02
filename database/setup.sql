create database icl_consultation;
create database icl_finance;

use icl_consultation;

create table consultations (
  id VARCHAR(255) PRIMARY KEY
  , start_date datetime
  , end_date datetime
  , physician_id VARCHAR(255)
  , patient_id VARCHAR(255)
  , price NUMERIC(10,4));  
  

use icl_finance;

create table appointments (
    appointment_id VARCHAR(255) PRIMARY KEY
  , price NUMERIC(10,4));  


CREATE USER 'icl_cons_user'@'%' IDENTIFIED BY 'iclpassword';
CREATE USER 'icl_fina_user'@'%' IDENTIFIED BY 'iclpassword';
GRANT USAGE ON *.* TO 'icl_cons_user'@'%';
GRANT USAGE ON *.* TO 'icl_fina_user'@'%';
GRANT EXECUTE, SELECT, SHOW VIEW, ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE, CREATE TEMPORARY TABLES, CREATE VIEW, DELETE, DROP, EVENT, INDEX, INSERT, REFERENCES, TRIGGER, UPDATE, LOCK TABLES  ON `icl\_consultation`.* TO 'icl_cons_user'@'%' WITH GRANT OPTION;
GRANT EXECUTE, SELECT, SHOW VIEW, ALTER, ALTER ROUTINE, CREATE, CREATE ROUTINE, CREATE TEMPORARY TABLES, CREATE VIEW, DELETE, DROP, EVENT, INDEX, INSERT, REFERENCES, TRIGGER, UPDATE, LOCK TABLES  ON `icl\_finance`.* TO 'icl_fina_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

