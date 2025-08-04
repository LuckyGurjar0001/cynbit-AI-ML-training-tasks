import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re

def scrape_quotes():
    """Scrape quotes from multiple pages"""
    base_url = "http://quotes.toscrape.com/page/{}/"
    all_quotes = []
    
    for page in range(1, 6):  # Scrape first 5 pages
        print(f"Scraping page {page}...")
        response = requests.get(base_url.format(page))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            
            all_quotes.append({
                'quote': text,
                'author': author,
                'tags': ', '.join(tags)
            })
    
    return pd.DataFrame(all_quotes)

def analyze_data(df):
    """Analyze the scraped data"""
    # Most frequent words (excluding common words)
    all_words = ' '.join(df['quote']).lower()
    words = re.findall(r'\b\w{4,}\b', all_words)  # Only words with 4+ letters
    stopwords = {'that', 'this', 'with', 'have', 'your', 'they'}
    meaningful_words = [word for word in words if word not in stopwords]
    word_counts = Counter(meaningful_words).most_common(15)
    
    # Top authors
    top_authors = df['author'].value_counts().head(10)
    
    return {
        'word_counts': word_counts,
        'top_authors': top_authors,
        'total_quotes': len(df),
        'unique_authors': df['author'].nunique()
    }

# Main execution
if __name__ == "__main__":
    print("Starting web scraping...")
    quotes_df = scrape_quotes()
    quotes_df.to_csv('quotes_data.csv', index=False)
    print("Saved data to quotes_data.csv")
    
    analysis = analyze_data(quotes_df)
    print("\n=== Analysis Results ===")
    print(f"Total Quotes Collected: {analysis['total_quotes']}")
    print(f"Unique Authors: {analysis['unique_authors']}")
    print("\nTop 15 Words:")
    for word, count in analysis['word_counts']:
        print(f"{word}: {count}")
    print("\nTop Authors:")
    print(analysis['top_authors'])