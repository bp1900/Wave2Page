import shutil
import subprocess
import traceback
from PIL import Image
import streamlit as st
import main

path_to_root_folder = '../'

# @st.cache_data

#########################################################################################
####################################### INTERFACE #######################################
#########################################################################################
from tempfile import NamedTemporaryFile
try:
    st.title("Wave2Page")
    image = Image.open(path_to_root_folder+'images/w2pLogo.png')
    # _, second, _ = st.columns([5,3,5])
    st.image(image, caption='Developed by Gerard Caravaca, Benjami Parellada and Armando Rodriguez')

    first, second = st.columns([9,2])
    first.header("Subtitle of Wave2Page")

    uploaded_file = st.file_uploader("Choose a file",type=[".wav"])
    if uploaded_file is not None:
        with NamedTemporaryFile(dir='.', suffix='.wav') as f:
            f.write(uploaded_file.getbuffer())
            path_to_audio = path_to_root_folder+"data/audio/"+uploaded_file.name
            shutil.copy(f.name, path_to_audio)
            subprocess.call(['python3', "main.py", path_to_audio, "--separate", "--wav2midi", "--midi2sheet"])
    
except Exception as e:
    traceback.print_exc()
    print(e)
    st.error('Unexpected error. Try again. If the error persist, please contact the administrators. ', icon="🚨")
