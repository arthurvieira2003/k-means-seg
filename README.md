# Segmentação de Clientes com K-Means

Este projeto implementa a segmentação de clientes de e-commerce utilizando o algoritmo K-Means.

## Objetivo

Agrupar clientes automaticamente em segmentos com comportamentos semelhantes baseado em:

- Idade
- Renda anual
- Gasto médio mensal na loja

## Instalação e Execução

Para instalar as dependências:

```bash
pip install -r requirements.txt
```

Para executar a análise de segmentação:

```bash
python segmentacao_clientes.py
```

Para visualizar os resultados de forma interativa:

```bash
python visualizar_segmentacao.py
```

## Resultados da Análise

A análise de segmentação de clientes de e-commerce utilizando o algoritmo K-Means foi concluída com sucesso. Foram identificados cinco segmentos distintos de clientes com base em idade, renda anual e gasto mensal na loja.

### Segmentos Identificados

Os clientes foram segmentados em cinco grupos com perfis bem definidos:

1. **Adultos com alta renda e alto gasto**

   - Quantidade: 40 clientes
   - Idade média: 32,9 anos
   - Renda média: R$ 86.100,00
   - Gasto médio: R$ 8.152,50
   - Perfil: Adultos jovens com alto poder aquisitivo e dispostos a gastar mais na plataforma.

2. **Jovens com baixa renda e alto gasto**

   - Quantidade: 54 clientes
   - Idade média: 25,2 anos
   - Renda média: R$ 41.092,59
   - Gasto médio: R$ 6.224,07
   - Perfil: Jovens que, apesar de renda menor, priorizam gastos na plataforma.

3. **Seniores com renda média e gasto moderado**

   - Quantidade: 47 clientes
   - Idade média: 55,6 anos
   - Renda média: R$ 54.382,98
   - Gasto médio: R$ 4.885,11
   - Perfil: Clientes mais maduros com uma relação equilibrada entre renda e consumo.

4. **Adultos com alta renda e baixo gasto**

   - Quantidade: 39 clientes
   - Idade média: 39,9 anos
   - Renda média: R$ 86.102,56
   - Gasto médio: R$ 1.935,90
   - Perfil: Clientes com alto poder aquisitivo mas que não priorizam gastos na plataforma.

5. **Adultos com baixa renda e baixo gasto**
   - Quantidade: 20 clientes
   - Idade média: 46,2 anos
   - Renda média: R$ 26.750,00
   - Gasto médio: R$ 1.835,00
   - Perfil: Clientes com menor poder aquisitivo e baixo engajamento com a plataforma.

## Pontuação de Silhueta

A pontuação de silhueta obtida foi de 0,417, indicando uma separação moderadamente boa entre os clusters. Valores próximos a 1 indicam clusters bem separados, enquanto valores próximos a 0 indicam sobreposição.

## Visualizações Geradas

Foram geradas as seguintes visualizações para análise:

1. **Método do Cotovelo** (`metodo_cotovelo.png`): Ajuda a determinar o número ideal de clusters para este conjunto de dados.
2. **Segmentação 2D** (`segmentacao_renda_gasto.png`): Visualização dos clientes em um gráfico 2D (Renda vs. Gasto) com cores diferentes para cada grupo.
3. **Segmentação 3D** (`segmentacao_3d.png`): Visualização tridimensional dos clientes considerando idade, renda e gasto.
4. **Distribuição de Características** (`distribuicao_caracteristicas.png`): Boxplots mostrando a distribuição de idade, renda e gasto por cluster.

## Recomendações Estratégicas

Com base nos segmentos identificados, recomendamos as seguintes estratégias:

### Para Adultos com alta renda e alto gasto:

- Programa de fidelidade premium
- Produtos exclusivos e de luxo
- Comunicação focada em qualidade e exclusividade

### Para Jovens com baixa renda e alto gasto:

- Programa de cashback e benefícios
- Produtos com apelo a tendências e moda
- Comunicação focada em novidades e experiências

### Para Seniores com renda média e gasto moderado:

- Comunicação com foco em benefícios e segurança
- Produtos com boa relação custo-benefício
- Atendimento personalizado e facilitado

### Para Adultos com alta renda e baixo gasto:

- Incentivos para aumentar o engajamento
- Produtos com apelo a qualidade e durabilidade
- Comunicação destacando valor agregado e exclusividade

### Para Adultos com baixa renda e baixo gasto:

- Descontos e condições especiais de pagamento
- Produtos com preços mais acessíveis
- Comunicação focada em economia e praticidade

## Conclusão

A segmentação de clientes permite personalizar estratégias de marketing, desenvolvimento de produtos e experiência do usuário para cada grupo, maximizando o potencial de vendas e a satisfação dos clientes.

O código implementado permite:

1. Baixar e processar o dataset automaticamente
2. Realizar a segmentação utilizando K-Means
3. Gerar visualizações estáticas e interativas
4. Analisar as características de cada segmento

Os dados e as visualizações estão disponíveis para uma análise mais detalhada nos arquivos PNG gerados pelo script principal.
