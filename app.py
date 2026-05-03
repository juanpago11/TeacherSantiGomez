import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="Texto a Audio",
    page_icon="🔊",
    layout="wide"
)

# ======================
# ESTILOS PRO
# ======================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #146AEF;
}

.block-container {
    padding: 2rem;
}

.card {
    background-color: #1E222A;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #2C2F36;
    margin-bottom: 20px;
}

textarea {
    background-color: #1E222A !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid #146AEF !important;
}

.stSelectbox div {
    background-color: #1E222A !important;
    color: white !important;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    background-color: #146AEF;
    color: white;
    border: none;
    padding: 12px;
    font-size: 16px;
}

.stButton button:hover {
    background-color: #0d4fc2;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
col1, col2 = st.columns([1,2])

with col1:
    try:
        image = Image.open('gato_raton.png')
        st.image(image, width=250)
    except:
        pass

with col2:
    st.title("Conversión de Texto a Audio")
    st.markdown("Convierte cualquier texto en audio de forma rápida y sencilla")

st.markdown("---")

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.subheader("Instrucciones")
    st.markdown("Escribe o pega un texto y conviértelo en audio.")

# ======================
# TEMP FOLDER
# ======================
try:
    os.mkdir("temp")
except:
    pass

# ======================
# FABULA
# ======================
st.markdown("## Ejemplo")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Una pequeña fábula")
    st.write(
        '¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '
        'Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. '
        'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '
        'la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. '
        'Franz Kafka.'
    )

    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# INPUT
# ======================
st.markdown("## Tu texto")
text = st.text_area("Escribe aquí el texto")

# ======================
# IDIOMA
# ======================
col1, col2 = st.columns(2)

with col1:
    option_lang = st.selectbox("Selecciona el lenguaje", ("Español", "English"))

if option_lang == "Español":
    lg = 'es'
else:
    lg = 'en'

# ======================
# FUNCION
# ======================
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# ======================
# BOTON
# ======================
if st.button("Convertir a Audio"):
    if text.strip() == "":
        st.warning("Por favor escribe un texto")
    else:
        with st.spinner("Generando audio..."):
            result, output_text = text_to_speech(text, 'com', lg)

        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("## Resultado")
        st.audio(audio_bytes, format="audio/mp3")

        with open(f"temp/{result}.mp3", "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio"), unsafe_allow_html=True)

# ======================
# LIMPIEZA
# ======================
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)

# ======================
# FOOTER
# ======================
st.markdown("---")
st.markdown('<div class="footer">Texto a Audio | Juan Pablo Gomez</div>', unsafe_allow_html=True)
