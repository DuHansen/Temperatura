import pandas as pd
import os

# Configurações
caminho_arquivos = 'C:/xampp/htdocs/TemperaturaGlobal/'
arquivos_csv = [
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2010_A_31-12-2010.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2011_A_31-12-2011.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2012_A_31-12-2012.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2013_A_31-12-2013.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2014_A_31-12-2014.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2015_A_31-12-2015.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2016_A_31-12-2016.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2017_A_31-12-2017.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2018_A_31-12-2018.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2019_A_31-12-2019.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2020_A_31-12-2020.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2021_A_31-12-2021.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2022_A_31-12-2022.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2023_A_31-12-2023.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2024_A_31-12-2024.CSV",
    "INMET_S_SC_A806_FLORIANOPOLIS_01-01-2025_A_31-05-2025.CSV"
]

def unificar_todos_dados(arquivos):
    df_unificado = pd.DataFrame()
    
    for arquivo in arquivos:
        caminho_completo = os.path.join(caminho_arquivos, arquivo)
        
        if not os.path.exists(caminho_completo):
            print(f"Arquivo não encontrado: {caminho_completo}")
            continue
            
        try:
            # Ler o arquivo CSV
            df = pd.read_csv(caminho_completo, 
                           delimiter=';', 
                           encoding='ISO-8859-1', 
                           skiprows=11,
                           header=0)
            
            # Verificar o número de colunas
            num_colunas = len(df.columns)
            print(f"\nProcessando {arquivo} - Colunas encontradas: {num_colunas}")
            
            # Nomes padrão das colunas (ajustados para 20 colunas)
            nomes_colunas = [
                'DATA', 'HORA', 'PRECIPITACAO_TOTAL', 'PRESSAO_ESTACAO',
                'PRESSAO_MAX', 'PRESSAO_MIN', 'RADIACAO_GLOBAL', 'TEMPERATURA_AR',
                'TEMPERATURA_ORVALHO', 'TEMPERATURA_MAX', 'TEMPERATURA_MIN',
                'TEMPERATURA_ORVALHO_MAX', 'TEMPERATURA_ORVALHO_MIN',
                'UMIDADE_MAX', 'UMIDADE_MIN', 'UMIDADE_RELATIVA',
                'VENTO_DIRECAO', 'VENTO_RAJADA_MAX', 'VENTO_VELOCIDADE',
                'COLUNA_EXTRA'  # Para a 20ª coluna
            ]
            
            # Ajustar nomes conforme número de colunas
            if num_colunas == 19:
                nomes_colunas = nomes_colunas[:19]
            elif num_colunas == 20:
                pass  # Usa todos os 20 nomes
            else:
                print(f"Número inesperado de colunas: {num_colunas}")
                continue
                
            df.columns = nomes_colunas
            
            # Converter valores numéricos
            colunas_numericas = df.columns[2:]  # Todas exceto DATA e HORA
            for col in colunas_numericas:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
            
            # Adicionar ao DataFrame unificado
            df_unificado = pd.concat([df_unificado, df], ignore_index=True)
            
            print(f"Arquivo {arquivo} processado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")
            print("Colunas encontradas:", len(df.columns) if 'df' in locals() else "N/A")
    
    return df_unificado

# Processar os arquivos
df_final = unificar_todos_dados(arquivos_csv)

# Resultados e salvamento
if not df_final.empty:
    print("\nDados unificados com sucesso!")
    print(f"Total de registros: {len(df_final)}")
    print("\nEstrutura dos dados:")
    print(df_final.info())
    
    # Salvar arquivo
    nome_arquivo_saida = 'dados_meteorologicos_completos.csv'
    df_final.to_csv(nome_arquivo_saida, index=False, sep=';')
    print(f"\nArquivo salvo como '{nome_arquivo_saida}'")
else:
    print("Nenhum dado foi processado. Verifique os erros acima.")