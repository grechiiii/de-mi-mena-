import streamlit as st
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
# Creamos la lista de páginas
chocoframe = pd.read_excel('chocodata.xlsx')
#transformar a booleanos para poder analizar con true o false
conv_booleanos = chocoframe.columns[1:19]
chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

#transformar a números para contar cantidades
conv_float = chocoframe.columns[19:34]
chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

#transformar a strings para que salgan en display
conv_string = chocoframe.columns[34:37]
chocoframe[conv_string] = chocoframe[conv_string].astype(str)

paginas = ['Inicio', 'Experiencia'] #Cambiar por nombres deseados
# Creamos botones de navegación tomando la lista de páginas
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)
# Generamos condicionales para mostrar el contenido de cada página
if pagina_seleccionada == 'Inicio':
    # La función st.markdown permite centrar y agrandar la letra del título de la web en Streamlit.
    st.markdown("<h1 style='text-align: center;'>Vamos a comer!</h1>", unsafe_allow_html=True)
    #Acá
    if "step" not in st.session_state:
        st.session_state.step = "start"
    if "current_filtered_frame" not in st.session_state:
        st.session_state.current_filtered_frame = chocoframe.copy()
    def reset_chat():
        st.session_state.step = "start"
        st.session_state.current_filtered_frame = chocoframe.copy()

    st.title("🍫 Asistente de Selección de Chocolates")

    if st.session_state.step == "start":
        st.write("Hola! ¿Deseas comer chocolate?")
        col1, col2 = st.columns(2)
        if col1.button("Sí"):
            st.session_state.current_filtered_frame = chocoframe.copy()
            st.session_state.step = "tipo_chocolate"
        if col2.button("No"):
            st.write("Está bien. ¡Hasta la próxima!")

    elif st.session_state.step == "tipo_chocolate":
            choice = st.radio("¿Qué deseas comer?", [
                "Solo chocolate",
                "Hecho en su mayoría de chocolate",
                "Con acentos de chocolate"
            ])
            if choice == "Solo chocolate":
                st.session_state.step = "mani_almendras"
            elif choice == "Hecho en su mayoría de chocolate":
                st.session_state.step = "hecho_mayoria"
            else:
                st.session_state.step = "acentos"
            st.button("Siguiente", on_click=lambda: None)

    elif st.session_state.step == "mani_almendras":
        col = 'barra de chocolate'
        if col in chocoframe.columns:
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[
                    chocoframe[col] == True
                ]
            choice = st.radio("¿Prefieres chocolates con maní o almendras?", [
                "Con maní", "Sin maní", "Con Almendras", "Sin Almendras"
            ])
        if choice == "Con maní":
            col = 'mani'
            if col in chocoframe.columns:
                st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == True]
        elif choice == "Sin maní":
            col = 'mani'
            if col in chocoframe.columns:
                st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == False]
        elif choice == "Con Almendras":
            col = 'almendras'
            if col in chocoframe.columns:
                st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == True]
            elif choice == "Sin Almendras":
                col = 'almendras'
            if col in chocoframe.columns:
                st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == False]

            st.session_state.step = "tipo_final"
            st.button("Siguiente", on_click=lambda: None)

    elif st.session_state.step == "tipo_final":
            choice = st.radio("¿Deseas chocolate con leche, blanco o puro?", [
                "Con leche", "Blanco", "Puro"
            ])
            col_map = {
                "Con leche": "chocolate con leche",
                "Blanco": "chocolate blanco",
                "Puro": "chocolate puro"
            }
            col = col_map[choice]
            if col in chocoframe.columns:
                st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[
                    chocoframe[col] == True
                ]

            if not st.session_state.current_filtered_frame.empty:
                st.success("Según tus preferencias, te recomendamos los siguientes chocolates:")
                st.dataframe(st.session_state.current_filtered_frame)
            else:
                st.warning("Lo siento, no encontramos ningún chocolate que coincida con todas tus preferencias.")
            st.button("Reiniciar", on_click=reset_chat)

        # Puedes continuar la adaptación con bloques similares para:
        # - st.session_state.step == "hecho_mayoria"
        # - st.session_state.step == "acentos"
        # - y sus subopciones
else:
    st.markdown("<h1 style='text-align: center;'>Beneficios</h1>", unsafe_allow_html=True)
    #Toda la info que desee
      
