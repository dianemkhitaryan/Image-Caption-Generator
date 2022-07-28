import cv2
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
url = "http://127.0.0.1:5000/Submit"


try:
    os.mkdir("temp")
except:
    pass


@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img


st.set_page_config(layout="centered")
st.title(" IMAGE CAPTIONING")
st.write("\n")
st.write("\n")
st.subheader("Upload an Image")
uploaded_files = st.file_uploader(
    "", type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
if st.button('Process'):
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            files = {"file": uploaded_file.getvalue()}
            f = uploaded_file.name
            data = {"FileName": f}
            file_details = {"FileName": uploaded_file.name,
                            "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        # st.write(file_details)
            img = load_image(uploaded_file)
        # st.snow()
        # st.balloons()
            st.image(img, width=700)
        #st.spinner(text="Predicted result is ....")
            result = requests.get(url, json=data)
            d = result.json()
            print(d)
            st.success(d['label'])
            text = d['label']
            tts = gTTS(text, slow=False)
            try:
                my_file_name = text[0:100]
            except:
                my_file_name = "audio"
            tts.save(f"temp/{my_file_name}.mp3")
            audio_file = open(f"temp/{text}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

    else:
        st.error('Result')
# if st.button("Open Camera"):
    # cam = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = cam.read()
    #     if not ret:
    #         print("failed to grab frame")
    #         break
    #     cv2.imshow("Image Captioning Generator", frame)
    #     k = cv2.waitKey(1)
    #     if k % 256 == 27:
    #         print("Escape hit, closing...")
    #         break
    #     elif k % 256 == 32:
    #         img_name = "1111.jpg"
    #         img_pth = 'Flicker8k_Dataset/' + img_name
    #         cv2.imwrite(img_pth, frame)
    #         st.image(img_pth, width=700)
    #         data = {"FileName": img_name}
    #         # result = requests.get(url, json=data)
    #         # d = result.json()
    #         # print(d)
    #         # st.success(d['label'])
    #         # text = d['label']
    #         tts = gTTS(text, slow=False)
    #         try:
    #             my_file_name = text[0:100]
    #         except:
    #             my_file_name = "audio"
    #         tts.save(f"temp/{my_file_name}.mp3")
    #         audio_file = open(f"temp/{text}.mp3", "rb")
    #         audio_bytes = audio_file.read()
    #         st.audio(audio_bytes, format="audio/mp3", start_time=0)
    #         break

        

            
    cam.release()
    cv2.destroyAllWindows()
