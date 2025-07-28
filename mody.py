import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import joblib

# 1. Load dataset
def load_data(file_path):
    return pd.read_csv(file_path, sep=';', names=['text', 'emotion'])

train_df = load_data("train.txt")
val_df = load_data("val.txt")

# 2. Combine train and val for full training
df = pd.concat([train_df, val_df])

# 3. Preprocessing: not needed much, just lowercase (TF-IDF handles tokenizing)
df['text'] = df['text'].str.lower()

# 4. Define Pipeline: TF-IDF + Logistic Regression
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))
])

# 5. Train
model.fit(df['text'], df['emotion'])

# 6. Save model
joblib.dump(model, 'emotion_model.pkl')

print(" Model trained and saved as emotion_model.pkl")
