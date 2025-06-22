-- Question - 01

CREATE TABLE dept
(id NUMBER(7),
name VARCHAR2(25));


DESCRIBE dept;



-- Question - 02

INSERT INTO dept
SELECT department_id, department_name
FROM hr.departments;



-- Question - 03

CREATE TABLE emp
(id NUMBER(7),
last_name VARCHAR2(25),
first_name VARCHAR2(25),
dept_id NUMBER(7));


DESCRIBE emp;



-- Question - 04

ALTER TABLE emp
MODIFY (last_name VARCHAR2(50));


DESCRIBE emp;



-- Question - 05

SELECT table_name
FROM user_tables
WHERE table_name IN ('DEPT', 'EMP');



-- Question - 06

CREATE TABLE employees2 AS
SELECT employee_id id, first_name, last_name, salary, 
       department_id dept_id
FROM hr.employees;



-- Question - 07

DROP TABLE emp;



-- question - 08

RENAME employees2 TO emp;



-- Question - 09

COMMENT ON TABLE emp IS 'Employee Information';
COMMENT ON TABLE dept IS 'Department Information';

SELECT *
FROM user_tab_comments
WHERE table_name = 'DEPT'
OR table_name = 'EMP';



-- Question - 10

ALTER TABLE emp
DROP COLUMN FIRST_NAME;


DESCRIBE emp;



-- Question - 11

ALTER TABLE emp
SET UNUSED (dept_id);


DESCRIBE emp;



-- Question - 12

ALTER TABLE emp
DROP UNUSED COLUMNS;


DESCRIBE emp;


