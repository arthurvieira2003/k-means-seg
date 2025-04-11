import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.cm as cm
import requests
import io

# Configuração do estilo dos gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# Download do dataset Mall Customers (público)
print("Baixando o dataset 'Mall Customers'...")
url = "https://raw.githubusercontent.com/SteffiPeTaffy/machineLearningAZ/master/Machine%20Learning%20A-Z%20Template%20Folder/Part%204%20-%20Clustering/Section%2025%20-%20Hierarchical%20Clustering/Mall_Customers.csv"

try:
    response = requests.get(url)
    if response.status_code == 200:
        # Carregar o dataset diretamente na memória
        dados = pd.read_csv(io.StringIO(response.text))
        print("Dataset baixado com sucesso!")
        
        # Renomear as colunas para português
        dados.columns = ['ID_Cliente', 'Genero', 'Idade', 'Renda_Anual', 'Pontuacao_Gasto']
        
        # Remover a coluna ID_Cliente e Genero que não são relevantes para a segmentação
        dados = dados.drop(['ID_Cliente', 'Genero'], axis=1)
        
        # Converter Renda_Anual para milhares (K) para milhares de reais
        dados['Renda_Anual'] = dados['Renda_Anual'] * 1000
        
        # Renomear a coluna de pontuação de gasto para algo mais intuitivo
        dados = dados.rename(columns={'Pontuacao_Gasto': 'Gasto_Mensal'})
        
        # Multiplicar a pontuação de gasto por 100 para representar um valor em reais
        dados['Gasto_Mensal'] = dados['Gasto_Mensal'] * 100
        
        print("Dataset processado e pronto para análise!")
    else:
        raise Exception(f"Erro ao baixar o dataset. Código de status: {response.status_code}")
except Exception as e:
    print(f"Erro ao baixar o dataset: {e}")
    print("Não foi possível baixar o dataset. Verifique sua conexão com a internet e tente novamente.")
    exit(1)  # Encerrar o programa com erro

print("Dados do dataset:")
print(dados.describe())

# Normalização dos dados
scaler = StandardScaler()
dados_normalizados = scaler.fit_transform(dados)

# Determinando o número ideal de clusters usando o método do cotovelo
wcss = []
range_k = range(1, 11)
for k in range_k:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(dados_normalizados)
    wcss.append(kmeans.inertia_)

# Plotando o gráfico do método do cotovelo
plt.figure(figsize=(10, 6))
plt.plot(range_k, wcss, marker='o', linestyle='-')
plt.title('Método do Cotovelo para Determinar o Número Ideal de Clusters', fontsize=15)
plt.xlabel('Número de Clusters', fontsize=12)
plt.ylabel('WCSS (Within-Cluster Sum of Squares)', fontsize=12)
plt.xticks(range_k)
plt.grid(True)
plt.tight_layout()
plt.savefig('metodo_cotovelo.png')
plt.close()

# Determinando o número ótimo de clusters
# Analisando o gráfico do cotovelo, escolhemos k=5 para o dataset Mall Customers
k_otimo = 5
kmeans = KMeans(n_clusters=k_otimo, random_state=42, n_init=10)
clusters = kmeans.fit_predict(dados_normalizados)
dados['Cluster'] = clusters

# Calculando a pontuação de silhueta
silhouette_avg = silhouette_score(dados_normalizados, clusters)
print(f"Pontuação de Silhueta: {silhouette_avg:.3f}")

# Adicionando os centróides dos clusters aos dados originais
centros = scaler.inverse_transform(kmeans.cluster_centers_)
centros_df = pd.DataFrame(centros, columns=dados.columns[:-1])
print("\nCentróides dos clusters:")
print(centros_df)

# Verificando a distribuição dos clusters
print("\nDistribuição dos clusters:")
print(dados['Cluster'].value_counts())

# Estatísticas por cluster
print("\nEstatísticas por cluster:")
print(dados.groupby('Cluster').mean())

# Analisando os clusters
medias_cluster = dados.groupby('Cluster').mean().reset_index()
medias_cluster = medias_cluster.sort_values(by='Gasto_Mensal', ascending=False)

# Criando rótulos baseados nas características dos clusters
rotulos_clusters = {}

for i, row in medias_cluster.iterrows():
    cluster = row['Cluster']
    idade = row['Idade']
    renda = row['Renda_Anual']
    gasto = row['Gasto_Mensal']
    
    # Classificação por idade
    if idade < 30:
        faixa_idade = "Jovens"
    elif idade < 50:
        faixa_idade = "Adultos"
    else:
        faixa_idade = "Seniores"
    
    # Classificação por gasto
    if gasto > 6000:
        nivel_gasto = "alto gasto"
    elif gasto > 4000:
        nivel_gasto = "gasto moderado"
    else:
        nivel_gasto = "baixo gasto"
    
    # Classificação por renda
    if renda > 80000:
        nivel_renda = "alta renda"
    elif renda > 50000:
        nivel_renda = "renda média"
    else:
        nivel_renda = "baixa renda"
    
    # Combinando as classificações para criar um rótulo descritivo
    rotulos_clusters[cluster] = f"{faixa_idade} com {nivel_renda} e {nivel_gasto}"

# Adicionando rótulos descritivos ao DataFrame
dados['Segmento'] = dados['Cluster'].map(rotulos_clusters)

# Exibindo os rótulos e suas características
print("\nSegmentos identificados:")
for cluster, rotulo in rotulos_clusters.items():
    print(f"Cluster {cluster}: {rotulo}")

# Visualização 2D: Renda vs Gasto
plt.figure(figsize=(12, 8))
# Obter o número de clusters únicos
n_clusters = len(rotulos_clusters)
# Definir cores (apenas o número necessário)
cores = ['#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd', '#8c564b'][:n_clusters]
marcadores = ['o', 's', '^', 'D', 'P'][:n_clusters]

for i, (cluster, rotulo) in enumerate(rotulos_clusters.items()):
    plt.scatter(
        dados[dados['Cluster'] == cluster]['Renda_Anual'],
        dados[dados['Cluster'] == cluster]['Gasto_Mensal'],
        s=100, c=cores[i % len(cores)], marker=marcadores[i % len(marcadores)], alpha=0.7, 
        label=f'Cluster {cluster}: {rotulo}'
    )

# Plotando os centróides
plt.scatter(
    centros_df['Renda_Anual'],
    centros_df['Gasto_Mensal'],
    s=300, c='red', marker='*', alpha=1, edgecolor='black',
    label='Centróides'
)

plt.title('Segmentação de Clientes: Renda Anual vs Gasto Mensal', fontsize=15)
plt.xlabel('Renda Anual (R$)', fontsize=12)
plt.ylabel('Gasto Mensal (R$)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('segmentacao_renda_gasto.png')
plt.close()

# Visualização 3D: Idade, Renda e Gasto
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

for i, (cluster, rotulo) in enumerate(rotulos_clusters.items()):
    ax.scatter(
        dados[dados['Cluster'] == cluster]['Idade'],
        dados[dados['Cluster'] == cluster]['Renda_Anual'],
        dados[dados['Cluster'] == cluster]['Gasto_Mensal'],
        s=80, c=cores[i % len(cores)], marker=marcadores[i % len(marcadores)], alpha=0.7,
        label=f'Cluster {cluster}: {rotulo}'
    )

# Plotando os centróides em 3D
ax.scatter(
    centros_df['Idade'],
    centros_df['Renda_Anual'],
    centros_df['Gasto_Mensal'],
    s=300, c='red', marker='*', alpha=1, edgecolor='black',
    label='Centróides'
)

ax.set_title('Segmentação de Clientes em 3D: Idade, Renda e Gasto', fontsize=15)
ax.set_xlabel('Idade', fontsize=12)
ax.set_ylabel('Renda Anual (R$)', fontsize=12)
ax.set_zlabel('Gasto Mensal (R$)', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig('segmentacao_3d.png')
plt.close()

# Visualização da distribuição das características por cluster
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Idade por cluster
sns.boxplot(x='Cluster', y='Idade', data=dados, ax=axes[0], hue='Cluster', palette=cores, legend=False)
axes[0].set_title('Distribuição de Idade por Cluster', fontsize=12)
axes[0].set_xlabel('Cluster')
axes[0].set_ylabel('Idade')

# Renda por cluster
sns.boxplot(x='Cluster', y='Renda_Anual', data=dados, ax=axes[1], hue='Cluster', palette=cores, legend=False)
axes[1].set_title('Distribuição de Renda por Cluster', fontsize=12)
axes[1].set_xlabel('Cluster')
axes[1].set_ylabel('Renda Anual (R$)')

# Gasto por cluster
sns.boxplot(x='Cluster', y='Gasto_Mensal', data=dados, ax=axes[2], hue='Cluster', palette=cores, legend=False)
axes[2].set_title('Distribuição de Gasto por Cluster', fontsize=12)
axes[2].set_xlabel('Cluster')
axes[2].set_ylabel('Gasto Mensal (R$)')

plt.tight_layout()
plt.savefig('distribuicao_caracteristicas.png')
plt.close()

print("\nAnálise concluída! As visualizações foram salvas como arquivos PNG.")
print("Detalhes dos segmentos identificados:")
for cluster, rotulo in rotulos_clusters.items():
    grupo = dados[dados['Cluster'] == cluster]
    print(f"\n{rotulo}:")
    print(f"  - Quantidade: {len(grupo)} clientes")
    print(f"  - Idade média: {grupo['Idade'].mean():.1f} anos")
    print(f"  - Renda média: R$ {grupo['Renda_Anual'].mean():.2f}")
    print(f"  - Gasto médio: R$ {grupo['Gasto_Mensal'].mean():.2f}")

# Salvando os dados para uso posterior
dados.to_csv('segmentacao_clientes.csv', index=False)
print("\nDados salvos em 'segmentacao_clientes.csv'") 