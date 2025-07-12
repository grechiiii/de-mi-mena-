import streamlit as st
import pandas as pd

# ===================== ESTILO PERSONALIZADO =====================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #fffdf8;
            font-family: 'Arial Rounded MT Bold', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #5a3c2a;
        }
        .stButton>button {
            background-color: #a97155;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
        .stRadio > div {
            background-color: #f6ebe3;
            padding: 10px;
            border-radius: 10px;
        }
        .custom-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
        }
        .section {
            padding: 20px;
            background-color: #fdf6f0;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .zoom:hover {
            transform: scale(1.05);
            transition: transform .2s;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ===================== CARGA DE DATOS =====================
chocoframe = pd.read_excel("chocodataa.xlsx")

# Conversión de columnas
conv_booleanos = chocoframe.columns[1:19]
chocoframe[conv_booleanos] = chocoframe[conv_booleanos].astype(bool)

conv_float = chocoframe.columns[19:34]
chocoframe[conv_float] = chocoframe[conv_float].apply(pd.to_numeric, errors='coerce').astype(float)

conv_string = chocoframe.columns[34:37]
chocoframe[conv_string] = chocoframe[conv_string].astype(str)

# ===================== NAVEGACIÓN =====================
paginas = ['Inicio', 'Experiencia']
pagina_seleccionada = st.sidebar.selectbox('🍫 Menú', paginas)

# ===================== INICIO =====================
if pagina_seleccionada == 'Inicio':
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstrito.png", width=120)
    st.markdown("<div class='custom-title'>¡Vamos a comer chocolate!</div>", unsafe_allow_html=True)

    # Estado de navegación
    if "step" not in st.session_state:
        st.session_state.step = "start"
    if "current_filtered_frame" not in st.session_state:
        st.session_state.current_filtered_frame = chocoframe.copy()

    def reset_chat():
        st.session_state.step = "start"
        st.session_state.current_filtered_frame = chocoframe.copy()

    # === Paso 1: ¿Deseas chocolate? ===
    if st.session_state.step == "start":
        with st.container():
            st.subheader("¿Tienes antojo de chocolate? 🍬")
            col1, col2 = st.columns(2)
            if col1.button("Sí, claro 😋"):
                st.session_state.step = "tipo_chocolate"
            if col2.button("No, gracias 🙃"):
                st.warning("Está bien. ¡Hasta la próxima!")

    # === Paso 2: Tipo de chocolate ===
    elif st.session_state.step == "tipo_chocolate":
        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20cocinando.png", width=120)
        with st.container():
            st.subheader("¿Qué tipo de chocolate prefieres?")
            choice = st.radio("", [
                "Solo chocolate",
                "Hecho en su mayoría de chocolate",
                "Con acentos de chocolate"
            ])
            if st.button("Siguiente ➡️"):
                if choice == "Solo chocolate":
                    st.session_state.step = "mani_almendras"
                elif choice == "Hecho en su mayoría de chocolate":
                    st.session_state.step = "hecho_mayoria"
                else:
                    st.session_state.step = "acentos"

    # === Paso 3: Maní o Almendras ===
    elif st.session_state.step == "mani_almendras":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[
            chocoframe['barra de chocolate'] == True
        ]
        with st.container():
            st.subheader("¿Quieres maní o almendras?")
            choice = st.radio("", [
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

            if st.button("Siguiente ➡️"):
                st.session_state.step = "tipo_final"

    # === Paso 4: Tipo final ===
    elif st.session_state.step == "tipo_final":
        with st.container():
            st.subheader("¿Qué tipo de chocolate prefieres?")
            choice = st.radio("", ["Con leche", "Blanco", "Puro"])
            col_map = {
                "Con leche": "chocolate con leche",
                "Blanco": "chocolate blanco",
                "Puro": "chocolate puro"
            }
            col = col_map[choice]
            st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe[col] == True]

            if not st.session_state.current_filtered_frame.empty:
                st.success("✨ ¡Estos chocolates son perfectos para ti!")
                st.dataframe(st.session_state.current_filtered_frame)
            else:
                st.warning("Uy... no encontramos chocolates con esas preferencias 😢")

            st.button("🔁 Reiniciar", on_click=reset_chat)

        # === Postres finales ===
        st.subheader("Postres de chocolate ❤️")
        cols = st.columns(4)
        with cols[0]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolatito.png", width=100, caption="Chocolate")
        with cols[1]:
            st.image("https://github.com/grechiiii/de-mi-mena-/blob/main/image/brownie.png?raw=true", width=100, caption="Brownie")
        with cols[2]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/torta.png", width=100, caption="Quequito")
        with cols[3]:
            st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/galletita.png", width=100, caption="Galletita")

        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20comiendo.png", width=120)
        st.markdown("<p style='text-align: center;'>¡Gracias por usar nuestro asistente! 🥰</p>", unsafe_allow_html=True)

# ===================== EXPERIENCIA =====================
else:
    st.markdown("<h1 style='text-align: center;'>🌱 Beneficios del chocolate</h1>", unsafe_allow_html=True)
    st.write("""
    El chocolate oscuro tiene antioxidantes, mejora el estado de ánimo, y puede ser una experiencia sensorial maravillosa. 
    Combinado con ingredientes como frutos secos o frutas, ¡es aún mejor! 🌰🍓
    """)
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolates.jpg", use_column_width=True)

