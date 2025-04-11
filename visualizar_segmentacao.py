"""
Visualizador de segmentação de clientes - Script auxiliar
Este script carrega os dados de segmentação gerados pelo script principal
e exibe visualizações interativas.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Definir estilo dos gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

def carregar_dados():
    try:
        # Tentar carregar o arquivo CSV
        dados = pd.read_csv('segmentacao_clientes.csv')
        print(f"Dados de segmentação carregados com sucesso! Encontrados {len(dados)} registros.")
        
        # Verificar se a coluna Cluster existe
        if 'Cluster' not in dados.columns:
            print("Erro: A coluna 'Cluster' não foi encontrada nos dados.")
            return None
        
        # Exibir distribuição dos clusters
        print("\nDistribuição dos clusters:")
        distribuicao = dados['Cluster'].value_counts().sort_index()
        for cluster, contagem in distribuicao.items():
            print(f"Cluster {cluster}: {contagem}")
        
        # Estatísticas por cluster
        print("\nEstatísticas por cluster:")
        # Selecionar apenas colunas numéricas, excluindo 'Cluster' e 'Segmento'
        colunas_numericas = dados.select_dtypes(include=['number']).columns.tolist()
        if 'Cluster' in colunas_numericas:
            colunas_numericas.remove('Cluster')
        if 'Segmento' in colunas_numericas:
            colunas_numericas.remove('Segmento')
            
        estatisticas = dados.groupby('Cluster')[colunas_numericas].mean()
        print(estatisticas)
        
        # Identificar segmentos com base nos dados
        if 'Segmento' in dados.columns:
            segmentos = dados[['Cluster', 'Segmento']].drop_duplicates().set_index('Cluster')['Segmento']
            print("\nSegmentos identificados:")
            for cluster, segmento in segmentos.items():
                print(f"Cluster {cluster}: {segmento}")
        
        return dados
    
    except FileNotFoundError:
        print("Erro: O arquivo 'segmentacao_clientes.csv' não foi encontrado.")
        print("Execute primeiro o script 'segmentacao_clientes.py' para gerar o arquivo.")
        return None
    
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

def visualizar_2d(dados):
    plt.figure(figsize=(12, 8))
    
    # Verificar se a coluna 'Segmento' existe para os rótulos
    if 'Segmento' in dados.columns:
        segmentos = dados[['Cluster', 'Segmento']].drop_duplicates().set_index('Cluster')['Segmento']
        clusters_unicos = segmentos.index
    else:
        clusters_unicos = dados['Cluster'].unique()
        segmentos = {cluster: f"Cluster {cluster}" for cluster in clusters_unicos}
    
    # Obter o número de clusters únicos
    n_clusters = len(clusters_unicos)
    
    # Definir cores (apenas o número necessário)
    cores = ['#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b'][:n_clusters]
    marcadores = ['o', 's', '^', 'D', 'P'][:n_clusters]
    
    for i, cluster in enumerate(sorted(clusters_unicos)):
        plt.scatter(
            dados[dados['Cluster'] == cluster]['Renda_Anual'],
            dados[dados['Cluster'] == cluster]['Gasto_Mensal'],
            s=100, c=cores[i % len(cores)], marker=marcadores[i % len(marcadores)], alpha=0.7,
            label=f'Cluster {cluster}: {segmentos.get(cluster, f"Cluster {cluster}")}'
        )
    
    # Adicionar média dos clusters
    medias = dados.groupby('Cluster')[['Renda_Anual', 'Gasto_Mensal']].mean().reset_index()
    plt.scatter(
        medias['Renda_Anual'],
        medias['Gasto_Mensal'],
        s=300, c='red', marker='*', alpha=1, edgecolor='black',
        label='Média dos Clusters'
    )
    
    plt.title('Segmentação de Clientes: Renda Anual vs Gasto Mensal', fontsize=15)
    plt.xlabel('Renda Anual (R$)', fontsize=12)
    plt.ylabel('Gasto Mensal (R$)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

def visualizar_3d(dados):
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Verificar se a coluna 'Segmento' existe para os rótulos
    if 'Segmento' in dados.columns:
        segmentos = dados[['Cluster', 'Segmento']].drop_duplicates().set_index('Cluster')['Segmento']
        clusters_unicos = segmentos.index
    else:
        clusters_unicos = dados['Cluster'].unique()
        segmentos = {cluster: f"Cluster {cluster}" for cluster in clusters_unicos}
    
    # Obter o número de clusters únicos
    n_clusters = len(clusters_unicos)
    
    # Definir cores (apenas o número necessário)
    cores = ['#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b'][:n_clusters]
    marcadores = ['o', 's', '^', 'D', 'P'][:n_clusters]
    
    for i, cluster in enumerate(sorted(clusters_unicos)):
        ax.scatter(
            dados[dados['Cluster'] == cluster]['Idade'],
            dados[dados['Cluster'] == cluster]['Renda_Anual'],
            dados[dados['Cluster'] == cluster]['Gasto_Mensal'],
            s=80, c=cores[i % len(cores)], marker=marcadores[i % len(marcadores)], alpha=0.7,
            label=f'Cluster {cluster}: {segmentos.get(cluster, f"Cluster {cluster}")}'
        )
    
    # Adicionar média dos clusters
    medias = dados.groupby('Cluster')[['Idade', 'Renda_Anual', 'Gasto_Mensal']].mean().reset_index()
    ax.scatter(
        medias['Idade'],
        medias['Renda_Anual'],
        medias['Gasto_Mensal'],
        s=300, c='red', marker='*', alpha=1, edgecolor='black',
        label='Média dos Clusters'
    )
    
    ax.set_title('Segmentação de Clientes em 3D: Idade, Renda e Gasto', fontsize=15)
    ax.set_xlabel('Idade', fontsize=12)
    ax.set_ylabel('Renda Anual (R$)', fontsize=12)
    ax.set_zlabel('Gasto Mensal (R$)', fontsize=12)
    ax.legend(fontsize=10)
    plt.tight_layout()
    plt.show()

def visualizar_boxplots(dados):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Obter o número de clusters únicos
    n_clusters = len(dados['Cluster'].unique())
    
    # Definir cores (apenas o número necessário)
    cores = ['#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b'][:n_clusters]
    
    # Idade por cluster
    sns.boxplot(x='Cluster', y='Idade', data=dados, ax=axes[0], palette=cores, hue='Cluster', legend=False)
    axes[0].set_title('Distribuição de Idade por Cluster', fontsize=12)
    axes[0].set_xlabel('Cluster')
    axes[0].set_ylabel('Idade')
    
    # Renda por cluster
    sns.boxplot(x='Cluster', y='Renda_Anual', data=dados, ax=axes[1], palette=cores, hue='Cluster', legend=False)
    axes[1].set_title('Distribuição de Renda por Cluster', fontsize=12)
    axes[1].set_xlabel('Cluster')
    axes[1].set_ylabel('Renda Anual (R$)')
    
    # Gasto por cluster
    sns.boxplot(x='Cluster', y='Gasto_Mensal', data=dados, ax=axes[2], palette=cores, hue='Cluster', legend=False)
    axes[2].set_title('Distribuição de Gasto por Cluster', fontsize=12)
    axes[2].set_xlabel('Cluster')
    axes[2].set_ylabel('Gasto Mensal (R$)')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    dados = carregar_dados()
    
    if dados is not None:
        print("\nExecutando visualizações interativas...")
        
        try:
            visualizar_2d(dados)
            visualizar_3d(dados)
            visualizar_boxplots(dados)
        except Exception as e:
            print(f"Erro ao gerar visualizações: {e}")
            print("As visualizações geradas pelo script principal estão salvas como arquivos PNG.")
    else:
        print("Não foi possível visualizar os dados devido a erros no carregamento.") 