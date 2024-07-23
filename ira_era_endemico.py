import streamlit as st
import pandas as pd
import plotly.graph_objects as go

GLOBAL_THEME='seaborn'
def create_endemic_corridor(df, cause, total_column, title):
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
        line=dict(color='red')
    ))

    fig.update_layout(
        title=f'Corredor Endémico de {title}',
        xaxis_title='Semana',
        yaxis_title='Total de Atenciones',
        template=GLOBAL_THEME,
        yaxis=dict(tickformat='.0f', tickprefix='', ticksuffix='')
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
    'Total Atenciones de urgencias': total_au,
    'Total Respiratorios': total_resp,
    'IRAB': irab,
    'IRAA': iraa,
    'COVID': covid,
    'Influenza': influ,
    'Otras': otras
}

causa_select=st.sidebar.selectbox('Seleccione causa:',causas_dict.keys(),1)
causa=causas_dict[causa_select]
dict_columnas={'Total':'Total de la población', 
      'Menores_1':'Menores de 1 año', 
      'De_1_a_4': '1 a 4 años', 
      'De_5_a_14': '5 a 14 años', 
      'De_15_a_64':'15 a 64 años',
    'De_65_y_mas':'Mayores de 45 años'}

st.markdown("""
### ¿Qué es un corredor endémico?
Un corredor endémico es una herramienta epidemiológica utilizada para monitorear enfermedades infecciosas y otros eventos de salud a lo largo del tiempo. Se basa en el análisis de datos históricos para determinar los límites esperados de ocurrencia de una enfermedad durante un período específico (por ejemplo, semanal). Estos límites ayudan a identificar niveles de éxito, seguridad, alerta y alerta roja.

#### Componentes del Corredor Endémico:
- **Éxito (Percentil 25)**: Representa el límite bajo del corredor endémico. Si los casos están por debajo de este límite, se considera que la situación está bajo control.
- **Seguridad (Mediana)**: Representa el valor medio de los casos esperados. Los casos entre el percentil 25 y la mediana indican una situación dentro del rango normal.
- **Alerta (Percentil 75)**: Representa el límite superior del corredor endémico. Los casos entre la mediana y el percentil 75 indican una situación de alerta.
- **Alerta Roja (por encima del Percentil 75)**: Representa una situación crítica donde los casos superan significativamente el nivel esperado.

#### Instrucciones:
1. Seleccione el intervalo de años deseado en el control deslizante de la barra lateral.
2. Seleccione si desea ver la información de APS (Atención Primaria de Salud) o Hospitales.
3. Seleccione la causa de las atenciones de urgencia que desea analizar.
4. Observe los gráficos generados para cada grupo de edad.

Esta herramienta proporciona una visualización clara de las tendencias de atención de urgencia para diferentes causas y grupos de edad, ayudando a identificar situaciones anómalas y a tomar decisiones informadas.
""")

for key,value in dict_columnas.items():
    create_endemic_corridor(df_rm, cause=causa, total_column=key, title=value)
