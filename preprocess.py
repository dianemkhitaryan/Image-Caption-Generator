import os
import pickle
import numpy as np
from tqdm.notebook import tqdm
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model


#Base and working direction
BASE_DIR    = 'Flickr8k_Dataset'
WORKING_DIR = 'Models'

# load vgg16 model
def Load_model():
    model = load_model('Models/best_model.h5')
    return model

#extract features from image
def extract_features(model):
    features = {}
    directory = BASE_DIR
    for img_name in tqdm(os.listdir(BASE_DIR)):
        img_path = directory + '/' + img_name
        image = load_img(img_path, target_size=(224, 224))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        feature = model.predict(image, verbose=0)
        image_id = img_name.split('.')[0]
        features[image_id] = feature
        pickle.dump(features, open(os.path.join(WORKING_DIR, 'features.pkl'), 'wb'))

#loading the features from pickle
def load_features():
    with open(os.path.join(WORKING_DIR, 'features.pkl'), 'rb') as f:
        features = pickle.load(f)
    return features

#reading captions
def read_caption():
    with open(os.path.join(WORKING_DIR, 'captions.txt'), 'r') as f:
        next(f)
        captions_doc = f.read()
    mapping = {}
    for line in tqdm(captions_doc.split('\n')):
        tokens = line.split(',')
        if len(line) < 2:
            continue
        image_id, caption = tokens[0], tokens[1:]
        image_id = image_id.split('.')[0]
        caption = " ".join(caption)
        if image_id not in mapping:
            mapping[image_id] = []
        mapping[image_id].append(caption)
    return mapping


#clean mapping
def clean(mapping):
    for key, captions in mapping.items():
        for i in range(len(captions)):
            caption = captions[i]
            caption = caption.lower()
            caption = caption.replace('[^A-Za-z]', '')
            caption = caption.replace('\s+', ' ')
            caption = '<start>' + " ".join([word for word in caption.split() if len(word)>1]) + '<end>'
            captions[i] = caption
    return captions

#adding captions in array
def caption_array(mapping):
    all_captions = []
    for key in mapping:
        for caption in mapping[key]:
            all_captions.append(caption)
    max_length = max(len(caption.split()) for caption in all_captions)

    return all_captions, max_length


#tokenize the text
def tokenizer(all_captions):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(all_captions)
    vocab_size = len(tokenizer.word_index) + 1
    return tokenizer, vocab_size