

-- Create TREAT relation --

CREATE TABLE Treats (
    drug_id NUMBER,
    disease_name VARCHAR2(100),

    -- Constraints
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    FOREIGN KEY (disease_name) REFERENCES Disease(disease_name)
);








-- Create HasSideEffect table -- 

CREATE TABLE HasSideEffect (
    drug_id NUMBER,
    side_effect_name VARCHAR2(200),
    
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    FOREIGN KEY (side_effect_name) REFERENCES SideEffect(side_effect_name)
);







-- Create TestedIn table --

CREATE TABLE TestedIn (
    drug_id NUMBER,
    clinical_trial_title VARCHAR2(200),

    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id),
    FOREIGN KEY (clinical_trial_title) REFERENCES ClinicalTrial(clinical_trial_title)
);





-- Create StudiedIn table --

CREATE TABLE Studies (
    clinical_trial_title VARCHAR2(200),
    condition_name VARCHAR2(100),

    FOREIGN KEY (clinical_trial_title) REFERENCES ClinicalTrial(clinical_trial_title),
    FOREIGN KEY (condition_name) REFERENCES Condition(condition_name)
);
