import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("xAPI-Edu-Data.csv")

# 1️⃣ App Title
st.title("📚 Student Performance Dashboard")

# 2️⃣ Summary Section
st.header("📊 Data Summary")
st.write(df.describe(include='all'))

# 3️⃣ Cleaning Explanation
st.header("🧹 Data Cleaning Steps")
st.markdown("""
- Encoded Yes/No → 1/0  
- Gender M/F → 1/0  
- One-hot encoded categorical values  
- Removed duplicates and handled nulls  
""")

# 4️⃣ Visualizations
st.header("📈 Visualizations")

st.subheader("Class Distribution")
sns.countplot(x='Class', data=df)
st.pyplot(plt.gcf())  # Shows the Seaborn plot

plt.clf()  # Clear the figure for next plot

st.subheader("Class vs Gender")
sns.countplot(x='gender', hue='Class', data=df)
st.pyplot(plt.gcf())

# 5️⃣ Filter Example
st.sidebar.header("🔎 Filter")
gender = st.sidebar.selectbox("Choose Gender", df['gender'].unique())
filtered = df[df['gender'] == gender]
st.write(filtered.head())

# 6️⃣ Insights
st.header(" Key Insights")
st.markdown("""
- Students with more 'raised hands' perform better.  
- Attendance plays a role in final grade.  
- Parental satisfaction may affect performance.
""")
