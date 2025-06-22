-- Question - 01

CREATE TABLE MY_EMPLOYEE (
    ID         NUMBER(4)
    CONSTRAINT MY_EMPLOYEE_ID_NN NOT NULL,
    LAST_NAME  VARCHAR2(25),
    FIRST_NAME VARCHAR2(25),
    USERID     VARCHAR2(8),
    SALARY     NUMBER(9, 2)
);




-- Question - 02

DESCRIBE my_employee;




-- Question - 03

INSERT INTO MY_EMPLOYEE VALUES (1, 'Patel', 'Ralph', 'rpatel', 895 );




-- Question - 04

INSERT INTO MY_EMPLOYEE (ID, LAST_NAME, FIRST_NAME, USERID, SALARY) 
VALUES ( 2, 'Dancs', 'Betty','bdancs', 860 );




-- Question - 05

SELECT *
FROM MY_EMPLOYEE;




-- Question - 06

SET ECHO OFF
SET VERIFY OFF
INSERT INTO my_employee
VALUES (&p_id, '&p_last_name', '&p_first_name',
lower(substr('&p_first_name', 1, 1) ||
substr('&p_last_name', 1, 7)), &p_salary);
SET VERIFY ON
SET ECHO ON




-- Question - 07

SET ECHO OFF
SET VERIFY OFF
INSERT INTO my_employee
VALUES (&p_id, '&p_last_name', '&p_first_name',
lower(substr('&p_first_name', 1, 1) ||
substr('&p_last_name', 1, 7)), &p_salary);
SET VERIFY ON
SET ECHO ON



-- Question - 08

SELECT *
FROM MY_EMPLOYEE
ORDER BY ID;



-- Question - 09

COMMIT;




-- Question - 10

UPDATE MY_EMPLOYEE
SET LAST_NAME = 'Drexler'
WHERE ID = 3;




-- Question - 11

UPDATE MY_EMPLOYEE
SET SALARY = 1000
WHERE SALARY < 900;




-- Question - 12

SELECT *
FROM MY_EMPLOYEE
ORDER BY ID;




-- Question - 13

DELETE FROM MY_EMPLOYEE
WHERE LAST_NAME = 'Dancs';




-- Question - 14

SELECT *
FROM MY_EMPLOYEE
ORDER BY ID;




-- Question - 15

COMMIT;



-- Question - 16

SET ECHO OFF
SET VERIFY OFF
INSERT INTO my_employee
VALUES (&p_id, '&p_last_name', '&p_first_name',
lower(substr('&p_first_name', 1, 1) ||
substr('&p_last_name', 1, 7)), &p_salary);
SET VERIFY ON
SET ECHO ON




-- Question - 17

SELECT *
FROM MY_EMPLOYEE
ORDER BY ID;



-- Question - 18

SAVEPOINT STEP_18;




-- Question - 19

DELETE FROM MY_EMPLOYEE;



-- Question - 20

SELECT *
FROM MY_EMPLOYEE;




-- Question - 21

ROLLBACK TO STEP_18;



-- Question - 22

SELECT *
FROM MY_EMPLOYEE
ORDER BY ID;



-- Question - 23

COMMIT;



