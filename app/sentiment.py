# importing necessary packages
import pandas as pd
import matplotlib

matplotlib.use("Agg")
from keras_preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from .models import loadModel
import numpy as np


import re
from nltk.corpus import stopwords

stop = set(stopwords.words("english"))


MAX_LEN = 1000
tokenizer_obj = Tokenizer()


# list of all mobile review files
listt = [
    "./data/samsung3.csv",
    "./data/Iphone4.csv",
    "./data/Redmi2.csv",
    "./data/GalaxyNote5.csv",
    "./data/Honor6.csv",
    "./data/Motorolla7.csv",
    "./data/OnePlus8.csv",
    "./data/Nokia9.csv",
    "./data/Oppo10.csv",
    "./data/Vivo1.csv",
]

# list of all laptop review files
listt2 = [
    "./data/lk/AsusVivoBook10.csv",
    "./data/lk/HP-Pavilion1.csv",
    "./data/lk/LenovoPad2.csv",
    "./data/lk/MacBookAir3.csv",
    "./data/lk/AcerAspire4.csv",
    "./data/lk/Dell5.csv",
    "./data/lk/RazorBlade6.csv",
    "./data/lk/surface7.csv",
    "./data/lk/mi-notebook8.csv",
    "./data/lk/samsungChromeBook9.csv",
]


def get_score(product_id):
    """this function will scrap the reviews from the selected mobile phone file and feed it to the model

    Args : product_id (int)

    Returns
          list containg reviews and no of positive and negative reviews

    """
    lt = []
    for l in listt:
        if str(product_id) in l:
            data = pd.read_csv(l, encoding="latin-1")
            rev = data["Reviews"]
            data["Reviews"] = data["Reviews"].apply(lambda x: clean_text(x))

            testX, testY = data.Reviews.astype(str), data.Verdict

            tokenizer_obj.fit_on_texts(testX)
            sequences = tokenizer_obj.texts_to_sequences(testX)
            text = pad_sequences(sequences, maxlen=MAX_LEN)

            # Evaluates the loaded model on product review data
            loadModel.reconstructed_model.fit(text, testY)
            result = loadModel.reconstructed_model.predict(text)
            oneD_array = np.ravel(result)

            # reviews with predicted sentiment score greater then 0.5 are labeled '1' while other labeled as '0'
            pred_sentiment = np.array(
                list(map(lambda x: 1 if x > 0.5 else 0, oneD_array))
            )

            # count the number of 0's and 1's
            t1 = np.count_nonzero(pred_sentiment)
            f1 = pred_sentiment.size - t1

            lt = [t1, f1, rev]

    return lt


def get_score_laptop(product_id):

    """this function will scrap the reviews from the selected laptop file and feed it to the model

    Args : product_id (int)

    Returns
          list containg reviews and no of positive and negative reviews

    """

    lt = []
    for l in listt2:
        if str(product_id) in l:
            data = pd.read_csv(l, encoding="latin-1")
            rev = data["Reviews"]
            data["Reviews"] = data["Reviews"].apply(lambda x: clean_text(x))
            # data['Reviews'] = ''.join([i for i in data['Reviews'][1] if not i.isdigit()])

            testX, testY = data.Reviews, data.Verdict

            tokenizer_obj.fit_on_texts(testX)
            sequences = tokenizer_obj.texts_to_sequences(testX)
            text = pad_sequences(sequences, maxlen=MAX_LEN)

            # Evaluates the loaded model on product review data
            loadModel.reconstructed_model.fit(text, testY)
            result = loadModel.reconstructed_model.predict(text)
            oneD_array = np.ravel(result)

            # reviews with predicted sentiment score greater then 0.5 are labeled '1' while other labeled as '0'
            pred_sentiment = np.array(
                list(map(lambda x: 1 if x > 0.5 else 0, oneD_array))
            )

            # count the number of 0's and 1's
            t1 = np.count_nonzero(pred_sentiment)
            f1 = pred_sentiment.size - t1

            lt = [t1, f1, rev]

    return lt


def clean_text(text):
    text = re.sub("[^a-zA-Z]", " ", str(text))

    text = text.lower()

    text = text.split(" ")

    text = [w for w in text if not w in set(stopwords.words("english"))]

    text = " ".join(text)

    text = re.sub(r"\b\w{1,3}\b", "", text)

    return text
