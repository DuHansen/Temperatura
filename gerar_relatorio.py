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

   # 1. Detecção de Eventos de Alta Temperatura
    temp_alta = df[df['TEMPERATURA_AR'] > 35]  # Considerando temperatura acima de 35°C como alta
    plt.figure(figsize=(11, 8))
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

    # 2. Análise de Vento: Direção e Intensidade
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

    # 3. Correlação entre Temperatura e Umidade Relativa
    plt.figure(figsize=(11, 8))
    plt.scatter(df['TEMPERATURA_AR'], df['UMIDADE_RELATIVA'], color='green', alpha=0.5)
    plt.title("Correlação entre Temperatura e Umidade Relativa", pad=20)
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Umidade Relativa (%)')
    plt.grid(True)

    # Adicionar valores nas coordenadas dos pontos
    for i in range(len(df)):
        plt.annotate(f'({df["TEMPERATURA_AR"].iloc[i]:.2f}, {df["UMIDADE_RELATIVA"].iloc[i]:.2f})',
                    (df['TEMPERATURA_AR'].iloc[i], df['UMIDADE_RELATIVA'].iloc[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8)

    pdf.savefig()
    plt.close()

    # 4. RESULTADOS - TENDÊNCIAS E SAZONALIDADE
    plt.figure(figsize=(11, 8))

    # 4.1 Tendência de Temperatura e Umidade Relativa
    temp_ano = df.groupby('ANO')['TEMPERATURA_AR'].mean()
    umidade_ano = df.groupby('ANO')['UMIDADE_RELATIVA'].mean()

    # Salvar a inclinação da tendência para a discussão
    z_temp = np.polyfit(temp_ano.index, temp_ano.values, 1)
    z_umidade = np.polyfit(umidade_ano.index, umidade_ano.values, 1)

    plt.subplot(2, 1, 1)
    plt.plot(temp_ano.index, temp_ano.values, marker='o', color='red', label="Temperatura Média Anual")
    plt.plot(temp_ano.index, np.polyval(z_temp, temp_ano.index), color='black', linestyle='--', label="Tendência Temperatura")
    plt.plot(umidade_ano.index, umidade_ano.values, marker='x', color='blue', label="Umidade Relativa Média Anual")
    plt.plot(umidade_ano.index, np.polyval(z_umidade, umidade_ano.index), color='black', linestyle='--', label="Tendência Umidade Relativa")
    plt.title("Tendência de Temperatura e Umidade Relativa (2010-2025)", pad=20)
    plt.xlabel('Ano')
    plt.ylabel('Valor Médio')
    plt.grid(True)
    plt.legend()

    # Adicionar valores nos pontos de temperatura e umidade
    for i, txt in enumerate(temp_ano.values):
        plt.annotate(f'{txt:.2f}', (temp_ano.index[i], temp_ano.values[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center')
    for i, txt in enumerate(umidade_ano.values):
        plt.annotate(f'{txt:.2f}', (umidade_ano.index[i], umidade_ano.values[i]),
                    textcoords="offset points", xytext=(0, 10), ha='center')

    # 4.2 Análise Sazonal e Tendências Temporais
    temp_mensal = df.groupby('MES')['TEMPERATURA_AR'].mean()
    precip_mensal = df.groupby('MES')['PRECIPITACAO_TOTAL'].sum()

    plt.subplot(2, 1, 2)
    plt.plot(temp_mensal.index, temp_mensal.values, marker='o', color='orange', label="Temperatura Média Mensal")
    plt.bar(precip_mensal.index, precip_mensal.values, color='lightblue', alpha=0.6, label="Precipitação Total Mensal")
    plt.title("Análise Sazonal de Temperatura e Precipitação", pad=20)
    plt.xlabel('Mês')
    plt.ylabel('Valor Médio / Total')
    plt.grid(True)
    plt.legend()

    # Adicionar valores nas colunas de precipitação
    for i in range(len(precip_mensal)):
        plt.text(precip_mensal.index[i], precip_mensal.values[i] + 0.5, f'{precip_mensal.values[i]:.2f}',
                ha='center', fontsize=10, color='black')

    plt.tight_layout()
    pdf.savefig()
    plt.close()


    # 5. DISCUSSÃO
    discussao_text = [
        f"Os resultados apresentados demonstram padrões interessantes nas variáveis meteorológicas ",
        f"analisadas para a estação {ESTACAO}. A tendência de aumento de temperatura observada ",
        f"({z_temp[0]:.3f}°C/ano) está em concordância com... [complete com comparações]",
        "",
        f"Quanto aos ventos, a variação observada... [discuta os resultados]",
        "",
        "A umidade relativa e pressão atmosférica apresentaram... [discuta os resultados]",
        "",
        "Estes resultados são consistentes/com diferem de estudos anteriores como... [cite estudos]"
    ]
    add_text_page(pdf, "6. Discussão", discussao_text)

    # 6. CONCLUSÃO
    conclusao_text = [
        "Esta análise abrangente dos dados meteorológicos de 2010 a 2025 para a estação de ",
        f"{ESTACAO} revelou várias tendências importantes:",
        "",
        "1. [Liste as principais conclusões sobre temperatura]",
        "2. [Conclusões sobre ventos]",
        "3. [Conclusões sobre umidade e pressão]",
        "",
        "Estes resultados têm implicações importantes para... [discuta implicações]",
        "",
        "Como trabalhos futuros, sugere-se... [indique possíveis extensões do estudo]"
    ]
    add_text_page(pdf, "7. Conclusão", conclusao_text)

    # 7. REFERÊNCIAS
    referencias_text = [
        "INSTITUTO NACIONAL DE METEOROLOGIA (INMET). Banco de Dados Meteorológicos para Ensino e ",
        f"Pesquisa (BDMEP). Disponível em: {FONTE_DADOS}. Acesso em: {DATA_RELATORIO}.",
        "",
        "IPCC. Climate Change 2021: The Physical Science Basis. Contribution of Working Group I to ",
        "the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge ",
        "University Press, 2021.",
        "",
        "MAIA, J. D. et al. Análise de tendências climáticas no Brasil. Revista Brasileira de ",
        "Meteorologia, v. 30, n. 3, p. 423-434, 2015.",
        "",
        "WMO. Guide to Meteorological Instruments and Methods of Observation. WMO-No. 8, 2018.",
        "",
        "Para citação deste relatório:",
        f"{AUTOR}. Análise Meteorológica Completa: Estação {ESTACAO} {PERIODO}. {DATA_RELATORIO}."
    ]
    add_text_page(pdf, "8. Referências", referencias_text)

print("Artigo completo gerado com sucesso: 'artigo_meteorologico_completo.pdf'")
