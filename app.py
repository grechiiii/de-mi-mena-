import streamlit as st
import pandas as pd

# ================== ESTILO PERSONALIZADO ==================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #fffaf3;
            font-family: 'Comic Sans MS', cursive;
        }

        h1, h2, h3, h4 {
            color: #4b2e1e;
        }

        .css-1d391kg, .css-1n76uvr {
            background-color: #e8d5c4;
        }

        .stButton>button {
            background-color: #d4a373;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            height: 3em;
            margin: 5px;
        }

        .zoom:hover {
            transform: scale(1.1);
            transition: transform .2s;
        }

        .separator {
            height: 2px;
            background-color: #a97155;
            margin: 20px 0;
        }

        .img-redonda {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== CARGA DE DATOS ==================
chocoframe = pd.read_excel('chocodata.xlsx')

# Transformaciones de columnas
conv_booleanos = chocoframe.columns[1:19]
chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

conv_float = chocoframe.columns[19:34]
chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

conv_string = chocoframe.columns[34:37]
chocoframe[conv_string] = chocoframe[conv_string].astype(str)

# ================== PÁGINAS ==================
paginas = ['Inicio', 'Experiencia']
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# ================== PÁGINA DE INICIO ==================
if pagina_seleccionada == 'Inicio':
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstrito.png", width=150)
    st.markdown("<h1 style='text-align: center;'>¡Vamos a comer!</h1>", unsafe_allow_html=True)

    if "step" not in st.session_state:
        st.session_state.step = "start"
    if "current_filtered_frame" not in st.session_state:
        st.session_state.current_filtered_frame = chocoframe.copy()

    def reset_chat():
        st.session_state.step = "start"
        st.session_state.current_filtered_frame = chocoframe.copy()

    st.markdown("<h3 style='text-align: center;'>🍫 Asistente de Selección de Chocolates 🍫</h3>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolates%20tres%20tipos.png", use_column_width=True)
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

    if st.session_state.step == "start":
        st.write("Hola! ¿Deseas comer chocolate?")
        col1, col2 = st.columns(2)
        if col1.button("Sí"):
            st.session_state.current_filtered_frame = chocoframe.copy()
            st.session_state.step = "tipo_chocolate"
        if col2.button("No"):
            st.write("Está bien. ¡Hasta la próxima!")

    elif st.session_state.step == "tipo_chocolate":
        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20cocinando.png", width=120)
        choice = st.radio("¿Qué deseas comer?", [
            "Solo chocolate",
            "Hecho en su mayoría de chocolate",
            "Con acentos de chocolate"
        ])
        if choice:
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
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['mani'] == True]
        elif choice == "Sin maní":
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['mani'] == False]
        elif choice == "Con Almendras":
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['almendras'] == True]
        elif choice == "Sin Almendras":
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['almendras'] == False]

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
            st.success("✨ Según tus preferencias, te recomendamos los siguientes chocolates:")
            st.dataframe(st.session_state.current_filtered_frame)
        else:
            st.warning("Lo siento, no encontramos ningún chocolate que coincida con tus preferencias.")
        st.button("Reiniciar", on_click=reset_chat)

        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        # POSTRES FINALES
        st.markdown("### 🍰 Postres con chocolate:")

        cols = st.columns(4)
        with cols[0]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolatito.png", width=100, caption="Chocolate")
        with cols[1]:
            st.image("https://github.com/grechiiii/de-mi-mena-/blob/main/image/brownie.png?raw=true", width=100, caption="Brownie")
        with cols[2]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/torta.png", width=100, caption="Quequito")
        with cols[3]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/galletita.png", width=100, caption="Galletita")

        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20comiendo.png", width=150)
        st.markdown("<p style='text-align: center;'>¡Esperamos que disfrutes tu chocolate! 🥰</p>", unsafe_allow_html=True)

# ================== PÁGINA DE EXPERIENCIA ==================
else:
    st.markdown("<h1 style='text-align: center;'>Beneficios del chocolate</h1>", unsafe_allow_html=True)
    st.write("""
    El chocolate no solo es delicioso, sino que también tiene propiedades antioxidantes, mejora el estado de ánimo y puede ser parte de una dieta balanceada. ¡Disfrútalo con amor!
    """)
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolates.jpg", use_column_width=True)
