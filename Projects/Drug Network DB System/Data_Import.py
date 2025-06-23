import pandas as pd
import oracledb

# Load CSV data
df = pd.read_csv('sampleInformation.csv')

# Add drug_id: generate unique ID for each drug_name
drug_id_map = {name: idx + 1 for idx, name in enumerate(df['drug_name'].unique())}
df['drug_id'] = df['drug_name'].map(drug_id_map)


country_id_map = {address: idx + 1 for idx, address in enumerate(df['clinical_trial_address1'].unique())}
df['country_id'] = df['clinical_trial_address1'].map(country_id_map)

product_id_map = {address: idx + 1 for idx, address in enumerate(df['product_name'].unique())}
df['product_id'] = df['product_name'].map(product_id_map)



# Define the expected columns — now including drug_id
columns = [
    'drug_id', 'drug_name', 'side_effect1', 'side_effect2', 'side_effect3', 'side_effect4', 'side_effect5',
    'interacts_with1', 'interacts_with2', 'interacts_with3',
    'disease_name', 'disease_category', 'drug_category', 'product_id', 'product_name', 'company_name',
    'clinical_trial_title', 'clinical_trial_start_date', 'clinical_trial_completion_date',
    'clinical_trial_participants', 'clinical_trial_status',
    'clinical_trial_condition1', 'clinical_trial_condition2', 'country_id', 'clinical_trial_address1',
    'clinical_trial_institution', 'clinical_trial_address2', 'clinical_trial_main_researcher',
    'clinical_trial_condition3'
]

# Select and clean the necessary columns
df = df[columns].fillna('').astype(str)

# Connect to Oracle
username = 'new'
password = '******'
dsn = 'localhost:1521/FREEPDB1'

connection = oracledb.connect(user=username, password=password, dsn=dsn)
cursor = connection.cursor()

# Read SQL INSERT statement
with open('insertFlatTableData.sql', 'r', encoding='utf-8') as file:
    insert_sql = file.read().strip()

# Insert each row
for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_sql, row)

# Finalize
connection.commit()
cursor.close()
connection.close()

print("CSV data inserted into DRUGS_FULL successfully with generated drug_id, product_id and country_id.")
