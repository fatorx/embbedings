import pandas as pd

# Read the CSV file into a DataFrame, trying 'utf-8' first and then 'latin-1' if it fails
try:
    df = pd.read_csv('EmpresasFormatCSV - Faturamento.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('EmpresasFormatCSV - Faturamento.csv', encoding='latin-1')

# Filter the dataframe to keep only the rows where the values in the `CNPJ` column are not equal to ",,CNPJ,,"
filtered_df = df[df['CNPJ'] != ",,CNPJ,,"].copy()

# Write the filtered dataframe to a new CSV file
filtered_df.to_csv('empresas_filtradas.csv', index=False, encoding='utf-8')

# Print a success message
print("Arquivo 'empresas_filtradas.csv' criado com sucesso!")
