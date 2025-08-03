import streamlit as st
import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors

# Load the preprocessed data and models
data = joblib.load('student_matcher_models.pkl')
df = data['df']
tfidf = data['tfidf']
knn_model = data['knn_model']
kmeans = data['kmeans']

# Streamlit app
st.title("🎯 Student Skill Matcher")
st.subheader("Find your perfect tech collaboration match!")

# Input section
st.sidebar.header("Your Skills & Interests")

# Skill inputs
python_skill = st.sidebar.selectbox("Python skill level:", ['Weak', 'Average', 'Strong'])
sql_skill = st.sidebar.selectbox("SQL skill level:", ['Weak', 'Average', 'Strong'])
java_skill = st.sidebar.selectbox("Java skill level:", ['Weak', 'Average', 'Strong'])

# Interest input
interest = st.sidebar.text_input("Your primary interest domain (e.g., AI, Web Dev):")
career_goal = st.sidebar.text_input("Your future career goal:")
project_exp = st.sidebar.text_input("Your project experience:")

# Filter by domain
domain_filter = st.sidebar.selectbox("Filter by domain:", 
                                   ['All'] + sorted(df['Interested Domain'].unique().tolist()))

# Process input
if st.sidebar.button("Find Matches"):
    # Create input feature string
    skill_mapping = {'Weak': 0, 'Average': 1, 'Strong': 2}
    input_text = (f"Python_{skill_mapping[python_skill]} SQL_{skill_mapping[sql_skill]} "
                 f"Java_{skill_mapping[java_skill]} Domain_{interest} Career_{career_goal} "
                 f"Project_{project_exp}")
    
    # Vectorize input
    input_vector = tfidf.transform([input_text])
    
    # Find nearest neighbors
    distances, indices = knn_model.kneighbors(input_vector)
    
    # Get recommendations
    recommendations = df.iloc[indices[0][1:]]  # Skip first which is the input itself
    
    # Apply domain filter if selected
    if domain_filter != 'All':
        recommendations = recommendations[recommendations['Interested Domain'] == domain_filter]
    
    # Display results
    st.success("Here are your top collaboration matches:")
    
    for i, (_, row) in enumerate(recommendations.head(3).iterrows(), 1):
        match_score = 100 * (1 - distances[0][i])  # Convert cosine distance to percentage
        
        st.subheader(f"Match #{i}: {row['Name']} ({match_score:.1f}% match)")
        st.write(f"**Skills:** Python: {row['Python']}, SQL: {row['SQL']}, Java: {row['Java']}")
        st.write(f"**Interested Domain:** {row['Interested Domain']}")
        st.write(f"**Career Goal:** {row['Future Career']}")
        st.write(f"**Project Experience:** {row['Projects']}")
        st.write(f"**GPA:** {row['GPA']}")
        st.write("---")
    
    # Show cluster visualization (bonus)
    st.subheader("Your Skill Cluster")
    input_cluster = kmeans.predict(input_vector)[0]
    cluster_members = df[df['Cluster'] == input_cluster]
    
    st.write(f"You belong to a cluster with {len(cluster_members)} students who have similar skills/interests.")
    st.write("Common skills in this cluster:")
    
    # Calculate average skills for the cluster
    avg_python = cluster_members['Python'].mean()
    avg_sql = cluster_members['SQL'].mean()
    avg_java = cluster_members['Java'].mean()
    
    st.write(f"- Python: {'Strong' if avg_python > 1.5 else 'Average' if avg_python > 0.5 else 'Weak'}")
    st.write(f"- SQL: {'Strong' if avg_sql > 1.5 else 'Average' if avg_sql > 0.5 else 'Weak'}")
    st.write(f"- Java: {'Strong' if avg_java > 1.5 else 'Average' if avg_java > 0.5 else 'Weak'}")
    
    st.write("Common interest domains:")
    top_domains = cluster_members['Interested Domain'].value_counts().head(3)
    for domain, count in top_domains.items():
        st.write(f"- {domain} ({count} students)")