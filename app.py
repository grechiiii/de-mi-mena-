import streamlit as st
import pandas as pd

# ===================== ESTILO Y FONDO =====================
st.markdown("""
    <style>
        /* Fondo con chocolate */
        .stApp {
            background-image: url('https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/Fondo%20para%20una%20parte.png');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            font-family: 'Comic Sans MS', cursive;
        }

        /* Fondo marrón del sidebar */
        [data-testid="stSidebar"] {
            background-color: #d7b49e;
        }

        /* Texto centrado con sombra */
        .titulo {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #3e2723;
            text-shadow: 2px 2px 6px #ffffff;
            margin-top: 10px;
        }

        /* Botones marrones */
        .stButton>button {
            background-color: #8d6e63;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            margin: 5px;
        }

        .pregunta {
            text-align: center;
            font-size: 22px;
            color: #4e342e;
            font-weight: normal;
            margin-bottom: 10px;
        }

        .container {
            background-color: rgba(255,255,255,0.85);
            border-radius: 18px;
            padding: 30px;
            margin-top: 40px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.2);
        }

        .sidebar-image {
            border-radius: 10px;
            margin-top: 30px;
            margin-left: auto;
            margin-right: auto;
            display: block;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR CON IMAGEN =====================
with st.sidebar:
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolates%20tres%20tipos.png", caption="Tipos de chocolate", use_column_width=True)

# ===================== CONTENIDO PRINCIPAL =====================
# Mounstrito centrado arriba
st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstrito.png", width=150)

# Caja blanca con contenido central
with st.container():
    st.markdown("<div class='container'>", unsafe_allow_html=True)

    # Título principal
    st.markdown("<div class='titulo'>Vamos a comer un chocolate</div>", unsafe_allow_html=True)

    # Pregunta dulce
    st.markdown("<p class='pregunta'>¿Te provoca algo dulce?</p>", unsafe_allow_html=True)

    # Botones centrados
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sí"):
            st.session_state.step = "tipo_chocolate"
    with col2:
        if st.button("No"):
            st.info("¡Está bien! Vuelve cuando tengas hambre 😋")

    st.markdown("</div>", unsafe_allow_html=True)

# ===================== DATOS =====================
chocoframe = pd.read_excel("chocodataa.xlsx")
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
    with st.container():
        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstrito.png", width=120)
        st.markdown("<div class='title-box'><h1>¡Vamos a comer chocolate!</h1></div>", unsafe_allow_html=True)

    if "step" not in st.session_state:
        st.session_state.step = "start"
    if "current_filtered_frame" not in st.session_state:
        st.session_state.current_filtered_frame = chocoframe.copy()

    def reset_chat():
        st.session_state.step = "start"
        st.session_state.current_filtered_frame = chocoframe.copy()

    # === Paso 1 ===
    if st.session_state.step == "start":
        st.subheader("¿Te provoca algo dulce?")
        col1, col2 = st.columns(2)
        if col1.button("Sí 🥺"):
            st.session_state.step = "tipo_chocolate"
        if col2.button("No 😅"):
            st.warning("¡Ok! Te esperamos con hambre la próxima vez.")

    # === Paso 2 ===
    elif st.session_state.step == "tipo_chocolate":
        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20cocinando.png", width=120)
        st.subheader("¿Qué tipo de chocolate quieres?")
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

    # === Paso 3 ===
    elif st.session_state.step == "mani_almendras":
        st.session_state.current_filtered_frame = st.session_state.current_filtered_frame.loc[chocoframe['barra de chocolate'] == True]
        st.subheader("¿Maní o almendras?")
        choice = st.radio("", ["Con maní", "Sin maní", "Con Almendras", "Sin Almendras"])
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

    # === Paso 4 ===
    elif st.session_state.step == "tipo_final":
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
            st.success("✨ ¡Estos chocolates son ideales para ti!")
            st.dataframe(st.session_state.current_filtered_frame)
        else:
            st.warning("No encontramos chocolates con esas preferencias 😢")

        st.button("🔁 Reiniciar", on_click=reset_chat)

        # ========== GALERÍA DE POSTRES FLOTANTE ==========
        st.markdown("<div class='floating-gallery'>", unsafe_allow_html=True)

        def floating_img(url, caption):
            st.markdown(f"""
                <div>
                    <img src="{url}" width="120" class="hover-image">
                    <div class="gallery-caption">{caption}</div>
                </div>
            """, unsafe_allow_html=True)

        floating_img("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolatito.png", "Chocolate 🍫")
        floating_img("https://github.com/grechiiii/de-mi-mena-/blob/main/image/brownie.png?raw=true", "Brownie 🟤")
        floating_img("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/torta.png", "Quequito 🎂")
        floating_img("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/galletita.png", "Galletita 🍪")

        st.markdown("</div>", unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/mounstro%20comiendo.png", width=120)
        st.markdown("<p style='text-align: center;'>¡Gracias por usar nuestro recomendador! 💘</p>", unsafe_allow_html=True)

# ===================== EXPERIENCIA =====================
else:
    st.markdown("<h1>🌟 Beneficios del chocolate</h1>", unsafe_allow_html=True)
    st.write("""
    El chocolate, especialmente el oscuro, es fuente de antioxidantes, energía y felicidad. 
    Tiene efectos positivos en el ánimo, el corazón y el alma. 
    ¡Perfecto para compartir contigo y con quien más quieres! 💛
    """)
    st.image("https://raw.githubusercontent.com/grechiiii/de-mi-mena-/refs/heads/main/image/chocolates.jpg", use_column_width=True)
