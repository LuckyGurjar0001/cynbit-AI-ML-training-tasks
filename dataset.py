import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import numpy as np

# Load the dataset
df = pd.read_csv('cs_students.csv')

# Data Cleaning
# Convert skill levels to numerical values (0: Weak, 1: Average, 2: Strong)
skill_mapping = {'Weak': 0, 'Average': 1, 'Strong': 2}
for skill in ['Python', 'SQL', 'Java']:
    df[skill] = df[skill].map(skill_mapping)

# Combine skills and interests into a single text feature for vectorization
df['Skills_Interests'] = df.apply(lambda row: 
    f"Python_{row['Python']} SQL_{row['SQL']} Java_{row['Java']} "
    f"Domain_{row['Interested Domain']} Career_{row['Future Career']} "
    f"Project_{row['Projects']}", axis=1)

# Vectorize the combined text feature
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['Skills_Interests'])

# Build two models for recommendation:
# 1. KNN model for similarity-based recommendations
knn_model = NearestNeighbors(n_neighbors=4, metric='cosine')
knn_model.fit(tfidf_matrix)

# 2. K-Means clustering model for grouping similar students
kmeans = KMeans(n_clusters=20, random_state=42)
clusters = kmeans.fit_predict(tfidf_matrix)
df['Cluster'] = clusters

# Save the processed data and models for the Streamlit app
import joblib
joblib.dump({
    'df': df,
    'tfidf': tfidf,
    'knn_model': knn_model,
    'kmeans': kmeans
}, 'student_matcher_models.pkl')