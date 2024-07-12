import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def create_endemic_corridor(df, cause, total_column):
    # Filtrar el dataframe para la causa específica
    df_cause = df.loc[df['Causa'].isin(cause)]
    
    # Agrupar los datos por año y semana
    grouped = df_cause.groupby(by=['año', 'semana'])[total_column].sum().reset_index()
    
    # Calcular la mediana y los cuartiles para cada semana
    quartiles = grouped.groupby('semana')[total_column].quantile([0.25, 0.5, 0.75]).unstack().reset_index()
    quartiles.columns = ['semana', 'percentil_25', 'mediana', 'percentil_75']
    
    # Agregar los datos del año seleccionado
    selected_year = grouped['año'].max()  # Seleccionar el último año disponible
    current_year_data = grouped[grouped['año'] == selected_year][['semana', total_column]]
    current_year_data.columns = ['semana', 'current_year_total']
    endemic_corridor = pd.merge(quartiles, current_year_data, on='semana', how='left')
    
    # Visualizar el corredor endémico
    fig = go.Figure()
    
    # Éxito (bajo el percentil 25)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_25'], 
        mode='lines', 
        name='Éxito (Percentil 25)', 
        line=dict(color='rgba(0, 255, 0, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=[0] * len(endemic_corridor), 
        mode='lines', 
        line=dict(color='rgba(0, 255, 0, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(0, 255, 0, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Seguridad (entre percentil 25 y mediana)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        name='Seguridad (Mediana)', 
        line=dict(color='rgba(0, 0, 255, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_25'], 
        mode='lines', 
        line=dict(color='rgba(0, 0, 255, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(0, 0, 255, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Alerta (entre mediana y percentil 75)
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['percentil_75'], 
        mode='lines', 
        name='Alerta (Percentil 75)', 
        line=dict(color='rgba(255, 255, 0, 0.2)')
    ))
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        line=dict(color='rgba(255, 255, 0, 0.2)'), 
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.2)',
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Alerta Roja (por encima del percentil 75)
    # fig.add_trace(go.Scatter(
    #     x=endemic_corridor['semana'], 
    #     y=[endemic_corridor['percentil_75'].max()] * len(endemic_corridor), 
    #     mode='lines', 
    #     name='Alerta (Percentil 75+)', 
    #     line=dict(color='rgba(255, 0, 0, 0.2)')
    # ))
    # fig.add_trace(go.Scatter(
    #     x=endemic_corridor['semana'], 
    #     y=endemic_corridor['percentil_75'], 
    #     mode='lines', 
    #     line=dict(color='rgba(255, 0, 0, 0.2)'), 
    #     fill='tonexty',
    #     fillcolor='rgba(255, 0, 0, 0.2)',
    #     hoverinfo='skip',
    #     showlegend=False
    # ))

    # Mediana histórica
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['mediana'], 
        mode='lines', 
        name='Mediana Histórica', 
        line=dict(color='blue')
    ))

    # Datos del año en curso
    fig.add_trace(go.Scatter(
        x=endemic_corridor['semana'], 
        y=endemic_corridor['current_year_total'], 
        mode='lines+markers', 
        name=f'Año {selected_year}', 
        line=dict(color='green')
    ))

    fig.update_layout(
        title='Corredor Endémico de Atenciones de Urgencia',
        xaxis_title='Semana',
        yaxis_title='Total de Atenciones',
        template='plotly_white'
    )
    
    st.plotly_chart(fig)

# Ejemplo de uso de la función en un script de Streamlit

# Cargar datos según el intervalo de años seleccionado
def load_data(start_year, end_year):
    dataframes = []
    for year in range(start_year, end_year + 1):
        try:
            df = pd.read_csv(f'data/df_{year}_rm_resp.csv')
            df['año'] = year  # Agregar columna de año
            dataframes.append(df)
        except FileNotFoundError:
            st.error(f'Archivo para el año {year} no encontrado.')
    if dataframes:
        return dataframes
    else:
        return None



# Configurar la interfaz de Streamlit
st.title('Visualización del Corredor Endémico')

# Cargar datos según el intervalo de años seleccionado
year_range = st.sidebar.slider('Seleccione el intervalo de años', 2018, 2024, (2018, 2023))
hospital = st.sidebar.selectbox('Seleccione si desea ver la información de APS o Hospital', ['APS', 'Hospitales'], index=0)

start_year, end_year = year_range
selected_year = end_year  # Definir el último año del rango como el año seleccionado
list_df_rm = load_data(start_year, end_year)
if list_df_rm is None:
    st.stop()
df_rm = pd.concat(list_df_rm)

# Filtrar dataframes para APS y hospitales
if hospital == 'Hospitales':
    df_rm = df_rm.loc[(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]
else:
    df_rm = df_rm.loc[~(df_rm.GLOSATIPOESTABLECIMIENTO == 'Hospital')]

# Verificar datos filtrados
print("Datos filtrados:")
print(df_rm.head())

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
total_resp = ['Atenciones de urgencia - Total Respiratorios']+covid
influ = ['Atenciones de urgencia - Influenza (J09-J11)']
otras = ['Atenciones de urgencia - Otra causa respiratoria (J22, J30-J39, J47, J60-J98)']

causas_dict = {
    'IRAB': irab,
    'IRAA': iraa,
    'COVID': covid,
    'Total AU': total_au,
    'Total Respiratorios': total_resp,
    'Influenza': influ,
    'Otras': otras
}

# Crear el corredor endémico
# Elegir CAUSA
create_endemic_corridor(df_rm, cause=total_resp, total_column='Total')  # Ajustar los parámetros según sea necesario
