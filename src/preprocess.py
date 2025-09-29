import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    tokens = [WordNetLemmatizer().lemmatize(w) 
              for w in text.split() 
              if w not in stopwords.words('english') and len(w) > 2]
    return " ".join(tokens)