#  Titanic Survival Predictor


A machine learning web app that predicts passenger survival chances on the Titanic with 82% accuracy.

## 🌟 Features
- **Interactive inputs**: Adjust passenger details via sidebar sliders
- **Instant predictions**: Real-time survival probability calculation
- **Visual feedback**: Celebration animation for survival predictions
- **Responsive design**: Works on desktop and mobile devices

## ⚙️ How It Works
1. **Data Processing**:
   - Cleans the original Titanic dataset (handles missing values, converts categories)
   - Creates new features like family size
2. **Machine Learning**:
   - Uses a Random Forest classifier
   - Trained on passenger class, age, gender, fare, etc.
3. **Web Interface**:
   - Built with Streamlit for easy interaction
   - Hosted on Streamlit Community Cloud

## 🛠️ Technical Stack
- **Backend**: Python 3.9+
- **ML Framework**: scikit-learn
- **Web Framework**: Streamlit
- **Deployment**: Streamlit Community Cloud

## 🚀 Quick Start
```bash
# 1. Clone repository
git clone https://github.com/LuckyGurjar0001/cynbit-AI-ML-training-tasks
cd project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train model (first time only)
python model.py

# 4. Run app locally
streamlit run predict.py