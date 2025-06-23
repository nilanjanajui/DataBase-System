-- Question - 01

SELECT sysdate "Date"
FROM dual;




-- Question - 02

SELECT employee_id,
    last_name,
    salary,
    round(salary * 1.155) "New Salary"
FROM employees;




-- Question - 04

SELECT employee_id,
    last_name,
    salary,
    round(salary * 1.155) "New Salary",
    round(salary * 1.155) - salary "Increase"
FROM employees;



-- Question - 05

SELECT initcap(last_name) "Name",
    length(last_name) "Length"
FROM employees
WHERE last_name LIKE 'J%' OR last_name
LIKE 'A%' OR last_name LIKE 'M%'
ORDER BY last_name;





-- Question - 06

SELECT last_name,
    round(months_between(sysdate, hire_date)) months_worked
FROM employees
ORDER BY months_worked;




-- Question - 07

SELECT last_name,
   lpad(salary, 15, '$') salary
FROM employees;





-- Question - 08

SELECT substr(last_name, 1, 8) || rpad(' ', round(salary/1000) + 1, '*')
employees_and_their_salaries
FROM employees
ORDER BY salary DESC;



-- Question - 09

SELECT last_name, trunc((sysdate- hire_date) / 7) tenure
FROM employees
WHERE department_id = 90
ORDER BY tenure DESC;



