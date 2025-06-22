-- Question - 01

SELECT last_name, department_id, salary
FROM hr.employees
WHERE (salary, department_id) IN
      (SELECT salary, department_id
      FROM hr.employees
      WHERE commission_pct IS NOT NULL);



-- Question - 02

SELECT last_name, department_name, salary
FROM hr.employees e, hr.departments d
WHERE e.department_id = d.department_id
AND (salary, NVL(commission_pct,0)) IN
    (SELECT salary, NVL(commission_pct,0)
    FROM hr.employees e, hr.departments d
    WHERE e.department_id = d.department_id
    AND d.location_id = 1700);



-- Question - 03

SELECT last_name, hire_date, salary
FROM hr.employees
WHERE (salary, NVL(commission_pct, NULL)) IN
    (SELECT salary, NVL(commission_pct,NULL)
        FROM hr.employees
        WHERE last_name = 'Kochhar')
AND last_name != 'Kochhar';


-- alternative
-- SELECT last_name, TO_CHAR(hire_date, 'DD-MON-RR') AS hire_date, salary
-- FROM hr.employees
-- WHERE salary = 17000 AND commission_pct IS NULL AND last_name != 'Kochhar';




-- Question - 04

SELECT last_name, job_id, salary
FROM hr.employees
WHERE salary > ALL
                (SELECT salary
                FROM hr.employees
                WHERE job_id = 'SA_MAN')
ORDER BY salary DESC;



-- Question - 05

SELECT employee_id, last_name, department_id
FROM hr.employees
WHERE department_id IN (SELECT department_id
FROM hr.departments
WHERE location_id IN (SELECT location_id
                      FROM hr.locations
                      WHERE city LIKE 'T%'));



-- Question - 06

SELECT e.last_name ename, e.salary salary,
e.department_id deptno, ROUND(AVG(a.salary), 4) dept_avg
FROM hr.employees e, hr.employees a
WHERE e.department_id = a.department_id
AND e.salary > (SELECT AVG(salary)
                FROM hr.employees
                WHERE department_id = e.department_id )
GROUP BY e.last_name, e.salary, e.department_id
ORDER BY AVG(a.salary);



-- Question - 07

-- a)

SELECT e1.last_name
FROM hr.employees e1
WHERE NOT EXISTS (SELECT 'X'
                  FROM hr.employees e2
                  WHERE e2.manager_id = e1.employee_id);



-- b)

SELECT e1.last_name
FROM hr.employees e1
WHERE e1.employee_id NOT IN (SELECT e2.manager_id
        FROM hr.employees e2);



-- Question - 08

SELECT last_name
FROM hr.employees e1
WHERE e1.salary < (SELECT ROUND(AVG(e2.salary), 4)
                   FROM hr.employees e2
                   WHERE e2.department_id = e1.department_id);



-- Question - 09

SELECT last_name
FROM hr.employees e1
WHERE EXISTS (SELECT 'X'
              FROM hr.employees e2
              WHERE e2.department_id = e1.department_id
              AND e2.hire_date > e1.hire_date
              AND e2.salary > e1.salary);



-- Question - 10

SELECT employee_id, last_name,
        (SELECT department_name
        FROM hr.departments d
        WHERE e.department_id = d.department_id ) department
FROM hr.employees e
ORDER BY department;



-- Question - 11

WITH
summary AS (
    SELECT department_name, SUM(salary) AS dept_total
    FROM hr.employees, hr.departments
    WHERE employees.department_id =
    departments.department_id
    GROUP BY department_name)
SELECT department_name, dept_total
FROM summary
WHERE dept_total > (
    SELECT SUM(dept_total) * 1/8
    FROM summary)
ORDER BY dept_total DESC;