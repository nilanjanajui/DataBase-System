-- Question - 01

SELECT last_name, salary
FROM employees
WHERE salary > 12000;




-- Question - 02

SELECT last_name, department_id
FROM employees
WHERE employee_id = 176;




-- Question - 03

SELECT last_name, salary
FROM employees
WHERE salary NOT BETWEEN 5000 AND 12000;



-- Question - 04

SELECT last_name, job_id, hire_date
FROM employees
WHERE last_name IN ('Matos', 'Taylor')
ORDER BY hire_date;




-- Question - 05

SELECT last_name, department_id
FROM employees
WHERE department_id IN (20, 50)
ORDER BY last_name;




-- Question - 06

SELECT last_name "Employee", salary "Monthly Salary"
FROM employees
WHERE salary BETWEEN 5000 AND 12000
AND department_id IN (20, 50)
ORDER BY last_name;





-- Question - 07

SELECT last_name, hire_date
FROM employees
WHERE hire_date LIKE '94%';



-- Question - 08

SELECT last_name, job_id
FROM employees
WHERE manager_id IS NULL;




-- Question - 09

SELECT last_name, salary, commission_pct
FROM employees
WHERE commission_pct IS NOT NULL
ORDER BY 2 DESC, 3 DESC;




-- Question - 10

SELECT last_name, salary
FROM employees
WHERE salary > &salary;




-- Question - 11

SELECT employee_id, last_name, salary, department_id
FROM employees
WHERE manager_id = &manager_id
ORDER BY &order_col;



-- Question - 12

SELECT last_name
FROM employees
WHERE last_name LIKE '__a%';





-- Question - 13

SELECT last_name
FROM employees
WHERE last_name LIKE '%a%' AND last_name LIKE '%e%';




-- Question - 14

SELECT last_name, job_id, salary
FROM employees
WHERE job_id IN ('SA_REP', 'ST_CLERK')
AND salary NOT IN (2500, 3500, 7000);




-- Question - 15

SELECT last_name "Employee",
    salary "Monthly Salary",
    commission_pct
FROM employees
WHERE commission_pct = .2;




