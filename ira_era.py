#%%
# Importar librerías
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.image('img/seremi-100-años.png', width=300)
logo_horizontal = 'img/horizontal_SEREMIRM_blue.png'
logo_icono = 'img/icon_SEREMIRM.png'
st.logo(logo_horizontal,icon_image=logo_icono)

def ira_era():
    st.title("IRA ERA - RM 2018-2025")
    st.subheader("Capítulo IV - Vigilancia Enfermedades Respiratorias")
    texto = """
    En función del refuerzo asistencial estacional para las consultas de salud en toda la Red Pública Asistencial, se activa la vigilancia de enfermedades respiratoria a través de la estrategia “Programa Campaña de Invierno”. Este método procura enfrentar en la red asistencial el aumento de las infecciones respiratorias agudas (IRA), las que constituyen un problema epidemiológico nacional en los meses de otoño e invierno.

    Las infecciones respiratorias agudas afectan a un número importante de la población durante todo el año, pero tienen un peak en un determinado momento del mismo, caracterizado por un conjunto de variables tales como: exposición a contaminantes, frío, humedad y virus circulantes, pudiendo llegar a adquirir un carácter epidémico con gran impacto en la morbilidad y mortalidad.

    En este contexto se pone en acción el refuerzo asistencial estacional y una campaña de comunicación social para educación a la comunidad. Esta campaña se focaliza preferentemente en menores de un año y en los mayores de 65 años, que son los grupos biológicamente más vulnerables.

    Complementariamente la vigilancia epidemiológica de las enfermedades tipo influenza (ETI), se realiza a través de establecimientos de atención primaria que actúan como centros centinelas, vigilando morbilidad y etiología.
    """
    st.write(texto)


pg =st.navigation([
    st.Page(ira_era, title="IRA ERA - RM 2018-2025", icon=":material/home:"),
    st.Page('ira_era_au.py', title="Atenciones de Urgencias", icon=":material/monitoring:"),
    st.Page('ira_era_au_resp.py', title="A. Urgencias Respiratorias", icon=":material/monitoring:"),
    st.Page('ira_era_au_año.py', title="A. Urgencia Respiratorios por años", icon=":material/monitoring:"),
    st.Page('ira_era_endemico.py', title="A. Urgencia Corredor Endémico", icon=":material/monitoring:"),
    st.Page('ira_era_hosp.py', title="Hospitalizaciones", icon=":material/monitoring:"),
    st.Page('ira_era_hosp_año.py', title="Hospitalizaciones - Año", icon=":material/monitoring:"),
    st.Page('ira_era_hosp_endemico.py', title="Hospitalizaciones - Corredor Endémico", icon=":material/monitoring:"),

])

pg.run()