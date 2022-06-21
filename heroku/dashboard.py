import streamlit as st
import pandas as pd
import geopandas
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


# Settings
st.set_page_config( layout='wide' ) # Ajuste de resolução
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Header
st.title('House Rocket Company')
st.markdown('Bem vindo a análise de dados da House Rocket. Este site tem como objetivo apresentar'
            ' os resultados construidos através do projeto de dados gerado pelo link: '
            '[House Rocket Project](https://github.com/SamuelOliveirads/project_insight_house_rocket)'
            , unsafe_allow_html=True)


# Helper Funcions
@st.cache(allow_output_mutation=True)
def get_data (path):
    data = pd.read_csv(path)
    return data


@st.cache(allow_output_mutation=True)
def get_geofile(url):
    geofile = geopandas.read_file(url)
    return geofile


# Feature Engineering
def set_features(df):
    # Delimitador entre imoveis antigas e novas (anteriores a 1955 serão consideradas antigas)
    df.loc[df['yr_built'] < 1955, 'age_house'] = 'old'
    df.loc[df['yr_built'] >= 1955, 'age_house'] = 'new'

    # Imoveis com e sem porao
    df.loc[df['sqft_basement'] == 0, 'basement'] = 'no'
    df.loc[df['sqft_basement'] > 0, 'basement'] = 'yes'

    # Coluna contendo apenas o ano da publicacao do imovel para a venda
    df['year'] = pd.to_datetime(df['date']).dt.year

    # Coluna contendo apenas o mês da publicacao do imovel para a venda
    df['month'] = pd.to_datetime(df['date']).dt.month

    # Coluna discriminando se o imovel foi ou nao renovado
    df.loc[df['yr_renovated'] == 0, 'is_renovated'] = 'no'
    df.loc[df['yr_renovated'] > 0, 'is_renovated'] = 'yes'

    # Coluna discriminando as estacoes do ano em que o imovel foi publicado a venda
    bins = [0, 2, 5, 8, 11, 12]
    df['season'] = pd.cut(df['month'], bins, labels=['winter', 'spring', 'summer', 'fall', 'winter'], ordered=False)

    # Coluna para discriminar banheiros completos (chuveiro, pia, vaso) dos banheiros sem chuveiro
    bathint = [0, 1, 2, 3, 4, 5, 6, 8]  # Banheiro com chuveiro
    bathfloat = [0.5, 0.75, 1.25, 1.5, 1.75, 2.25, 2.5, 2.75, 3.25, 3.5, 3.75,
                 4.25, 4.5, 4.75, 5.25, 5.5, 5.75, 6.25, 6.5, 6.75, 7.5, 7.75]  # Banheiro sem chuveiro

    df.loc[df['bathrooms'].isin(bathint), 'complete_bathroom'] = 'yes'
    df.loc[df['bathrooms'].isin(bathfloat), 'complete_bathroom'] = 'no'

    return df


def data_overview(df):
    # Title
    st.header('Principais Insights')
    st.markdown('Abaixo se encontra os 10 Insights gerados pela análise de dados')

    # Plot de hipoteses

    # H1: Imóveis que possuem vista para água, são 30% mais caros, na média.
    h1 = df[['waterfront', 'price']].groupby('waterfront').mean().reset_index()

    # Plot
    c1, c2 = st.columns((1, 1))
    c1.subheader('Houses per waterview')
    c1.markdown('Hipotese 1: Imóveis que possuem vista para água, são 30% mais caros, na média.')
    fig = px.bar(h1, x='waterfront', y='price', labels={'waterfront': 'Vista a água', 'price': 'Preço'}
                 , color='waterfront')
    c1.plotly_chart(fig, use_container_width=True)

    c1.markdown('A hipótese 1 é falsa, pois imóveis com vista para água são em média 212.64% mais caros')

    # H2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.
    h2 = df[['age_house', 'price']].groupby('age_house').mean().reset_index()

    # Plot
    c2.subheader('Houses per age')
    c2.markdown('Hipotese 2: Imóveis com data de construção menor que 1955, são 50% mais baratos, na média')

    fig = px.bar(h2, x='age_house', y='price',labels={'age_house': 'Condição do imóvel', 'price': 'Preço'},
                  color='age_house')
    c2.plotly_chart(fig, use_container_width=True)

    c2.markdown('A hipótese 2 é falsa, pois imóveis com data de construção menor que 1955 são 0.79% mais barato.')

    # H3: Imóveis sem porão (sqft_basement), são 40% maiores do que com porão em media.
    h3 = df[['basement', 'sqft_lot']].groupby('basement').mean().reset_index()

    # Plot
    c3, c4 = st.columns((1, 1))
    c3.subheader('Houses with/without basement')
    c3.markdown('Hipotese 3: Imóveis sem porão (sqft_basement), são 40% maiores do que com porão em media')

    fig = px.bar(h3, x='basement', y='sqft_lot', labels={'basement': 'Porão', 'sqft_lot': 'Tamnho do Lote'},
                 color='basement')
    c3.plotly_chart(fig, use_container_width=True)

    c3.markdown('A hipótese 3 é falsa, pois imóveis sem porão são 22.56% maiores.')

    # H4: O crescimento do preço dos imóveis YoY (Year over Year) é de 10%
    h4 = df[['year', 'price']].groupby('year').mean().reset_index()

    # plot
    c4.subheader('Houses with price per year')
    c4.markdown('Hipotese 4: O crescimento do preço dos imóveis YoY (Year over Year) é de 10%')

    fig = px.bar(h4, x='year', y='price', labels={'year': 'Ano de publicação', 'price': 'Preço'},
                 color='year')
    c4.plotly_chart(fig, use_container_width=True)

    c4.markdown('A hipótese 4 é falsa, pois o crescimento ano a ano dos preços é 0.05% em média.')

    # H5: Imóveis com 3 banheiros tem um crescimento MoM (Month over Month) de 15% em média
    h5 = df.copy()
    h5 = h5[h5['bathrooms'] == 3]  # Filtragem para imoveis com 3 banheiros
    h5 = h5[['bathrooms', 'month', 'price']].groupby('month').mean().reset_index()
    h5.drop(columns='bathrooms', inplace=True)

    # Plot
    c5, c6 = st.columns((1, 1))
    c5.subheader('Houses with price per month')
    c5.markdown('Hipotese 5: Imóveis com 3 banheiros tem um crescimento MoM (Month over Month) de 15% em média')

    fig = px.bar(h5, x='month', y='price', labels={'month': 'Mês de publicação', 'price': 'Preço'},
                 color='month')
    c5.plotly_chart(fig, use_container_width=True)

    c5.markdown('A hipótese 5 é falsa, pois o crescimento mês a mês dos preços é de 0.99% em média.')

    # H6: Imóveis com reforma são 30% mais caros na média.
    h6 = df[['is_renovated', 'price']].groupby('is_renovated').mean().reset_index()

    # Plot
    c6.subheader('Houses renovated')
    c6.markdown('Hipotese 6: Imóveis com reforma são 30% mais caros na média')

    fig = px.bar(h6, x='is_renovated', y='price', labels={'is_renovated': 'Reforma', 'price': 'Preço'},
                 color='is_renovated')
    c6.plotly_chart(fig, use_container_width=True)

    c6.markdown('A hipótese 6 é verdadeira, pois imóveis com reforma são 43.37% mais caros em média.')

    # H7: Imóveis vendem 30% mais no verão na média
    h7 = df[['season', 'price']].groupby('season').count().reset_index()

    # Plot
    c7, c8 = st.columns((1, 1))
    c7.subheader('Sales per season')
    c7.markdown('Hipotese 7: Imóveis vendem 30% mais no verão na média')

    fig = px.bar(h7, x='season', y='price', labels={'season': 'Temporada do ano', 'price': 'Preço'},
                 color='season')
    c7.plotly_chart(fig, use_container_width=True)

    c7.markdown('A hipótese 7 é falsa, pois os imóveis vendem 3.00% a menos no verão em comparação a primavera (maior'
                ' estação de vendas).')

    # H8: Imóveis são 20% mais caros no verão na média.
    h8 = df[['season', 'price']].groupby('season').mean().reset_index()

    # Plot
    c8.subheader('Saler per season')
    c8.markdown('Hipotese 8: Imóveis são 20% mais caros no verão na média')

    fig = px.bar(h8, x='season', y='price', labels={'season': 'Temporada do ano', 'price': 'Preço'},
                 color='season')
    c8.plotly_chart(fig, use_container_width=True)

    c8.markdown('A hipótese 8 é falsa, pois os imóveis em verão vendem 1.07% a menos do que na primavera (maior estação'
                ' em preços).')

    # H9: Imóveis com banheiros completos são 10% mais caros na média.
    h9 = df[['complete_bathroom', 'price']].groupby('complete_bathroom').mean().reset_index()

    # Plot
    c9, c10 = st.columns((1, 1))
    c9.subheader('Houses per type of bathroom')
    c9.markdown('Hipotese 9: Imóveis com banheiros completos são 10% mais caros na média')

    fig = px.bar(h9, x='complete_bathroom', y='price',
                 labels={'complete_bathroom': 'Banheiro completo', 'price': 'Preço'},
                 color='complete_bathroom')
    c9.plotly_chart(fig, use_container_width=True)

    c9.markdown('A hipótese 9 é falsa, pois os imóveis com banheiro completo vendem 30.53% a'
                ' menos do que banheiros sem chuveiro.')

    # H10: Para cada andar do imóvel, o preço médio é 20% maior.
    h10 = df[['floors', 'price']].groupby('floors').mean().reset_index()

    # Plot
    c10.subheader('Houses per floors')
    c10.markdown('Hipotese 10: Para cada andar do imóvel, o preço médio é 20% maior')

    fig = px.bar(h10, x='floors', y='price', labels={'floors': 'Andares', 'price': 'Preço'},
                 color='floors')
    c10.plotly_chart(fig, use_container_width=True)

    c10.markdown('A hipótese 10 é falsa, pois o crescimento do preço médio para cada'
                 ' andar é de aproximandamente 16.10%.')

    return None

def filters(relt1, relt2):
    st.sidebar.title('Filtros para os relatórios')

    # Filtro lateral para relatório
    f_zipcode = st.sidebar.multiselect('Entre com o zipcode', relt1['zipcode'].unique())
    f_condition = st.sidebar.multiselect('Entre com o valor de condition', relt1['condition'].unique())

    if (f_zipcode != []) & (f_condition != []):
        relt1 = relt1.loc[(relt1['zipcode'].isin(f_zipcode)) & (relt1['condition'].isin(f_condition))]
        relt2 = relt2.loc[(relt2['zipcode'].isin(f_zipcode)) & (relt2['condition'].isin(f_condition))]

    elif (f_zipcode != []) & (f_condition == []):
        relt1 = relt1.loc[relt1['zipcode'].isin(f_zipcode)]
        relt2 = relt2.loc[relt2['zipcode'].isin(f_zipcode)]

    elif (f_zipcode == []) & (f_condition != []):
        relt1 = relt1.loc[relt1['condition'].isin(f_condition)]
        relt2 = relt2.loc[relt2['condition'].isin(f_condition)]

    else:
        relt1 = relt1.copy()
        relt2 = relt2.copy()

    return relt1, relt2


def dataframe_overview(relt1, relt2):
    # Drop de colunas geográficas
    relt1 = relt1.drop(['lat', 'long'], axis=1)

    # Plot de relatórios
    st.header('Relatórios')
    st.markdown('Abaixo se encontra os relatórios com análises indicando imóveis a comprar e a vender')

    c1, c2 = st.columns((1, 1))

    c1.subheader('Relatório de recomendação de compra dos imóveis')
    c1.dataframe(relt1, height=600)

    c2.subheader('Relatório de recomendação de venda dos imóveis')
    c2.dataframe(relt2, height=600)

    return None


def region_overview(data, geofile):
    # Densidade de portfolio
    st.title('Visualização geográfica do relatório de compras')

    c1, c2 = st.columns((1, 1))
    c1.header('Densidade do porftolio')

    df = data.copy()

    # Mapa base - Folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in df.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold R${0}'
                      .format(row['price'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Mapa de região de preço
    c2.header('Densidade de preço')

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()], default_zoom_start=15)

    region_price_map.choropleth(data=df, geo_data=geofile, columns=['ZIP', 'PRICE'], key_on='feature.properties.ZIP',
                                fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2, legend_name='AVG PRICE')

    with c2:
        folium_static(region_price_map)

    return None


if __name__ == "__main__":
    path1 = 'kc_house_data.csv'
    path2 = 'kc_house_buy_report_geo.csv'
    path3 = 'kc_house_sell_report.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    # Load data
    df = get_data(path1)
    relt1 = get_data(path2)
    relt2 = get_data(path3)
    geofile = get_geofile(url)

    # Set features
    set_features(df)

    # Filters
    relt1, relt2 = filters(relt1, relt2)

    # Transform data
    data_overview(df)

    # Show report
    dataframe_overview(relt1, relt2)

    # Region Display
    region_overview(relt1, geofile)
