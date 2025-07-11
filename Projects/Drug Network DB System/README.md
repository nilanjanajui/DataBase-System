# 🧬 Structured Drug Database – Mini Project

A fully normalized relational database system designed from a raw Excel dataset involving drugs, diseases, clinical trials, and related metadata. This mini project demonstrates the end-to-end process of building a clean database schema using ER modeling, normalization theory, SQL implementation, and documentation.

## 📌 Project Overview

This project was designed to transform a messy and redundant clinical data spreadsheet into a structured, scalable, and query-efficient relational database. It involved ER modeling, dependency analysis, normalization proofs (up to BCNF), schema implementation in Oracle SQL, and sample query development.

## 🎯 Key Features

- ✅ Designed an ER diagram with proper relationships (1:1, 1:N, M:N, recursive, weak entities)
- ✅ Normalized all relations to 3NF and BCNF with formal proofs
- ✅ Verified lossless decomposition & dependency preservation using attribute closures
- ✅ Implemented all schema and constraints (PK, FK) in Oracle SQL
- ✅ Created a procedural flowchart showing the full design process
- ✅ Developed complex queries for analysis (e.g. top side effects, common drugs, etc.)

## 📁 Folder Structure
---
├── ER-Diagrams/ → PDF & PNG versions of ER Diagram and Procedure Flowchart
├── SQL/ → All SQL schema creation & queries
│ ├── create_tables.sql
│ ├── insert_data.sql
│ └── queries.sql
├── Python/ → Data preprocessing script
│ └── data_preprocessing.py
├── Report/ → Normalization proofs, FD analysis, LaTeX documentation
│ └── DB_Report.pdf
└── Screenshots/ → Sample query outputs & schema previews
---


## 📘 Entity Tables

- Drug (drug_id, drug_name, drug_category)  
- Disease (disease_name, disease_category)  
- Product (product_id, product_name, company_name, drug_id)  
- ClinicalTrial (clinical_trial_title, start_date, completion_date, ...)  
- Institution (institute_name, address, country)  
- SideEffect (side_effect_name)  
- Condition (condition_name)

## 🔗 Relation Tables

- Treats (drug_id, disease_name)  
- HasSideEffect (drug_id, side_effect_name)  
- TestedIn (drug_id, clinical_trial_title)  
- StudiedIn (clinical_trial_title, condition_name)  
- InteractsWith (drug_id, interacts_with_name)

## 📚 Documentation

- Functional Dependencies for all relations  
- Attribute Closure and Dependency Preservation proof  
- Lossless Decomposition validation  
- All tables verified to satisfy BCNF

## 🛠 Tech Stack

- Oracle SQL  
- Python (for data preparation & ID mapping)  
- Draw.io (for ER diagrams)  
- LaTeX (for report and proofs)

## 📸 Screenshots

Include:
- ER diagram  
- Flowchart  
- Table sample  
- Query output (e.g. drug_id with most trials)

## 📬 Author

Nilanjana Das Jui  
🎓 4th Semester, CSE, CU

## 📎 License

This is a mini academic project and is free for learning and reference. Please credit the author if reused.


