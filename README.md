# Project Insights – House Rocket
 ![crop-hand-holding-house-near-coins](https://user-images.githubusercontent.com/107287165/175185016-1ac7ddca-a12a-42da-b223-46184753a414.jpg)

# 1. Problema de Negócio
A House Rocket é uma plataforma digital que tem como modelo de negócio, a compra e a venda de imóveis usando tecnologia.
O CEO da House Rocket gostaria de maximizar a receita da empresa encontrando boas oportunidades de negócio.

Sua principal estratégia é comprar boas casas em ótimas localizações com preços baixos e depois revendê-las posteriormente à preços mais altos. Quanto maior a diferença entre a compra e a venda, maior o lucro da empresa e, portanto, maior sua receita.

Entretanto, as casas possuem muitos atributos que as tornam mais ou menos atrativas aos compradores e vendedores e a localização e o período do ano também podem influenciar os preços.

Portanto, desenvolvi uma análise exploratória buscando identificar casas com potencial de compra e venda. Além disso desenvolvi um site hospedado em Cloud para que o time de negócio possa realizar filtros e visualizar os dados, assim como também a localização de cada imóvel.

# 2. Suposições de Negócio.
As seguintes suposições para este problema de negócio foram tomadas:

-> Id’s repetidos serão mantidos para a análise exploratória caracterizando imóveis sendo anunciados em dias diferentes. Para os relatórios foram descartados id’s duplicados com o objetivo de melhorar a experiência do time de negócios em suas análises. 

-> Os andares de cada imóvel foram tratados como números inteiros, números flutuantes serão arredondados ao número inteiro anterior.

# Lista de Atributos
Para o processo de análise foi utilizado um dataset público hospedado no [Kaggle](https://www.kaggle.com/harlfoxem/housesalesprediction).

Este dataset possui as seguintes variáveis:

|Atributos | Descrição |
|----------|-----------|
|id | Identificador de anúncio para cada propriedade. |
|date |	Data em que a propriedade ficou disponível. |
|price | O preço anunciado de cada imóvel. |
|bedrooms | Número de quartos. |
|bathrooms | O número de banheiros, sendo os valores 0,5 o indicador de um quarto com banheiro, mas sem chuveiro, já o valor 0,75 ou 3/4 representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira. |
|sqft_living | Pés quadrados do interior das casas. |
|sqft_lot |	Pés quadrados do terreno das casas. |
|floors | Número de andares. |
|waterfront | Variável indicadora para imóveis com visualização ao mar (1) ou não (0). |
|view | Um índice de 0 a 4 de quão boa era a visualização da propriedade. |
|condition |  Um índice de 1 a 5 sobre o estado das moradias, 1 indica propriedade degradada e 5 excelente. |
|grade | Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 representa baixo nível da qualidade de construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade. |
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo. |
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo. |
|yr_built | Ano de construção da propriedade. |
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as propriedades nunca renovadas. |
|zipcode | Um código de cinco dígitos, similar ao CEP, para indicar a área onde se encontra a propriedade. |
|lat | Coordenada de Latitude. |
|long | Coordenada de Longitude. |
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas. |
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas. |

# 3. A solução
A problemática destaca a necessidade de análise dos imóveis no banco de dados, porém o time de negócio não possui tempo hábil para realizar a pesquisa em um volume tão grande. Para solucionar este projeto desenvolvi dois relatórios, o primeiro com sugestões de compra por imóvel juntamente com o valor recomendado, para o segundo relatório conterá sugestão de venda indicando os melhores momentos para venda e o valor recomendado.

A estrutura para recomendação de compras leva em consideração a mediana de preço do imóvel por região, portanto imóveis com preço abaixo da mediana, boas condições e avaliações serão os recomendados.

A estrutura utilizada para a venda de imóveis considera a mediana do preço de imóveis e a sazonalidade (temporada) do ano, estes atributos permitem recomendar vendas com base na mediana de preço da região e os melhores meses para anunciar. 

Os relatórios foram disponibilizados em Excel, mas para melhor comodidade a equipe de negócio, também foi entregue um site que permita filtrar as informações no relatório. O resultado se encontra neste [site](https://house-rocket-analysis-cds.herokuapp.com/).

# 4. Estratégia de Solução
![image](https://user-images.githubusercontent.com/107287165/175185090-7fc87ee7-706e-4fc9-b01b-48c5728ffdc4.png)

Minha estratégia para resolver esse desafio foi:

**Step 01. Data Description:** Realizar limpeza e identificar outliers que comprometam a análise dos dados.

**Step 02. Feature Engineering:** Derivar novos atributos com base nas variáveis originais para descrever melhor o fenômeno a ser compreendido.

**Step 03. Exploratory Data Analysis:** Explorar os dados para encontrar insights e entender melhor o impacto das variáveis.

**Step 04. Business Value:** Transcrever a análise produzida em um resultado de negócio.

**Step 05. Deploy Model to Production:** Publicar os relatórios em um ambiente web para que outras pessoas ou serviços possam usar os resultados para melhorar a decisão de negócios.


# 5. Top 5 Insights de Negócio
No processo das análises exploratórias dos dados, foram levantadas algumas hipóteses de negócio que deveriam ser validadas (ou invalidadas) a fim de trazer insights de negócio. Destaco aqui 5 Insights identificados nos dados.

**Hipótese:** Imóveis com reforma são 30% mais caros na média.

![image](https://user-images.githubusercontent.com/107287165/175185144-ee7ac0c7-e20b-480c-9715-8a0a0a6830f1.png)

Através do gráfico podemos comprovar que a hipótese é verdadeira, pois imóveis renovados são em média 43.37% mais caros.

**Hipótese:** Imóveis vendem 30% mais no verão na média.

![image](https://user-images.githubusercontent.com/107287165/175185243-410820b2-189b-4f90-91d5-b55665c4ddaf.png)

Este Insight nos mostra que o pico de vendas ocorre na primavera com uma diferença de 3% para o verão.

**Hipótese:** Imóveis são 20% mais caros no verão na média.

![image](https://user-images.githubusercontent.com/107287165/175185286-8ff660aa-3836-4e9b-84e7-ea32adcde11f.png)

O gráfico demonstra que imóveis vendem por um preço maior na primavera com uma diferença de 1,07% para o verão.

**Hipótese:** Imóveis com banheiros completos são 10% mais caros na média.

![image](https://user-images.githubusercontent.com/107287165/175187546-9d7f4e72-8fb2-48ff-96ec-a163594a95c7.png)

O gráfico demonstra que a hipótese é falsa, pois imóveis com banheiro completo vendem 30.53% a menos do que banheiros sem chuveiro.

**Hipótese:** Para cada andar do imóvel, o preço médio é 20% maior.

![image](https://user-images.githubusercontent.com/107287165/175185328-4953654c-8503-4064-88bb-1e5f94a05880.png)

O gráfico demonstra que a hipótese é falsa, pois o crescimento do preço médio para cada andar é de aproximadamente 16.10%.

# 6. Resultados de Negócio
Os relatórios gerados permitem a equipe de negócios consultar imóveis indicados para compra e venda com a seguinte previsão de faturamento:

| Compras totais | Vendas totais | Lucro bruto total |
|----------------|---------------|-------------------|
| $ 3.535.777.760,00 | 4.561.543.361,20 | 1.025.765.601,20|

O resultado esperado corresponde a 8.578 imóveis recomendados para compra com um lucro por imóvel de aproximadamente $ 119.580,97.


Em contraste ao realizar a compra de todos os imóveis traria o seguinte resultado:

| Compras totais | Vendas totais | Lucro bruto total |
|----------------|---------------|-------------------|
|$ 11.610.168.601,00 | $ 13.611.834.574,50 | $ 2.001.665.973,50 |

Este resultado corresponde a 21.435 com um lucro por imóvel de aproximadamente $ 93.383,06.

A comparação entre os resultados destaca que utilizar a abordagem de compra com base nos indicadores apontados no relatório permite um aumento do lucro de aproximadamente 28,05% por imóvel com um custo total aproximado de 228,36% a menos.

# 7. Produto de Dados
Para que a equipe de análise de negócios possa ter acesso ao relatório e realizar filtros permitindo identificar os melhores imóveis foi disponibilizado um site hospedado nos serviços Cloud da Heroku. Também consta um mapa que possibilite a rápida localização do imóvel. 

![image](https://user-images.githubusercontent.com/107287165/175185345-beb7fccd-3861-4d75-b535-5f4775fe96d9.png)

O site se encontra [aqui](https://house-rocket-analysis-cds.herokuapp.com/).

# 8. Conclusões
Podemos concluir que o resultado, para um primeiro ciclo de desenvolvimento, se mostra satisfatório. Foi possível após uma coleta de dados e uma análise completa, identificar alavancas de negócios, elaboração de insights e desenvolver relatórios capazes de responder as perguntas de negócio com os potenciais margens de ganho de aproximadamente 28%. 

# 9. Próximos Passos
 Um segundo ciclo de desenvolvimento é indicado para otimizar a estrutura de análise e melhorar a performance dos ganhos, também possibilita observar o problema de diferentes ângulos identificando Insights antes não observados.

**Tópicos a serem explorados:**

-> Elaborar um novo plano de recomendação de compras e vendas dos imóveis através da aplicação de Machine Learning.

-> Identificar novos Insights que possuem grande correlação para o preço.

-> Otimizar a resposta de informações disponíveis no site melhorando a experiência de usuário. 

-> Disponibilizar novos filtros para os dados gerados no site para melhorar a análise do time de negócios.
