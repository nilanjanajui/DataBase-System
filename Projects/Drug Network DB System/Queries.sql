
-- a) Find the number of drugs that have nausea as a side effect

SELECT COUNT(DISTINCT drug_id) AS num_drugs
FROM HasSideEffect
WHERE side_effect_name = 'nausea';




-- b) Find the drugs that interact with butabarbital

SELECT DISTINCT drug_name
FROM DRUGS_FULL
WHERE interacts_with1 = 'butabarbital'
   OR interacts_with2 = 'butabarbital'
   OR interacts_with3 = 'butabarbital';






-- c) Find the drugs with side effects cough and headache

SELECT d.drug_id, d.drug_name
FROM HasSideEffect hs
JOIN Drug d ON hs.drug_id = d.drug_id
WHERE hs.side_effect_name IN ('cough', 'headache')
GROUP BY d.drug_id, d.drug_name
HAVING COUNT(DISTINCT hs.side_effect_name) = 2;




-- d) Find the drugs that can be used to treat endocrine diseases

SELECT DISTINCT d.drug_name, d.drug_id
FROM Treats t
JOIN Disease dis ON t.disease_name = dis.disease_name
JOIN Drug d ON t.drug_id = d.drug_id
WHERE LOWER(dis.disease_category) = 'endocrine';






-- e) Find the most common treatment for immunological diseases that have not been used for hematological diseases

SELECT t.drug_id, d.drug_name, COUNT(*) AS usage_count
FROM Treats t
JOIN Disease dis ON t.disease_name = dis.disease_name
JOIN Drug d ON t.drug_id = d.drug_id
WHERE LOWER(dis.disease_category) = 'immunological'
  AND NOT EXISTS (
    SELECT 1
    FROM Treats t2
    JOIN Disease d2 ON t2.disease_name = d2.disease_name
    WHERE LOWER(d2.disease_category) = 'hematological'
      AND t2.drug_id = t.drug_id
)
GROUP BY t.drug_id, d.drug_name
ORDER BY usage_count DESC;




-- f) Find the diseases that can be treated with hydrocortisone but not with etanercept

SELECT DISTINCT t1.disease_name
FROM Treats t1
JOIN Drug d1 ON t1.drug_id = d1.drug_id
WHERE LOWER(d1.drug_name) = 'hydrocortisone'
  AND NOT EXISTS (
    SELECT 1
    FROM Treats t2
    JOIN Drug d2 ON t2.drug_id = d2.drug_id
    WHERE LOWER(d2.drug_name) = 'etanercept'
      AND t2.disease_name = t1.disease_name
);






-- g) Find the top-10 side effects that drugs used to treat asthma related diseases have

SELECT hs.side_effect_name, COUNT(*) AS frequency
FROM Treats t
JOIN Disease d ON t.disease_name = d.disease_name
JOIN HasSideEffect hs ON t.drug_id = hs.drug_id
WHERE LOWER(d.disease_name) LIKE '%asthma%'
GROUP BY hs.side_effect_name
ORDER BY frequency DESC;




-- h) Find the drugs that have been studied in more than three clinical trials with more than 30 participants

SELECT d.drug_name
FROM TestedIn ti
JOIN ClinicalTrial ct ON ti.clinical_trial_title = ct.clinical_trial_title
JOIN Drug d ON ti.drug_id = d.drug_id
WHERE ct.clinical_trial_participants > 30
GROUP BY d.drug_id, d.drug_name
HAVING COUNT(DISTINCT ti.clinical_trial_title) > 3;




-- i) Find the largest number of clinical trials and the drugs they have studied that have been active in the same period of time

WITH TrialActivity AS (
  SELECT 
    TRUNC(clinical_trial_start_date + LEVEL - 1) AS active_day,
    clinical_trial_title
  FROM ClinicalTrial
  CONNECT BY LEVEL <= clinical_trial_completion_date - clinical_trial_start_date + 1
    AND PRIOR clinical_trial_title = clinical_trial_title
    AND PRIOR DBMS_RANDOM.VALUE IS NOT NULL
),
PeakDate AS (
  SELECT active_day, COUNT(*) AS trial_count
  FROM TrialActivity
  GROUP BY active_day
  ORDER BY trial_count DESC
  FETCH FIRST 1 ROW ONLY
),
PeakTrials AS (
  SELECT ta.clinical_trial_title
  FROM TrialActivity ta
  JOIN PeakDate pd ON ta.active_day = pd.active_day
),
DrugsInPeakTrials AS (
  SELECT DISTINCT d.drug_name, pt.clinical_trial_title
  FROM PeakTrials pt
  JOIN TestedIn ti ON pt.clinical_trial_title = ti.clinical_trial_title
  JOIN Drug d ON d.drug_id = ti.drug_id
)
SELECT * FROM DrugsInPeakTrials;




-- j) Find the main researchers that have conducted clinical trials that study drugs that can be 
--    used to treat both respiratory and cardiovascular diseases

WITH DualCategoryDrugs AS (
  SELECT t.drug_id
  FROM Treats t
  JOIN Disease d ON t.disease_name = d.disease_name
  WHERE LOWER(d.disease_category) IN ('respiratory', 'cardiovascular')
  GROUP BY t.drug_id
  HAVING COUNT(DISTINCT LOWER(d.disease_category)) = 2
),
RelevantTrials AS (
  SELECT DISTINCT ti.clinical_trial_title
  FROM TestedIn ti
  JOIN DualCategoryDrugs dc ON ti.drug_id = dc.drug_id
)
SELECT DISTINCT ct.researcher_name
FROM ClinicalTrial ct
JOIN RelevantTrials rt ON ct.clinical_trial_title = rt.clinical_trial_title
WHERE ct.researcher_name IS NOT NULL;






-- k) Find up to three main researchers that have conductd the larger number of clinical trials
--    that study drugs that can be used to treat both respiratory and cardiovascular diseases

WITH DualCategoryDrugs AS (
  SELECT t.drug_id
  FROM Treats t
  JOIN Disease d ON t.disease_name = d.disease_name
  WHERE LOWER(d.disease_category) IN ('respiratory', 'cardiovascular')
  GROUP BY t.drug_id
  HAVING COUNT(DISTINCT LOWER(d.disease_category)) = 2
),
RelevantTrials AS (
  SELECT DISTINCT ti.clinical_trial_title
  FROM TestedIn ti
  JOIN DualCategoryDrugs dc ON ti.drug_id = dc.drug_id
),
ResearcherCounts AS (
  SELECT ct.researcher_name, COUNT(*) AS trial_count
  FROM ClinicalTrial ct
  JOIN RelevantTrials rt ON ct.clinical_trial_title = rt.clinical_trial_title
  WHERE ct.researcher_name IS NOT NULL
  GROUP BY ct.researcher_name
)
SELECT *
FROM ResearcherCounts
ORDER BY trial_count DESC;




-- l) Find the categories of drugs that have been only studied in clinical trials based in United States

SELECT d.drug_category
FROM Drug d
JOIN TestedIn ti ON d.drug_id = ti.drug_id
JOIN ClinicalTrial ct ON ti.clinical_trial_title = ct.clinical_trial_title
JOIN Institution i ON ct.institute_name = i.institute_name
GROUP BY d.drug_category
HAVING COUNT(*) = SUM(
  CASE
    WHEN LOWER(i.country) = 'united states' THEN 1
    ELSE 0
  END
);
