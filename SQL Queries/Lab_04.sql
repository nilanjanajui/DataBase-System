-- Question - 01

SELECT last_name || ' earns $' || to_char(salary, 'FM99,999.00') ||
        'monthly but wants $' ||to_char(salary * 3, 'FM99,999.00') 
        "Dream Salaries"
FROM employees;




-- Question - 02

SELECT last_name, hire_date, to_char(next_day (add_months(hire_date, 6), 1),
    'FMDAY, "the" DDSPTH "of" MONTH, YYYY') review
FROM employees;





-- Question - 03

SELECT last_name, hire_date, to_char(hire_date, 'FMDAY') day
FROM employees
ORDER BY to_char(hire_date, 'D');



-- Question - 04

SELECT last_name, nvl(to_char(commission_pct), 'No Commission') comm
FROM employees;





-- Question - 05

SELECT job_id, decode(job_id, 'AD_PRES', 'A', 
                               'ST_MAN', 'B',
                               'IT_PROG', 'C',
                               'SA_REP', 'D',
                               'ST_CLERL', 'E', 0) grade
FROM employees;




-- Question - 06

SELECT job_id,
    CASE job_id WHEN 'AD_PRES' THEN 'A'
                WHEN 'ST_MAN' THEN 'B'
                WHEN 'IT_PROG' THEN 'C'
                WHEN 'SA_REP' THEN 'D'
                WHEN 'ST_CLERK' THEN 'E'
                ELSE '0'
    END grade
FROM employees;



