
-- Insert into DRUG Table:

INSERT INTO DRUG (drug_id, drug_name, drug_category)
SELECT 
    ROW_NUMBER() OVER (ORDER BY drug_name, drug_category) AS drug_id,
    drug_name,
    drug_category
FROM (
    SELECT DISTINCT drug_name, drug_category
    FROM DRUGS_FULL
    WHERE drug_name IS NOT NULL
);


-- extra three drug_name into DRUG Table --

INSERT INTO DRUG (drug_id, drug_name, drug_category)
SELECT 
    ROW_NUMBER() OVER (ORDER BY drug_name) + (
        SELECT NVL(MAX(drug_id), 0) FROM DRUG
    ) AS drug_id,
    drug_name,
    NULL AS drug_category
FROM (
    SELECT 'butabarbital' AS drug_name FROM DUAL
    UNION ALL
    SELECT 'salsalate' FROM DUAL
    UNION ALL
    SELECT 'midodrine' FROM DUAL
) sub;


COMMIT;

SELECT * from DRUG;







--Insert into Disease table--

INSERT INTO Disease (disease_name, disease_category)
SELECT DISTINCT disease_name, disease_category
FROM DRUGS_FULL
WHERE disease_name IS NOT NULL;

COMMIT;

SELECT * from DISEASE;








-- Insert into Product table-- 

INSERT INTO PRODUCT (product_id, product_name, company_name, drug_id)
SELECT 
    ROW_NUMBER() OVER (ORDER BY product_name, company_name) AS product_id,
    product_name,
    company_name,
    drug_id
FROM (
    SELECT DISTINCT product_name, company_name, drug_id
    FROM DRUGS_FULL
    WHERE product_name IS NOT NULL 
      AND company_name IS NOT NULL
      AND drug_id IS NOT NULL
);

COMMIT;

SELECT * from PRODUCT;







--  Insert into SideEffect Table --

INSERT INTO SideEffect (side_effect_name)
SELECT DISTINCT side_effect FROM (
    SELECT side_effect1 AS side_effect FROM DRUGS_FULL
    UNION
    SELECT side_effect2 FROM DRUGS_FULL
    UNION
    SELECT side_effect3 FROM DRUGS_FULL
    UNION
    SELECT side_effect4 FROM DRUGS_FULL
    UNION
    SELECT side_effect5 FROM DRUGS_FULL
)
WHERE side_effect IS NOT NULL;

COMMIT;

SELECT * FROM SIDEEFFECT;







-- Insert into Clinical Table --

INSERT INTO ClinicalTrial (
    clinical_trial_title,
    clinical_trial_start_date,
    clinical_trial_completion_date,
    clinical_trial_participants,
    clinical_trial_status,
    researcher_name,
    institute_name
)
SELECT DISTINCT
    clinical_trial_title,
    TO_DATE(clinical_trial_start_date, 'YYYY-MM-DD'),
    TO_DATE(clinical_trial_completion_date, 'YYYY-MM-DD'),
    TO_NUMBER(clinical_trial_participants),
    clinical_trial_status,
    clinical_trial_main_researcher,
    clinical_trial_institution

FROM DRUGS_FULL
WHERE clinical_trial_title IS NOT NULL;

COMMIT;

SELECT * FROM CLINICALTRIAL;



-- Insert into Condition Table --

INSERT INTO Condition (condition_name)
SELECT DISTINCT condition_name FROM (
    SELECT CLINICAL_TRIAL_CONDITION1 AS condition_name FROM DRUGS_FULL
    UNION
    SELECT CLINICAL_TRIAL_CONDITION2 FROM DRUGS_FULL
    UNION
    SELECT CLINICAL_TRIAL_CONDITION3 FROM DRUGS_FULL
)
WHERE condition_name IS NOT NULL;

COMMIT;

SELECT * FROM CONDITION;





-- Insert into Institution Table --

INSERT INTO Institution (institute_name, country, address)
SELECT DISTINCT clinical_trial_institution, clinical_trial_address1, CLINICAL_TRIAL_ADDRESS2
FROM DRUGS_FULL
WHERE clinical_trial_institution IS NOT NULL;

COMMIT;

SELECT * FROM INSTITUTION;







