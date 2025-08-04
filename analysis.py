import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('Quotes Dataset.csv')

# 1. Most frequent words in quotes
all_words = ' '.join(df['Quote']).lower().split()
word_counts = Counter(all_words).most_common(20)

print("Top 20 Most Frequent Words:")
for word, count in word_counts:
    print(f"{word}: {count}")

# 2. Top authors
top_authors = df['Author'].value_counts().head(10)
print("\nTop 10 Authors:")
print(top_authors)

# 3. Visualization
plt.figure(figsize=(10,5))
top_authors.plot(kind='bar')
plt.title('Top 10 Authors by Quote Count')
plt.savefig('authors_plot.png')  