
-- insert data into TREATS Relation --

INSERT INTO Treats (drug_id, disease_name)
SELECT DISTINCT d.drug_id, TRIM(f.disease_name)
FROM DRUGS_FULL f
JOIN Drug d
  ON LOWER(TRIM(f.drug_name)) = LOWER(TRIM(d.drug_name))
 AND LOWER(TRIM(f.drug_category)) = LOWER(TRIM(d.drug_category))
JOIN Disease ds
  ON LOWER(TRIM(f.disease_name)) = LOWER(TRIM(ds.disease_name))
WHERE f.drug_name IS NOT NULL AND f.disease_name IS NOT NULL;

COMMIT;

SELECT * FROM TREATS;






-- insert data into HasSideEffect Relation --


INSERT INTO HasSideEffect (drug_id, side_effect_name)
SELECT DISTINCT d.drug_id, TRIM(se.side_effect)
FROM (
    SELECT drug_name, drug_category, side_effect1 AS side_effect FROM DRUGS_FULL
    UNION ALL
    SELECT drug_name, drug_category, side_effect2 FROM DRUGS_FULL
    UNION ALL
    SELECT drug_name, drug_category, side_effect3 FROM DRUGS_FULL
    UNION ALL
    SELECT drug_name, drug_category, side_effect4 FROM DRUGS_FULL
    UNION ALL
    SELECT drug_name, drug_category, side_effect5 FROM DRUGS_FULL
) se
JOIN Drug d
  ON LOWER(TRIM(se.drug_name)) = LOWER(TRIM(d.drug_name))
 AND LOWER(TRIM(se.drug_category)) = LOWER(TRIM(d.drug_category))
WHERE se.side_effect IS NOT NULL;



COMMIT;

SELECT * FROM HASSIDEEFFECT;









-- insert data into TestedIn Relation --

INSERT INTO TestedIn (drug_id, clinical_trial_title)
SELECT DISTINCT d.drug_id, TRIM(f.clinical_trial_title)
FROM DRUGS_FULL f
JOIN Drug d
  ON LOWER(TRIM(f.drug_name)) = LOWER(TRIM(d.drug_name))
 AND LOWER(TRIM(f.drug_category)) = LOWER(TRIM(d.drug_category))
WHERE f.clinical_trial_title IS NOT NULL;


SELECT * FROM TESTEDIN;


COMMIT;

DROP TABLE TestedIn;



-- insert data into Studies Relation --
INSERT INTO Studies (clinical_trial_title, condition_name)
SELECT DISTINCT clinical_trial_title, condition_name FROM (
    SELECT clinical_trial_title, clinical_trial_condition1 AS condition_name FROM DRUGS_FULL
    UNION
    SELECT clinical_trial_title, clinical_trial_condition2 FROM DRUGS_FULL
    UNION
    SELECT clinical_trial_title, clinical_trial_condition3 FROM DRUGS_FULL
)
WHERE clinical_trial_title IS NOT NULL AND condition_name IS NOT NULL;


SELECT * FROM STUDIES;


COMMIT;

