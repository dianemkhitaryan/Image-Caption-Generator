import os
import pickle
import numpy as np
from tqdm.notebook import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.translate.bleu_score import corpus_bleu
from PIL import Image
import matplotlib.pyplot as plt
import re
import preprocess

BASE_DIR    = 'Flicker8k_Dataset/'
WORKING_DIR = 'Models/'
#index to word function
def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# generate caption for an image
def predict_caption(model, image, tokenizer, max_length):
    in_text = '<start>'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], max_length)
        yhat = model.predict([image, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == '<end>':
            break
    return in_text


# validate with test data
def validate_text(test, mapping, features, tokenizer, max_length, model):
    actual, predicted = list(), list()

    for key in tqdm(test):
        captions = mapping[key]
        y_pred = predict_caption(model, features[key], tokenizer, max_length)
        actual_captions = [caption.split() for caption in captions]
        y_pred = y_pred.split()
        actual.append(actual_captions)
        predicted.append(y_pred)
        return actual, predicted

# calcuate BLEU score
def BLEU_score(actual, predicted):
    return "BLEU-1: %f" % corpus_bleu(actual, predicted, weights=(1.0, 0, 0, 0)), "BLEU-2: %f" % corpus_bleu(actual, predicted, weights=(0.5, 0.5, 0, 0))

#generate caption
def generate_caption(image_name, mapping, model, features, tokenizer, max_length):
    image_id = image_name.split('.')[0]
    # print(image_name)
    directory = BASE_DIR
    img_path = directory + image_name
    # img_path = os.path.join(BASE_DIR, image_name)
    print(os.getcwd())
    # image = Image.open(image_name)
    captions = mapping[image_id]
    print('---------------------Actual---------------------')
    i = 1
    for caption in captions:
      caption = re.sub('<start>', '', caption)
      caption = re.sub('<end>', '', caption)

      print(f"{i}- " + caption)
      i+=1
    y_pred = predict_caption(model, features[image_id], tokenizer, max_length)
    print('--------------------Predicted--------------------')
    y_pred = re.sub('end.*', '', y_pred)
    y_pred = re.sub('<start>', '', y_pred)
    print(y_pred)
    # plt.imshow(image)
    return y_pred


def pred(img_name):
    mapping = preprocess.read_caption()
    preprocess.clean(mapping)
    model = preprocess.Load_model()
    all_captions, max_length = preprocess.caption_array(mapping)
    features = preprocess.load_features()
    tokenizer, vocab_size = preprocess.tokenizer(all_captions)
    prediction = generate_caption(img_name, mapping, model, features, tokenizer, max_length)
    return prediction