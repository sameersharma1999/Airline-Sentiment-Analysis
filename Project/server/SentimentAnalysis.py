import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings('ignore')
import pickle


class SentimentAnalysis:
    def __init__(self, text):
        self.review = text
        self.copy_review = self.review

        self.emoji_pattern = re.compile("["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)

        self.patterns = ['(http:\/\/[a-z0-9]+\.[a-z]+\/[a-zA-Z0-9#]+\/?)',  # Links
                         '@[A-za-z]+',  # Mail
                         '[^A-Za-z]',  # Punctuation
                         ]

    def clean_text(self):
        for patt in self.patterns:
            self.review = re.sub(pattern=patt,
                                 repl=' ',
                                 string=self.review)

        self.review = self.review.lower()  # Lower case
        self.review = self.review.split()  # List of each words

        # StopWords
        all_stopwords = set(stopwords.words('english'))  # Set of all Stopwords
        all_stopwords.remove('not')

        # Stemming
        ps = PorterStemmer()

        self.review = [ps.stem(word) for word in self.review if word not in all_stopwords]
        self.review = ' '.join(self.review)

    def bag_of_words(self):
        new_corpus = [self.review]

        with open('..\Application\CountVectorizer.pkl', 'rb') as f:
            new_cv = pickle.load(f)

        self.review = new_cv.transform(new_corpus).toarray()

    def predict(self):
        loaded_model = load_model("..\Application\ANN_Model.h5")  # Load the model
        prediction = loaded_model.predict(self.review)

        thresh = 0.5  # Threshold
        prediction = [1 if i[0] > thresh else 0 for i in prediction]

        text = self.copy_review

        if prediction[0] == 1:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'

        data = {'Text': text,
                'Sentiment': sentiment,
                'Model': 'ANN',
                }

        return data
