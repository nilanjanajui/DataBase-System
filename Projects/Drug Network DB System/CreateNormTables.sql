

-- DRUG Table --

CREATE TABLE DRUG AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY drug_name, drug_category) AS drug_id,
    drug_name,
    drug_category
FROM (
    SELECT DISTINCT drug_name, drug_category
    FROM DRUGS_FULL
    WHERE drug_name IS NOT NULL
) sub;




-- Disease table-- 

CREATE TABLE Disease (
    disease_name VARCHAR2(100),
    disease_category VARCHAR2(100)
);






-- Product table--

CREATE TABLE PRODUCT AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY product_name, company_name) AS product_id,
    product_name,
    company_name,
    drug_id
FROM (
    SELECT DISTINCT product_name, company_name, drug_id
    FROM DRUGS_FULL
    WHERE product_name IS NOT NULL AND company_name IS NOT NULL AND drug_id IS NOT NULL
) sub;





-- SideEffect Table-- 

CREATE TABLE SideEffect (
    side_effect_name VARCHAR2(200) 
);




-- Create clinical table --

CREATE TABLE ClinicalTrial (
    clinical_trial_title VARCHAR2(200),
    clinical_trial_start_date DATE,
    clinical_trial_completion_date DATE,
    clinical_trial_participants NUMBER,
    clinical_trial_status VARCHAR2(50),
    researcher_name VARCHAR2(200),
    institute_name VARCHAR2(200)
);






-- Condition Table --

CREATE TABLE Condition (
    condition_name VARCHAR2(100)
);



-- Institution Table --

CREATE TABLE Institution (

    institute_name VARCHAR2(200),
    country VARCHAR2(100),
    address VARCHAR2(200)
);





