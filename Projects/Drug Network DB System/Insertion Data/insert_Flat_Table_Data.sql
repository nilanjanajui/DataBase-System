INSERT INTO DRUGS_FULL (
    drug_id,
    drug_name,
    side_effect1,
    side_effect2,
    side_effect3,
    side_effect4,
    side_effect5,
    interacts_with1,
    interacts_with2,
    interacts_with3,
    disease_name,
    disease_category,
    drug_category,
    product_id,
    product_name,
    company_name,
    clinical_trial_title,
    clinical_trial_start_date,
    clinical_trial_completion_date,
    clinical_trial_participants,
    clinical_trial_status,
    clinical_trial_condition1,
    clinical_trial_condition2,
    country_id,
    clinical_trial_address1,
    clinical_trial_institution,
    clinical_trial_address2,
    clinical_trial_main_researcher,
    clinical_trial_condition3
)
VALUES (
    :1, :2, :3, :4, :5, :6, :7,
    :8, :9, :10, :11, :12, :13, :14, :15,
    :16, :17, :18, :19, :20, :21, :22, :23,
    :24, :25, :26, :27, :28, :29
)


