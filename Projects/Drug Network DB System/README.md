# 🧬 Drug Network DB System

A relational database design project that models the relationships between drugs, diseases, clinical trials, researchers, institutions, and more — using real-world-inspired medical data.

> ✅ Designed using ER modeling principles  
> ✅ Fully normalized schema  
> ✅ SQL queries built to answer real clinical insights  
> ✅ Powered by Oracle SQL & Python (data import)

---

## 📁 Project Structure
```
📦 Drug Network DB System/
├── 📊 sampleInformation.xlsx # Raw dataset with drug, disease, trial info
├── 🐍 data_import.py # Python script to preprocess & insert data
├── 📄 schema.sql # SQL DDL statements for tables & relations
├── 📄 queries.sql # Answers to 12+ medical data questions
├── 📄 er_diagram.drawio.pdf # Chen-style ER diagram
```
---


---

## 🧠 What This Project Does

This database schema allows users to:

- Track drugs and their side effects
- Link drugs to diseases they treat
- Trace clinical trials and their associated researchers & institutions
- Analyze research trends (e.g., “top researchers in respiratory & cardiovascular trials”)
- Normalize messy data into clean SQL-ready structures

---

## 🗂️ Schema Overview

**Entities:**
- `Drug(drug_name, drug_category)`
- `Disease(disease_name, disease_category)`
- `SideEffect(side_effect_name)`
- `Product(product_name, company_name)`
- `Institution(institute_name, address, country)`
- `ClinicalTrial(title, start_date, status, participants, etc.)`

**Relations:**
- `Treats`: connects `Drug` and `Disease`
- `HasSideEffect`: maps `Drug` to `SideEffect`
- `TestedIn`: maps `Drug` to `ClinicalTrial`
- `StudiedIn`: trial conditions


📝 Primary and foreign keys are thoughtfully designed based on real-world uniqueness — no unnecessary synthetic IDs.

---

## 🧪 Sample Queries Answered

This schema can solve questions like:

✅ Find drugs that treat both respiratory and cardiovascular diseases  
✅ List researchers who led trials on those drugs  
✅ What are the top side effects of asthma treatments?  
✅ Which drug categories have only been studied in U.S.-based trials?

See `Queries.sql` for all answers!

---

## ⚙️ Technologies Used

- Oracle SQL (DDL + complex joins)
- IDE (VS Code)
- Python (pandas + oracledb for data insertion)
- Excel / CSV (data preprocessing)
- draw.io (ER diagramming)

---

## 🏁 How to Run

1. Load `schema.sql` into Oracle LiveSQL or your own Oracle DB  
2. Use `data_import.py` to populate tables from `sampleInformation.csv`  
3. Run queries from `queries.sql` to get insights  
4. Optional: visualize schema with `er_diagram.drawio.pdf`

---

## 📚 Learning Outcomes

- Real-world data modeling using ER principles  
- Handling multivalued and many-to-many attributes  
- Designing for clarity, queryability, and data integrity  
- Using JOINs and groupings to extract complex insights from normalized tables

---

## Author

**Nilanjana Das Jui**  
4th Semester, CSE, CU 

















