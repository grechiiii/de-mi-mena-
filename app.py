import streamlit as st
import pandas as pd

# ===================== CSS SUPER CUIDADO =====================
st.markdown("""
    <style>
        .stApp {
            background-color: #fefdfb;
            font-family: 'Trebuchet MS', sans-serif;
        }

        h1, h2, h3 {
            color: #4e342e;
            text-align: center;
        }

        .stButton>button {
            background-color: #8d6e63;
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 10px 20px;
        }

        .stRadio > div {
            background-color: #fceee3;
            padding: 12px;
            border-radius: 12px;
        }

        .hover-image {
            transition: transform .3s ease;
            border-radius: 12px;
        }

        .hover-image:hover {
            transform: scale(1.15);
            cursor: pointer;
        }

        .floating-gallery {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
            padding: 30px 10px;
            background-color: #f8f4f0;
            border-top: 2px solid #d7ccc8;
            margin-top: 30px;
        }

        .gallery-caption {
            text-align: center;
            font-size: 14px;
            color: #5d4037;
            margin-top: 5px;
        }

        .title-box {
            background-color: #fff8f1;
            padding: 20px;
            border-radius: 20px;
            margin: 30px 0;
        }
    </style>
""", unsafe_allow_html=True)

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
