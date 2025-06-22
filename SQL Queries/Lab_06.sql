-- Question - 01

SELECT location_id, street_address, city, state_province, country_name
FROM HR.LOCATIONS
NATURAL JOIN HR.COUNTRIES;


-- Question - 02

SELECT last_name, department_id, department_name
FROM HR.EMPLOYEES
JOIN HR.DEPARTMENTS using (department_id);



-- Question - 03

SELECT last_name, job_id, department_id, department_name
FROM HR.EMPLOYEES
JOIN HR.DEPARTMENTS using (department_id)
JOIN HR.LOCATIONS using (location_id)
WHERE city = 'Toronto';



-- Question - 04

SELECT e.last_name   "Employee",
       e.employee_id "Emp#",
       m.last_name   "Manager",
       m.employee_id "Mgr#"
FROM HR.EMPLOYEES e
JOIN HR.EMPLOYEES m ON (e.manager_id = m.employee_id)
ORDER BY e.employee_id;



-- Question - 05

SELECT e.last_name   "Employee",
       e.employee_id "Emp#",
       m.last_name   "Manager",
       m.employee_id "Mgr#"
FROM hr.EMPLOYEES e
LEFT JOIN HR.EMPLOYEES m ON (e.manager_id = m.employee_id)
ORDER BY e.employee_id;



--Question - 06

SELECT e.department_id department,
       e.last_name     employee,
       c.last_name     colleague
FROM HR.EMPLOYEES e
JOIN HR.EMPLOYEES c ON (e.department_id = c.department_id)
WHERE e.employee_id <> c.employee_id
ORDER BY department, employee, colleague;



-- Question - 07
-- Part-1
DESC HR.JOBS;

-- Part-2

SELECT e.last_name,
       e.job_id,
       d.department_name,
       e.salary,
       CASE
           WHEN e.salary BETWEEN 0 AND 3000 THEN 'A'
           WHEN e.salary BETWEEN 3001 AND 6000 THEN 'B'
           WHEN e.salary BETWEEN 6001 AND 9000 THEN 'C'
           WHEN e.salary BETWEEN 9001 AND 12000 THEN 'D'
           ELSE 'E'
       END AS grade_level
FROM HR.EMPLOYEES e
JOIN HR.DEPARTMENTS d ON e.department_id = d.department_id
ORDER BY e.salary;





-- Question - 08

SELECT e.last_name,
       to_char (e.hire_date, 'DD-MON-YY') hire_date
FROM HR.EMPLOYEES e
JOIN HR.EMPLOYEES davies ON (davies.last_name = 'Davies')
WHERE davies.hire_date < e.hire_date;



-- Question - 09

SELECT e.last_name AS last_name,
       TO_CHAR(e.hire_date, 'DD-MON-YY') AS hire_date_1,
       m.last_name AS last_name_1,
       TO_CHAR(m.hire_date, 'DD-MON-YY') AS hire_date_2
FROM HR.EMPLOYEES e
JOIN HR.EMPLOYEES m ON e.manager_id = m.employee_id
WHERE e.hire_date < m.hire_date
ORDER BY e.hire_date;
