import streamlit as st
from PIL import Image
import requests
import os
import time
import glob
import os
from gtts import gTTS
from googletrans import Translator
output_language = "en"

try:
    os.mkdir("temp")
except:
    pass

@st.cache

def load_image(image_file):
	img = Image.open(image_file)
	return img


st.set_page_config(layout="centered") ##wide
st.title(" IMAGE CAPTIONING")
st.write("\n")

st.write("\n")
st.subheader("Upload an Image")
uploaded_file = st.file_uploader("",type=['png','jpeg','jpg'])

if st.button('Process'):
    if uploaded_file is not None:
        files = {"file": uploaded_file.getvalue()}
        f = uploaded_file.name
        data = {"FileName": f}
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)
        img = load_image(uploaded_file)
        st.image(img, width=700)
        url = "http://127.0.0.1:5000/Submit"
        result = requests.get(url,json=data)
        d = result.json()
        print(d)
        st.success(d['label'])
        text = d['label']
        #st.write(text)
        tts = gTTS(text,slow=False)
        try:
            my_file_name = text[0:100]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        audio_file = open(f"temp/{text}.mp3", "rb")
        audio_bytes = audio_file.read()
        #st.markdown(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

    else:
        st.error('Result')
        #label = predict(uploaded_file)
        #st.write('%s (%.2f%%)' % (label[1], label[2] * 100))
        #st.write(label)

## code for converting text to speech #######################


#text = d['label']
# st.write(text)

# def text_to_speech(text):
#     tts = gTTS(text,slow=False)
#     try:
#         my_file_name = text[0:20]
#     except:
#         my_file_name = "audio"
#     tts.save(f"temp/{my_file_name}.mp3")
#     return my_file_name

# if st.button("convert"):
#     result = text_to_speech(text)
#     audio_file = open(f"temp/{result}.mp3", "rb")
#     audio_bytes = audio_file.read()
#     st.markdown(f"## Your audio:")
#     st.audio(audio_bytes, format="audio/mp3", start_time=0)

   

# def remove_files(n):
#     mp3_files = glob.glob("temp/*mp3")
#     if len(mp3_files) != 0:
#         now = time.time()
#         n_days = n * 86400
#         for f in mp3_files:
#             if os.stat(f).st_mtime < now - n_days:
#                 os.remove(f)
#                 print("Deleted ", f)

# remove_files(7)         
