import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configurações iniciais
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 14

def create_output_dir(directory: str) -> None:
    """Cria o diretório de saída se não existir"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_and_process_data(file_path: str) -> pd.DataFrame:
    """Carrega e processa os dados do arquivo Excel"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Erro: Arquivo '{file_path}' não encontrado.") from e
    
    # Verificar colunas necessárias
    required_columns = [
        'TEMPERATURA_MAX', 'TEMPERATURA_MIN', 'DATA',
        'PRECIPITACAO_TOTAL', 'PRESSAO_ESTACAO', 'RADIACAO_GLOBAL',
        'TEMPERATURA_AR', 'UMIDADE_RELATIVA', 'VENTO_VELOCIDADE'
    ]
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Erro: Colunas necessárias não encontradas: {missing_cols}")

    # Processamento de dados
    df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
    df = df.dropna(subset=['DATA'])
    df['ANO'] = df['DATA'].dt.year

    # Converter e tratar colunas numéricas
    numeric_cols = [
        'TEMPERATURA_MAX', 'TEMPERATURA_MIN', 'PRECIPITACAO_TOTAL',
        'PRESSAO_ESTACAO', 'RADIACAO_GLOBAL', 'TEMPERATURA_AR',
        'UMIDADE_RELATIVA', 'VENTO_VELOCIDADE'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].replace(-9999.0, np.nan).fillna(df[col].median())

    return df

def calculate_daily_average(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a média diária entre TEMPERATURA_MAX e TEMPERATURA_MIN"""
    df['MEDIA_DIARIA'] = df[['TEMPERATURA_MAX', 'TEMPERATURA_MIN']].mean(axis=1)
    return df

def calculate_annual_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula estatísticas anuais"""
    stats = df.groupby('ANO').agg({
        'MEDIA_DIARIA': 'median',
        'TEMPERATURA_MAX': 'max',
        'TEMPERATURA_MIN': 'min'
    }).reset_index()
    
    stats.columns = ['Ano', 'Mediana Temperatura (°C)', 'Temperatura Máxima (°C)', 'Temperatura Mínima (°C)']
    return stats

def save_plot(fig, output_dir: str, filename: str) -> None:
    """Salva uma figura no diretório de saída"""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)

def create_temperature_table(stats: pd.DataFrame, output_dir: str) -> None:
    """Cria e salva uma tabela com as estatísticas de temperatura"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    cell_text = []
    for _, row in stats.iterrows():
        cell_text.append([
            row['Ano'],
            f"{row['Mediana Temperatura (°C)']:.1f}",
            f"{row['Temperatura Máxima (°C)']:.1f}",
            f"{row['Temperatura Mínima (°C)']:.1f}"
        ])
    
    table = ax.table(
        cellText=cell_text,
        colLabels=stats.columns,
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    plt.title('Estatísticas de Temperatura por Ano', pad=20)
    save_plot(fig, output_dir, 'tabela_temperaturas.png')

def plot_temperature_trend(stats: pd.DataFrame, output_dir: str) -> None:
    """Cria e salva um gráfico de tendência de temperatura"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(stats['Ano'], stats['Mediana Temperatura (°C)'], 
            marker='o', color='red', label='Mediana', linewidth=2)
    ax.plot(stats['Ano'], stats['Temperatura Máxima (°C)'], 
            marker='^', color='darkred', label='Máxima', linestyle='--')
    ax.plot(stats['Ano'], stats['Temperatura Mínima (°C)'], 
            marker='v', color='blue', label='Mínima', linestyle='-.')
    
    ax.set_title('Tendência de Temperatura por Ano', fontsize=16)
    ax.set_xlabel('Ano', fontsize=14)
    ax.set_ylabel('Temperatura (°C)', fontsize=14)
    ax.grid(True)
    ax.legend()
    
    # Adicionar valores aos pontos
    for col in ['Mediana Temperatura (°C)', 'Temperatura Máxima (°C)', 'Temperatura Mínima (°C)']:
        for _, row in stats.iterrows():
            ax.text(row['Ano'], row[col], f"{row[col]:.1f}",
                   ha='center', va='bottom', fontsize=10)
    
    save_plot(fig, output_dir, 'tendencia_temperatura.png')

def plot_temperature_distribution(df: pd.DataFrame, output_dir: str) -> None:
    """Cria e salva um boxplot da distribuição de temperatura"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    sns.boxplot(
        data=df,
        x='ANO',
        y='MEDIA_DIARIA',
        hue='ANO',
        palette='coolwarm',
        legend=False,
        ax=ax
    )
    
    ax.set_title('Distribuição da Temperatura Média por Ano', fontsize=16)
    ax.set_xlabel('Ano', fontsize=14)
    ax.set_ylabel('Temperatura Média (°C)', fontsize=14)
    plt.xticks(rotation=45)
    
    save_plot(fig, output_dir, 'distribuicao_temperatura.png')

def plot_precipitation_distribution(df: pd.DataFrame, output_dir: str) -> None:
    """Gráfico de distribuição de precipitação total"""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.histplot(df['PRECIPITACAO_TOTAL'], kde=True, color='blue', bins=30, ax=ax)
    ax.set_title('Distribuição da Precipitação Total', fontsize=16)
    ax.set_xlabel('Precipitação Total (mm)', fontsize=14)
    ax.set_ylabel('Frequência', fontsize=14)
    save_plot(fig, output_dir, 'distribuicao_precipitacao.png')

def plot_temp_vs_humidity(df: pd.DataFrame, output_dir: str) -> None:
    """Gráfico de temperatura vs umidade relativa"""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.scatterplot(x=df['TEMPERATURA_AR'], y=df['UMIDADE_RELATIVA'], 
                   color='green', alpha=0.6, ax=ax)
    ax.set_title('Temperatura vs Umidade Relativa', fontsize=16)
    ax.set_xlabel('Temperatura (°C)', fontsize=14)
    ax.set_ylabel('Umidade Relativa (%)', fontsize=14)
    save_plot(fig, output_dir, 'temp_vs_umidade.png')

def plot_pressure_distribution(df: pd.DataFrame, output_dir: str) -> None:
    """Gráfico de distribuição de pressão atmosférica"""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.histplot(df['PRESSAO_ESTACAO'], kde=True, color='orange', bins=30, ax=ax)
    ax.set_title('Distribuição da Pressão Atmosférica', fontsize=16)
    ax.set_xlabel('Pressão Atmosférica (hPa)', fontsize=14)
    ax.set_ylabel('Frequência', fontsize=14)
    save_plot(fig, output_dir, 'distribuicao_pressao.png')

def plot_wind_speed_distribution(df: pd.DataFrame, output_dir: str) -> None:
    """Gráfico de distribuição da velocidade do vento"""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.histplot(df['VENTO_VELOCIDADE'], kde=True, color='purple', bins=30, ax=ax)
    ax.set_title('Distribuição da Velocidade do Vento', fontsize=16)
    ax.set_xlabel('Velocidade do Vento (m/s)', fontsize=14)
    ax.set_ylabel('Frequência', fontsize=14)
    save_plot(fig, output_dir, 'distribuicao_vento.png')

def plot_radiation_distribution(df: pd.DataFrame, output_dir: str) -> None:
    """Gráfico de distribuição de radiação global"""
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.histplot(df['RADIACAO_GLOBAL'], kde=True, color='red', bins=30, ax=ax)
    ax.set_title('Distribuição da Radiação Global', fontsize=16)
    ax.set_xlabel('Radiação Global (W/m²)', fontsize=14)
    ax.set_ylabel('Frequência', fontsize=14)
    save_plot(fig, output_dir, 'distribuicao_radiacao.png')

def main():
    output_dir = "imagens_resultados"
    create_output_dir(output_dir)

    try:
        print("Processando dados...")
        df = load_and_process_data('dados_meteorologicos_completos.xlsx')
        df = calculate_daily_average(df)
        stats = calculate_annual_stats(df)
        
        print("Gerando visualizações de temperatura...")
        create_temperature_table(stats, output_dir)
        plot_temperature_trend(stats, output_dir)
        plot_temperature_distribution(df, output_dir)
        
        print("Gerando visualizações meteorológicas adicionais...")
        plot_precipitation_distribution(df, output_dir)
        plot_temp_vs_humidity(df, output_dir)
        plot_pressure_distribution(df, output_dir)
        plot_wind_speed_distribution(df, output_dir)
        plot_radiation_distribution(df, output_dir)
        
        print("\n✅ Análise concluída com sucesso!")
        print(f"📁 Resultados salvos em: {os.path.abspath(output_dir)}")
        print("\nArquivos gerados:")
        print(f"- 📊 tabela_temperaturas.png (Tabela de temperaturas)")
        print(f"- 📈 tendencia_temperatura.png (Gráfico de tendência)")
        print(f"- 📦 distribuicao_temperatura.png (Boxplot por ano)")
        print(f"- 🌧️ distribuicao_precipitacao.png (Distribuição de chuva)")
        print(f"- 🌡️ temp_vs_umidade.png (Relação temperatura/umidade)")
        print(f"- ⏲️ distribuicao_pressao.png (Distribuição de pressão)")
        print(f"- 💨 distribuicao_vento.png (Distribuição de vento)")
        print(f"- ☀️ distribuicao_radiacao.png (Distribuição de radiação)")
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {str(e)}")

if __name__ == "__main__":
    main()