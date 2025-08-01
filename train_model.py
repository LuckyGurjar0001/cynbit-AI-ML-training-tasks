# train_model.py
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Load and prepare data
df = pd.concat([pd.read_csv("Fake.csv").assign(label=0),
                pd.read_csv("True.csv").assign(label=1)])

# Clean text
df['clean_text'] = df['text'].str.lower().str.replace(r'[^\w\s]', '')

# Vectorize
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(df['clean_text'])
y = df['label']

# Train and save model
model = RandomForestClassifier()
model.fit(X, y)
joblib.dump(model, 'model.joblib')
joblib.dump(vectorizer, 'vectorizer.joblib')
print("Model trained and saved!")