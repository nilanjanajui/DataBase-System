
-- add primary DRUG --

ALTER TABLE Drug
ADD CONSTRAINT pk_drug PRIMARY KEY (drug_id);






-- add primary to DISEASE --

ALTER TABLE Disease
ADD CONSTRAINT pk_disease PRIMARY KEY (disease_name);






-- add primary key to PRODUCT --

ALTER TABLE Product
ADD CONSTRAINT pk_product PRIMARY KEY (product_id);





-- add foreign key to PRODUCT--
ALTER TABLE PRODUCT
ADD CONSTRAINT fk_product_drug FOREIGN KEY (drug_id)
REFERENCES DRUG(drug_id);





-- add primary key to SIDE_EFFECT --
ALTER TABLE SideEffect
ADD CONSTRAINT pk_side_effect PRIMARY KEY (side_effect_name);





-- add primary key to CLINICAL_TRIAL --
ALTER TABLE ClinicalTrial
ADD CONSTRAINT pk_title PRIMARY KEY (clinical_trial_title);






-- add primary key to CONDITION --
ALTER TABLE Condition
ADD CONSTRAINT pk_name PRIMARY KEY (condition_name);
