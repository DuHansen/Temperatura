import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from datetime import datetime
from textwrap import wrap

# Configurações iniciais
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

# Dados de entrada
FONTE_DADOS = "https://bdmep.inmet.gov.br/"
ESTACAO = "Florianópolis/SC (A806)"
PERIODO = "2010-2025"
AUTOR = "Eduardo Hansen, Gabriel Laufer, Mateus Soster e Wesley"
DATA_RELATORIO = datetime.now().strftime("%d/%m/%Y")

# Carregar dados
df = pd.read_csv('dados_meteorologicos_completos.csv', sep=';')
df['DATA'] = pd.to_datetime(df['DATA'], format='%Y/%m/%d', errors='coerce')
df['ANO'] = df['DATA'].dt.year
df['MES'] = df['DATA'].dt.month
df['MES_ANO'] = df['DATA'].dt.to_period('M')

# Função para criar páginas de texto
def add_text_page(pdf, title, paragraphs, figsize=(11, 8)):
    plt.figure(figsize=figsize)
    plt.text(0.1, 0.9, title, fontsize=16, weight='bold')
    
    y_pos = 0.8
    for para in paragraphs:
        wrapped_text = wrap(para, width=120)
        for line in wrapped_text:
            plt.text(0.1, y_pos, line, fontsize=12, ha='left')
            y_pos -= 0.05
        y_pos -= 0.05  # Espaço entre parágrafos
    
    plt.axis('off')
    pdf.savefig()
    plt.close()

# Criar PDF
with PdfPages('artigo_meteorologico_completo.pdf') as pdf:
    
    # CAPA
    plt.figure(figsize=(11, 8))
    plt.text(0.5, 0.7, "ANÁLISE METEOROLÓGICA COMPLETA", fontsize=20, weight='bold', ha='center')
    plt.text(0.5, 0.6, f"Dados da Estação: {ESTACAO}", fontsize=16, ha='center')
    plt.text(0.5, 0.5, f"Período: {PERIODO}", fontsize=16, ha='center')
    plt.text(0.5, 0.4, f"Fonte: {FONTE_DADOS}", fontsize=14, ha='center')
    plt.text(0.5, 0.3, f"Autor: {AUTOR}", fontsize=14, ha='center')
    plt.text(0.5, 0.2, f"Data: {DATA_RELATORIO}", fontsize=14, ha='center')
    plt.axis('off')
    pdf.savefig()
    plt.close()

    # RESUMO
    abstract_text = [
        "Este relatório apresenta uma análise detalhada dos dados meteorológicos coletados na estação ",
        f"{ESTACAO} no período de {PERIODO}. Foram analisadas as tendências de temperatura, vento, umidade ",
        "e pressão atmosférica, com ênfase na identificação de padrões sazonais e variações anuais. "
    ]
    add_text_page(pdf, "Resumo", abstract_text)

    # 1. INTRODUÇÃO
    intro_text = [
        "A análise de dados meteorológicos históricos é fundamental para compreender as mudanças ",
        "climáticas e seus impactos locais. Este estudo foca na estação meteorológica de ",
        f"{ESTACAO}, operada pelo INMET, com dados disponíveis publicamente em {FONTE_DADOS}.",
        "",
        "O objetivo principal desta análise é identificar tendências temporais nas variáveis ",
        "meteorológicas básicas, incluindo temperatura do ar, precipitação, velocidade do vento, ",
        "umidade relativa e pressão atmosférica. A análise abrange tanto variações sazonais ",
        "quanto tendências de longo prazo.",
        ""
    ]
    add_text_page(pdf, "1. Introdução", intro_text)

    # 2. METODOLOGIA
    metodologia_text = [
        "Os dados foram obtidos através do Banco de Dados Meteorológicos para Ensino e Pesquisa ",
        f"(BDMEP) do INMET, disponível em {FONTE_DADOS}. A estação selecionada ({ESTACAO}) ",
        "apresenta dados horários desde 2010 até o presente.",
        "",
        "Foram utilizadas as seguintes variáveis para análise:",
        "- Temperatura do Ar (°C)",
        "- Precipitação Total (mm)",
        "- Velocidade do Vento (m/s)",
        "- Rajada Máxima (m/s)",
        "- Umidade Relativa (%)",
        "- Pressão Atmosférica (mB)",
        ""
    ]
    add_text_page(pdf, "2. Metodologia", metodologia_text)

    # 3. RESULTADOS - TEMPERATURA
    plt.figure(figsize=(11, 8))

    # Tabela de Temperaturas Mínimas e Máximas por Ano
    temp_ano_max_min = df.groupby('ANO')['TEMPERATURA_AR'].agg(['min', 'max'])
    add_text_page(pdf, "Temperaturas Mínimas e Máximas por Ano", 
                  [f"A tabela abaixo mostra as temperaturas mínimas e máximas por ano:"] + 
                  [str(temp_ano_max_min)])

    # 1. Detecção de Eventos de Alta Temperatura
    temp_alta = df[df['TEMPERATURA_AR'] > 35]  # Considerando temperatura acima de 35°C como alta
    plt.plot(temp_alta['DATA'], temp_alta['TEMPERATURA_AR'], marker='o', color='red', label="Eventos de Alta Temperatura")
    plt.title("Eventos de Alta Temperatura (> 35°C)", pad=20)
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.legend()

    # Adicionar valores acima dos pontos
    for i, txt in enumerate(temp_alta['TEMPERATURA_AR']):
        plt.annotate(f'{txt:.2f}', (temp_alta['DATA'].iloc[i], temp_alta['TEMPERATURA_AR'].iloc[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center')

    pdf.savefig()
    plt.close()

    # 2. Gráfico de Colunas de Temperatura Média por Ano
    temp_ano = df.groupby('ANO')['TEMPERATURA_AR'].mean()  # Temperatura média por ano
    plt.bar(temp_ano.index, temp_ano.values, color='skyblue')
    plt.title("Temperatura Média Anual", pad=20)
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Média (°C)')
    
    # Adicionar valores sobre as colunas
    for i, txt in enumerate(temp_ano.values):
        plt.text(temp_ano.index[i], txt + 0.1, f'{txt:.2f}', ha='center', color='black')

    pdf.savefig()
    plt.close()

    # 3. Análise de Vento: Direção e Intensidade
    vento_dir = df.groupby('ANO')['VENTO_DIRECAO'].mean()  # Direção média do vento por ano
    vento_vel = df.groupby('ANO')['VENTO_VELOCIDADE'].mean()  # Velocidade média do vento por ano
    plt.figure(figsize=(11, 8))

    # Gráfico para Velocidade do Vento
    plt.subplot(2, 1, 1)
    plt.plot(vento_vel.index, vento_vel.values, marker='o', color='blue', label="Velocidade do Vento")
    plt.title("Velocidade do Vento Média Anual", pad=20)
    plt.xlabel('Ano')
    plt.ylabel('Velocidade (m/s)')
    plt.grid(True)
    plt.legend()

    # Adicionar valores acima dos pontos de velocidade
    for i, txt in enumerate(vento_vel.values):
        plt.annotate(f'{txt:.2f}', (vento_vel.index[i], vento_vel.values[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center')

    # Gráfico para Direção Média do Vento
    plt.subplot(2, 1, 2)
    plt.plot(vento_dir.index, vento_dir.values, marker='x', color='orange', label="Direção Média do Vento")
    plt.title("Direção Média do Vento Anual", pad=20)
    plt.xlabel('Ano')
    plt.ylabel('Direção (°)')
    plt.grid(True)
    plt.legend()

    # Adicionar valores acima dos pontos de direção
    for i, txt in enumerate(vento_dir.values):
        plt.annotate(f'{txt:.2f}', (vento_dir.index[i], vento_dir.values[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center')

    plt.tight_layout()
    pdf.savefig()
    plt.close()

    # 5. DISCUSSÃO
    discussao_text = [
        "Os resultados apresentados demonstram padrões interessantes nas variáveis meteorológicas ",
        "analisadas para a estação {ESTACAO}. A tendência de aumento de temperatura observada...",
        "Quanto aos ventos, a variação observada...",
        "A umidade relativa e pressão atmosférica apresentaram...",
    ]
    add_text_page(pdf, "6. Discussão", discussao_text)

    # 6. CONCLUSÃO
    conclusao_text = [
        "Esta análise abrangente dos dados meteorológicos de 2010 a 2025 para a estação de {ESTACAO} revelou várias tendências importantes...",
    ]
    add_text_page(pdf, "7. Conclusão", conclusao_text)

    # 7. REFERÊNCIAS
    referencias_text = [
        "INSTITUTO NACIONAL DE METEOROLOGIA (INMET). Banco de Dados Meteorológicos para Ensino e Pesquisa...",
    ]
    add_text_page(pdf, "8. Referências", referencias_text)

print("Artigo completo gerado com sucesso: 'artigo_meteorologico_completo.pdf'")
