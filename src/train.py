import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
from preprocess import clean_text

def main():
    df = pd.read_csv("data/tickets.csv")
    df['text'] = (df['Subject'].fillna('') + " " + df['Description'].fillna('')).apply(clean_text)
    
    X, y = df['text'], df['Category']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X_train_vec = vectorizer.fit_transform(X_train)
    
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    X_test_vec = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vec)
    
    print(f"🎯 Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"⚖️  Macro F1: {f1_score(y_test, y_pred, average='macro'):.4f}")
    print("\n📋 Detailed Report:\n", classification_report(y_test, y_pred))
    
    joblib.dump((vectorizer, model), "models/best_model.pkl")
    print("\n✅ Model saved to models/best_model.pkl")

if __name__ == "__main__":
    main()