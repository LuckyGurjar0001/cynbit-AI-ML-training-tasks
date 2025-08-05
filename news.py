import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk

class NewsAnalyzer:
    def __init__(self):
        # Initialize NLTK resources
        self._download_nltk_resources()
        
        # Standard English stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Custom stopwords to add (expand this list as needed)
        self.custom_stopwords = {
            'said', 'will', 'new', 'one', 'us', '...', 'also', 'would',
            'could', 'may', 'might', 'must', 'shall', 'should', 'via',
            'since', 'however', 'yet', 'according', 'like', 'among'
        }
        
        # Common contractions to remove
        contractions = {
            "'s", "'re", "'ve", "'d", "'ll", "'m", "n't", "'t"
        }
        
        # Combine all stopwords
        self.stop_words.update(self.custom_stopwords)
        self.stop_words.update(contractions)

    def _download_nltk_resources(self):
        """Ensure all required NLTK resources are available"""
        resources = {
            'tokenizers/punkt': 'punkt',
            'corpora/stopwords': 'stopwords',
            'tokenizers/punkt_tab/english': 'punkt_tab'
        }
        
        for path, package in resources.items():
            try:
                nltk.data.find(path)
            except LookupError:
                nltk.download(package)

    def scrape_headlines(self, url, max_headlines=30):
        """Scrape headlines from a news website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = []
            
            # Try different selectors for different sites
            selectors = [
                ('h3', {}),
                ('h2', {}),
                ('h1', {}),
                ('[class*="headline"]', {}),
                ('article h3', {}),
                ('a', {'class': 'headline'}),
                ('div', {'class': 'headline'})
            ]
            
            for selector, attrs in selectors:
                if len(headlines) >= max_headlines:
                    break
                elements = soup.find_all(selector, attrs)
                headlines.extend([h.get_text().strip() for h in elements if h.get_text().strip()])
            
            return list(dict.fromkeys(headlines))[:max_headlines]  # Remove duplicates while preserving order
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

    def preprocess_text(self, text_list):
        """Process text to extract meaningful keywords with enhanced stopword removal"""
        keywords = []
        for text in text_list:
            # Remove punctuation and lowercase
            text = text.translate(str.maketrans('', '', string.punctuation))
            
            # Tokenize and clean
            words = word_tokenize(text.lower())
            
            # Filter words
            words = [
                w for w in words 
                if (w.isalpha() and  # Only alphabetic
                   len(w) > 2 and    # Minimum length
                   w not in self.stop_words)  # Not in stopwords
            ]
            
            keywords.extend(words)
        
        return keywords

    # [Rest of your methods (get_top_keywords, plot_bar_chart, generate_wordcloud) remain the same]
    def get_top_keywords(self, keywords, top_n=5):
        """Get most common keywords"""
        return Counter(keywords).most_common(top_n)

    def plot_bar_chart(self, top_keywords):
        """Create bar chart of top keywords"""
        words, counts = zip(*top_keywords)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(words, counts, color='skyblue')
        ax.set_title("Top Trending Topics", pad=20)
        ax.set_ylabel("Frequency")
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig

    def generate_wordcloud(self, keywords):
        """Generate word cloud from keywords"""
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100
        ).generate(' '.join(keywords))
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        plt.tight_layout()
        return fig