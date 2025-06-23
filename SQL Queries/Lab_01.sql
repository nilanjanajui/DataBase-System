-- Question - 04

DESCRIBE departments;
SELECT * FROM departments;



-- Question - 05

DESCRIBE employees;



-- Question - 06

SELECT employee_id, last_name, job_id, hire_date startdate
FROM employees;



-- Question - 07

SELECT DISTINCT job_id
FROM employees;




-- Question - 08

SELECT employee_id "Emp #",
last_name "Employee",
job_id  "Job",
hire_date "Hire Date"
FROM employees;




-- Question - 09

SELECT last_name ||','|| job_id "Employee and Title"
FROM employees;




-- Question - 10

SELECT employee_id || ',' ||
first_name || ',' ||
last_name || ',' ||
email || ',' ||
phone_number || ',' ||
job_id || ',' ||
manager_id || ',' ||
hire_date || ',' ||
commission_pct || ',' ||
department_id the_output
FROM employees;


