import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
from wordcloud import WordCloud

# Load the dataset
df = pd.read_csv('flipkart_product.csv')

# Data Cleaning
# 1. Clean Price column (remove non-numeric characters)
df['Price'] = df['Price'].str.replace('[^\d.]', '', regex=True).astype(float)

# 2. Clean Rate column (convert to numeric, handle any non-numeric values)
df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')

# Drop rows with missing values in Rate column
df = df.dropna(subset=['Rate'])

# Basic statistics
print("=== Basic Statistics ===")
print(f"Total products: {len(df['ProductName'].unique())}")
print(f"Total reviews: {len(df)}")
print(f"Average price: ₹{df['Price'].mean():.2f}")
print(f"Average rating: {df['Rate'].mean():.1f}/5")

# Product analysis
print("\n=== Product Analysis ===")
product_stats = df.groupby('ProductName').agg({
    'Price': 'mean',
    'Rate': 'mean',
    'Review': 'count'
}).rename(columns={'Review': 'ReviewCount'}).sort_values('ReviewCount', ascending=False)

print(product_stats)

# Rating distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='Rate', data=df)
plt.title('Distribution of Ratings')
plt.xlabel('Rating (1-5)')
plt.ylabel('Count')
plt.savefig('rating_distribution.png')  # Save the plot
plt.show()

# Sentiment analysis
def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

df['Sentiment'] = df['Summary'].apply(get_sentiment)

# Sentiment distribution
plt.figure(figsize=(8, 6))
df['Sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Sentiment Analysis of Reviews')
plt.ylabel('')
plt.savefig('sentiment_analysis.png')  # Save the plot
plt.show()

# Price vs Rating analysis
plt.figure(figsize=(10, 6))
sns.boxplot(x='Rate', y='Price', data=df)
plt.title('Price Distribution by Rating')
plt.xlabel('Rating')
plt.ylabel('Price (₹)')
plt.savefig('price_vs_rating.png')  # Save the plot
plt.show()

# Most common words in reviews
all_reviews = ' '.join(df['Summary'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)

plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Reviews')
plt.savefig('wordcloud.png')  # Save the plot
plt.show()

# Save cleaned data
df.to_csv('cleaned_flipkart_reviews.csv', index=False)
print("\nCleaned data saved to 'cleaned_flipkart_reviews.csv'")