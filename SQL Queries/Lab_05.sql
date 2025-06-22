--Question-04

SELECT round(MAX(Salary)) "Maximum",
        round(MIN(Salary)) "Minimum",
        round(SUM(Salary)) "Sum",
        round(AVG(Salary)) "Average"
FROM HR.EMPLOYEES;


--Question-05

SELECT job_id,
        round(MAX(Salary)) "Maximum",
        round(MIN(Salary)) "Minimum",
        round(SUM(Salary)) "Sum",
        round(AVG(Salary)) "Average"
FROM HR.EMPLOYEES
GROUP BY job_id;


--Question - 06

--Part-1

SELECT job_id, count(*)
FROM HR.EMPLOYEES
GROUP BY job_id;

--Part-2

SELECT job_id, count(*)
FROM HR.EMPLOYEES
where job_id = UPPER('&job_id')
GROUP BY job_id;


--Question - 07

SELECT count(distinct manager_id) "Number of Managers"
FROM HR.EMPLOYEES;


--Question - 08

SELECT MAX(salary) - MIN(salary) as Difference
FROM HR.EMPLOYEES;


--Question - 09


SELECT manager_id, MIN(Salary)
FROM HR.EMPLOYEES
WHERE manager_id IS NOT NULL
GROUP BY manager_id
HAVING MIN(Salary) >= 6000
ORDER BY MIN(Salary) DESC;


-- Question - 10

SELECT COUNT (*)                                               total,
       COUNT (decode (to_char (hire_date, 'YYYY'), 1995, '1')) "1995",
       COUNT (decode (to_char (hire_date, 'YYYY'), 1996, '1')) "1996",
       COUNT (decode (to_char (hire_date, 'YYYY'), 1997, '1')) "1997",
       COUNT (decode (to_char (hire_date, 'YYYY'), 1998, '1')) "1998"
FROM HR.EMPLOYEES;


-- Question - 11

SELECT job_id                                            "Job",
            SUM (decode (department_id, 20, salary)) "Dept 20",
            SUM (decode (department_id, 50, salary)) "Dept 50",
            SUM (decode (department_id, 80, salary)) "Dept 80",
            SUM (decode (department_id, 90, salary)) "Dept 90",
            SUM (salary)                                total
FROM HR.employees
WHERE department_id IN (20, 50, 80, 90)
GROUP BY job_id
ORDER BY job_id;
