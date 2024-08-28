import pdfplumber
import csv

def extract_data_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:  # Ignorando a linha de cabeçalho
                    data.append(row[:-1])  # Ignorando a última coluna ("Dívidas?")

    return data

def write_to_csv(data, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CNPJ", "Dados da Empresa", "Telefone e E-mail"])  # Cabeçalho
        writer.writerows(data)

if __name__ == "__main__":
    pdf_path = 'cubatao.pdf'  # Substitua pelo caminho para o arquivo PDF
    csv_path = 'cubatao.csv'  # Substitua pelo caminho onde deseja salvar o CSV
    
    data = extract_data_from_pdf(pdf_path)
    write_to_csv(data, csv_path)

    print(f"Dados extraídos e salvos em {csv_path}")



