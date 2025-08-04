#  Drug Network DB System – Mini Project

A fully normalized relational database system designed from a raw Excel dataset involving drugs, diseases, clinical trials, and related metadata. This mini project demonstrates the end-to-end process of building a clean database schema using ER modeling, normalization theory, SQL implementation, and documentation.

---

## Project Overview

This project was designed to transform a messy and redundant clinical data spreadsheet into a structured, scalable, and query-efficient relational database. It involved ER modeling, dependency analysis, normalization proofs (up to BCNF), schema implementation in Oracle SQL, and sample query development.

---

## Key Features

- ✅ Designed an ER diagram with proper relationships (1:1, 1:N, M:N, recursive, weak entities)
- ✅ Normalized all relations to 3NF and BCNF with formal proofs
- ✅ Verified lossless decomposition & dependency preservation using attribute closures
- ✅ Implemented all schema and constraints (PK, FK) in Oracle SQL
- ✅ Created a procedural flowchart showing the full design process
- ✅ Developed complex queries for analysis (e.g. top side effects, common drugs, etc.)

---

## Folder Structure
```plaintext
📁 DrugNetworkDBSystem/

├── README.md                        ← Project description and documentation  
├── history.log                      ← Terminal or development log  

├── DataProcessing/                  ← Python and dataset
│   ├── newpython.py                 ← Data cleaning and ID mapping script  
│   └── sampleInformation.csv        ← Raw dataset (source for all tables)
│   └── schema2.sql                      ← Alternative or merged schema script

├── ER_Diagram/                      ← Entity-Relationship model
│   └── DRUGs ER Diagram.pdf         ← Final ER diagram  

├── TableCreation/                   ← SQL scripts for table creation  
│   ├── Create_Flat_Table.sql        ← Create original DRUGS_FULL table  
│   ├── CreateNormTables.sql         ← Create normalized entity tables  
│   ├── CreateRelationTable.sql      ← Create relationship tables  
│   └── pk_FK.sql                     ← Add Primary and Foreign Keys  

├── InsertionData/                   ← Data population scripts  
│   ├── insert_Flat_Table_Data.sql   ← Insert data into DRUGS_FULL  
│   ├── insert_Norm_Tables_data.sql  ← Insert into entity tables  
│   └── insert_Relation_tables_data.sql ← Insert into relation tables  

├── Queries/                         ← Analysis and assignment queries  
│   └── QuestionQueries.sql          ← Solutions to all assignment questions  

```

---

## Entity Tables

- Drug (drug_id, drug_name, drug_category)  
- Disease (disease_name, disease_category)  
- Product (product_id, product_name, company_name, drug_id)  
- ClinicalTrial (clinical_trial_title, start_date, completion_date, ...)  
- Institution (institute_name, address, country)  
- SideEffect (side_effect_name)  
- Condition (condition_name)

## Relation Tables

- Treats (drug_id, disease_name)  
- HasSideEffect (drug_id, side_effect_name)  
- TestedIn (drug_id, clinical_trial_title)  
- StudiedIn (clinical_trial_title, condition_name)  
- InteractsWith (drug_id, interacts_with_name)

## Documentation

- Functional Dependencies for all relations  
- Attribute Closure and Dependency Preservation proof  
- Lossless Decomposition validation  
- All tables verified to satisfy BCNF

## Tech Stack

- Oracle SQL  
- Python (for data preparation & ID mapping)  
- Draw.io (for ER diagrams)  
- LaTeX (for report and proofs)

##  Screenshots

Include:
- ER diagram  
- Flowchart  
- Table sample  
- Query output (e.g. drug_id with most trials)

## Author

Nilanjana Das Jui  
🎓 4th Semester, CSE, CU

## 📎 License

This is a mini academic project and is free for learning and reference. Please credit the author if reused.


