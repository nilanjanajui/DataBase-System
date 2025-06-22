-- Question - 01

SELECT last_name, to_char (hire_date, 'DD-MON-YY') hire_date
FROM HR.EMPLOYEES
WHERE department_id = ( SELECT department_id
                        FROM hr.employees
                        WHERE last_name = initcap ('&&last_name'))
AND last_name <> initcap ('&last_name');



-- Question - 02

SELECT employee_id, last_name, salary
FROM HR.EMPLOYEES
WHERE salary > (SELECT AVG(salary)
                FROM HR.EMPLOYEES)
ORDER BY salary ASC;



-- Question - 03

SELECT employee_id, last_name
FROM HR.EMPLOYEES
WHERE department_id IN (SELECT department_id
                        FROM HR.EMPLOYEES
                        WHERE last_name LIKE '%u%');




-- Question - 04

SELECT last_name, department_id, job_id
FROM HR.EMPLOYEES
WHERE department_id IN (SELECT department_id
                        FROM HR.DEPARTMENTS
                        WHERE location_id = &location_id)
ORDER BY department_id;




-- Question - 05

SELECT last_name, salary
FROM HR.EMPLOYEES
WHERE manager_id IN (SELECT employee_id
                    FROM HR.EMPLOYEES
                    WHERE last_name = 'King');




-- Question - 06

SELECT department_id, last_name, job_id
FROM HR.EMPLOYEES
WHERE department_id IN (SELECT department_id
                          FROM HR.DEPARTMENTS
                          WHERE department_name = 'Executive');




-- Question - 07

SELECT employee_id, last_name, salary
FROM HR.EMPLOYEES
WHERE salary > (SELECT AVG(salary)
                FROM HR.EMPLOYEES)
AND department_id IN (SELECT department_id
                        FROM HR.EMPLOYEES
                        WHERE last_name LIKE '%u%');