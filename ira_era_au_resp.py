#%%
# Importar librerías
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Crear una función para cargar datos según el año seleccionado
def load_data(year):
    try:
        df = pd.read_csv(f'data/df_{year}_rm_resp.csv')
        return df
    except FileNotFoundError:
        st.error(f'Archivo para el año {year} no encontrado.')
        return None

# Configuración de la aplicación Streamlit

logo_horizontal = 'img/horizontal_SEREMIRM_blue.png'
logo_icono = 'img/icon_SEREMIRM.png'
st.logo(logo_horizontal, icon_image=logo_icono)

# Selector de año
selected_year = st.sidebar.selectbox(
    'Seleccione el año',
    options=[2018, 2019, 2020, 2021, 2022, 2023, 2024],
    index=5  # Establecer 2023 como valor predeterminado
)
hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital',['APS','Hospitales'],index=0)
st.title(f'Atenciones de Urgencia en {hospital} - RM 2018-2024')
# Cargar datos según el año seleccionado
df_rm = load_data(selected_year)
if df_rm is None:
    st.stop()

# Diccionario de mapeo de IdCausa a glosa_causa
diccionario_causas_au = {
    1: 'Atenciones de urgencia - Total',
    2: 'Atenciones de urgencia - Total Respiratorios',
    31: 'Atenciones de urgencia - Covid-19, No Identificado (U07.2)',
    30: 'Atenciones de urgencia - Covid-19, Identificado (U07.1)',
    6: 'Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)',
    5: 'Atenciones de urgencia - Neumonía (J12-J18)',
    4: 'Atenciones de urgencia - Influenza (J09-J11)',
    10: 'Atenciones de urgencia - IRA Alta (J00-J06)',
    3: 'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    11: 'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)',
    25: 'Hospitalizaciones - Total',
    7: 'Hospitalizaciones - Sistema Respiratorio',
    33: 'Hospitalizaciones - COVID-19 No Identificado (U7.2)',
    32: 'Hospitalizaciones - COVID-19 Identificado (U7.1)',
}

# Listas de causas
irab = [
    'Atenciones de urgencia - Neumonía (J12-J18)',
    'Atenciones de urgencia - Bronquitis/bronquiolitis aguda (J20-J21)',
    'Atenciones de urgencia - Crisis obstructiva bronquial (J40-J46)'
]
iraa = ['Atenciones de urgencia - IRA Alta (J00-J06)']
covid = [
    'Atenciones de urgencia - Covid-19, No Identificado (U07.2)',
    'Atenciones de urgencia - Covid-19, Identificado (U07.1)'
]
total_au = ['Atenciones de urgencia - Total']
total_resp = ['Atenciones de urgencia - Total Respiratorios']
influ = ['Atenciones de urgencia - Influenza (J09-J11)']
otras = ['Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)']

# Filtrar dataframes para APS y hospitales
if hospital == 'Hospitales':
    df_rm = df_rm.loc[(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
else:
    df_rm = df_rm.loc[~(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
#%%

def grafico_area_atenciones_respiratorias(df, col, title):
    # Filtrar y agrupar los datos
    df_iraa = df[df['Causa'].isin(iraa)].groupby('semana')[col].sum().reset_index()
    df_irab = df[df['Causa'].isin(irab)].groupby('semana')[col].sum().reset_index()
    df_influ = df[df['Causa'].isin(influ)].groupby('semana')[col].sum().reset_index()
    df_covid = df[df['Causa'].isin(covid)].groupby('semana')[col].sum().reset_index()
    df_otras = df[df['Causa'].isin(otras)].groupby('semana')[col].sum().reset_index()

    # Crear la figura del gráfico
    fig = go.Figure()

    # Añadir trazas para cada grupo de causas
    fig.add_trace(go.Scatter(
        x=df_iraa['semana'], y=df_iraa[col], 
        mode='lines', name='IRAS Altas'
    ))
    fig.add_trace(go.Scatter(
        x=df_irab['semana'], y=df_irab[col], 
        mode='lines', name='IRAS Bajas'
    ))
    fig.add_trace(go.Scatter(
        x=df_influ['semana'], y=df_influ[col], 
        mode='lines', name='Influenza'
    ))
    fig.add_trace(go.Scatter(
        x=df_covid['semana'], y=df_covid[col], 
        mode='lines', name='Covid-19'
    ))
    fig.add_trace(go.Scatter(
        x=df_otras['semana'], y=df_otras[col], 
        mode='lines', name='Otras causas respiratorias'
    ))

    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='Semana',
        yaxis_title='N° Atenciones',
        legend_title='Leyenda'
    )

    return fig

def grafico_atenciones_urgencia_respiratorias_pie(df, col, title):
    # Calcular totales por Causa
    total_iraa = df[df['Causa'].isin(iraa)][col].sum()
    total_irab = df[df['Causa'].isin(irab)][col].sum()
    total_influ = df[df['Causa'].isin(influ)][col].sum()
    total_covid = df[df['Causa'].isin(covid)][col].sum()
    total_otras = df[df['Causa'].isin(otras)][col].sum()

    # Calcular los porcentajes en relación a total_respiratorias
    total_respiratorias = total_iraa + total_irab + total_influ + total_covid + total_otras
    percentage_iraa = (total_iraa / total_respiratorias) * 100
    percentage_irab = (total_irab / total_respiratorias) * 100
    percentage_influ = (total_influ / total_respiratorias) * 100
    percentage_covid = (total_covid / total_respiratorias) * 100
    percentage_otras = (total_otras / total_respiratorias) * 100

    # Etiquetas y valores para el gráfico de pastel
    labels = [
        'IRAs Altas', 
        'IRAs Bajas', 
        'Influenza', 
        'Covid-19', 
        'Otras causas respiratorias'
    ]
    values = [percentage_iraa, percentage_irab, percentage_influ, percentage_covid, percentage_otras]
    
    # Crear la figura del gráfico de pastel
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
    )
    
    return fig


def grafico_atenciones_urgencia_barras(df, col, title):
    # Calcular totales por Causa
    total_iraa = df[df['Causa'].isin(iraa)][col].sum()
    total_irab = df[df['Causa'].isin(irab)][col].sum()
    total_influ = df[df['Causa'].isin(influ)][col].sum()
    total_covid = df[df['Causa'].isin(covid)][col].sum()
    total_otras = df[df['Causa'].isin(otras)][col].sum()
    
    # Etiquetas y valores para el gráfico de barras horizontales
    labels = [
        'IRAs Altas', 
        'IRAs Bajas', 
        'Influenza', 
        'Covid-19', 
        'Otras causas respiratorias'
    ]
    values = [total_iraa, total_irab, total_influ, total_covid, total_otras]
    
    # Crear la figura del gráfico de barras horizontales
    fig = go.Figure(data=[go.Bar(x=values, y=labels, orientation='h')])
    
    # Configuración del diseño del gráfico
    fig.update_layout(
        title=title,
        xaxis_title='N° Atenciones',
        yaxis_title='Causa',
        legend_title='Causas'
    )
    
    return fig
#%%
# Graficos
fig_area3_total = grafico_area_atenciones_respiratorias(df_rm, 'Total', f'Atenciones de Urgencia Respiratoria - Total {selected_year}')
fig_area3_menor1 = grafico_area_atenciones_respiratorias(df_rm, 'Menores_1', f'Atenciones de Urgencia Respiratoria - Menores de 1 Año {selected_year}')
fig_area3_mayor65 = grafico_area_atenciones_respiratorias(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia Respiratoria - Mayores de 65 Años {selected_year}')

fig_pie3_total = grafico_atenciones_urgencia_respiratorias_pie(df_rm, 'Total', f'Atenciones de Urgencia Respiratoria - Total {selected_year}')
fig_pie3_menor1 = grafico_atenciones_urgencia_respiratorias_pie(df_rm, 'Menores_1', f'Atenciones de Urgencia Respiratoria - Menores de 1 Año {selected_year}')
fig_pie3_mayor65 = grafico_atenciones_urgencia_respiratorias_pie(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia Respiratoria - Mayores de 65 Años {selected_year}')

fig_bar3_total = grafico_atenciones_urgencia_barras(df_rm, 'Total', f'Atenciones de Urgencia Respiratoria - Total {selected_year}')
fig_bar3_menor1 = grafico_atenciones_urgencia_barras(df_rm, 'Menores_1', f'Atenciones de Urgencia Respiratoria - Menores de 1 Año {selected_year}')
fig_bar3_mayor65 = grafico_atenciones_urgencia_barras(df_rm, 'De_65_y_mas', f'Atenciones de Urgencia Respiratoria - Mayores de 65 Años {selected_year}')

# Configuración de la aplicación Streamlit

# Índice de navegación
st.header(f'Atenciones de urgencia según tipo de causa respiratoria en {hospital}, RM {selected_year}')

st.subheader('Todas las Edades')
st.plotly_chart(fig_area3_total)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas específicas (IRAs Altas, IRAs Bajas, Influenza, COVID-19, y otras causas respiratorias) en todas las edades en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Menores de 1 Año')
st.plotly_chart(fig_area3_menor1)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas específicas (IRAs Altas, IRAs Bajas, Influenza, COVID-19, y otras causas respiratorias) en menores de 1 año en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Mayores de 65 Años')
st.plotly_chart(fig_area3_mayor65)
st.markdown(f"Este gráfico muestra la evolución semanal del total de atenciones de urgencia por causas específicas (IRAs Altas, IRAs Bajas, Influenza, COVID-19, y otras causas respiratorias) en mayores de 65 años en {hospital} de la Región Metropolitana durante el año {selected_year}.")

st.subheader('Todas las Edades')
st.plotly_chart(fig_pie3_total)
st.plotly_chart(fig_bar3_total)

st.subheader('Menores de 1 Año')
st.plotly_chart(fig_pie3_menor1)
st.plotly_chart(fig_bar3_menor1)

st.subheader('Mayores de 65 Años')
st.plotly_chart(fig_pie3_mayor65)
st.plotly_chart(fig_bar3_mayor65)
