import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress TensorFlow logs
from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    points = summary[0]['summary_text'].split('. ')
    return [f"{i+1}. {point.strip()}." for i, point in enumerate(points) if point.strip()][:5]

if __name__ == "__main__":
    print("Paste your text (Ctrl+Z + Enter on Windows to finish):")
    text = ""
    while True:
        try:
            line = input()
            text += line + "\n"
        except EOFError:  # Ctrl+Z triggers this
            break
    
    if text.strip():
        print("\nSummary:")
        for point in summarize_text(text):
            print(point)
    else:
        print("No text provided!")