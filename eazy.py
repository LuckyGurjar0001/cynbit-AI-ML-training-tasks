import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Download stopwords if not already
nltk.download('stopwords')

# Step 1: Scrape headlines from Inshorts
url = "https://inshorts.com/en/read"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Extract headlines
headlines = [span.text for span in soup.find_all('span', itemprop='headline')]
print("🔍 Total headlines found:", len(headlines))

# Step 2: Clean text
stop_words = set(stopwords.words("english"))
all_words = []

for title in headlines:
    title = re.sub(r'[^\w\s]', '', title.lower())  # remove punctuation, lowercase
    words = title.split()
    filtered = [word for word in words if word not in stop_words]
    all_words.extend(filtered)

# Step 3: Count words
word_freq = Counter(all_words)
top_keywords = word_freq.most_common(5)
print("🔥 Top 5 Trending Topics:\n", top_keywords)

# Step 4: Visualize
# Bar chart
words, counts = zip(*top_keywords)
plt.bar(words, counts)
plt.title("Top 5 Trending Topics")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.show()
