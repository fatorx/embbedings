import pandas as pd
import re

# Read the CSV file into a DataFrame
df_original = pd.read_csv('EmpresasFormatCSV-Coroados.csv')

# Filter the dataframe to keep only the rows where the values in the `CNPJ` column are not equal to ",,CNPJ,,"
filtered_df = df_original[df_original['CNPJ'] != ",,CNPJ,,"].copy()

# Extracting required information
filtered_df['CNPJ'] = filtered_df['CNPJ'].astype(str).str.split('-').str[0]

# Define the functions to extract Razao Social and Endereco
def extract_razao_social(text):
    match = re.search(r'(.*)\n(.*)\n', text)
    return ' '.join(match.groups()) if match else None

def extract_endereco(text):
    endereco_match = re.search(r'AVENIDA.*(?!Cidade)', text)
    return endereco_match.group(0).strip() if endereco_match else None

# Apply the functions to create new columns
filtered_df['Razao Social'] = filtered_df['Unnamed: 1'].astype(str).apply(extract_razao_social)
filtered_df['Endereco'] = filtered_df['Unnamed: 1'].astype(str).apply(extract_endereco)

filtered_df['Telefone'] = filtered_df['Unnamed: 2'].astype(str).str.extract(r'(\(\d+\)[\s\S]*\d+)')
filtered_df['Regime'] = filtered_df['Unnamed: 1'].astype(str).str.extract('Regime Atual: (.*)')

# Create a new DataFrame with the extracted columns
new_df = filtered_df[['CNPJ', 'Razao Social', 'Endereco', 'Telefone', 'Regime']].copy()

# Save the new DataFrame to a CSV file with ';' as delimiter
new_df.to_csv('dados_filtrados_e_formatados_v2.csv', sep=';', index=False)

# Read the saved CSV file into a new DataFrame using ; as the separator
df_filtered_formatted = pd.read_csv('dados_filtrados_e_formatados_v2.csv', sep=';')

# Iterate through each column and remove the character '"'
for col in df_filtered_formatted.columns:
    df_filtered_formatted[col] = df_filtered_formatted[col].astype(str).str.replace('"', '', regex=False)

# Remove rows containing the string 'CNPJ;;;;'
df_filtered_formatted = df_filtered_formatted[df_filtered_formatted['CNPJ'] != 'CNPJ;;;;']

# Save the DataFrame to a new CSV file with ';' as the delimiter and without the index
df_filtered_formatted.to_csv('dados_filtrados_e_formatados_limpos_v2.csv', sep=';', index=False)

# Read the CSV file into a DataFrame using ; as the separator
df_filtered_formatted_limpos_v2 = pd.read_csv('dados_filtrados_e_formatados_limpos_v2.csv', sep=';')

# Display the first 5 rows
print(df_filtered_formatted_limpos_v2.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df_filtered_formatted_limpos_v2.info())

# Create a temporary column concatenating all columns
df_filtered_formatted_limpos_v2['all_columns'] = df_filtered_formatted_limpos_v2.astype(str).apply(';'.join, axis=1)

# Filter the dataframe to keep only the rows where the concatenated string is not equal to 'CNPJ;nan;nan;nan;nan'
df_filtered_formatted_limpos_v2 = df_filtered_formatted_limpos_v2[df_filtered_formatted_limpos_v2['all_columns'] != 'CNPJ;nan;nan;nan;nan']

# Drop the temporary column
df_filtered_formatted_limpos_v2.drop('all_columns', axis=1, inplace=True)

# Save the DataFrame to a new CSV file with ';' as the delimiter and without the index
df_filtered_formatted_limpos_v2.to_csv('dados_filtrados_e_formatados_limpos_final.csv', sep=';', index=False)