from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import joblib

# --- Configuration ---
DATASET_CSV = "../../Task_2/research_dataset_final.csv"
MODEL_DIR = "../models"
REPORT_DIR = "../reports"

def main():
    if not os.path.exists(DATASET_CSV):
        print(f"Error: Dataset not found at {DATASET_CSV}")
        return

    print("Loading real-world dataset...")
    df = pd.read_csv(DATASET_CSV)
    
    X = df.drop(columns=['label'])
    y = df['label']
    
    # Train-Test Split (80/20 Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training on {len(X_train)} traces...")
    print(f"Testing on {len(X_test)} traces (Closed-World, 20 Classes)...")
    
    # Gaussian Naive Bayes model
    model = GaussianNB()
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Metrics
    acc = accuracy_score(y_test, y_pred)
    print(f"\nREAL-WORLD ATTACK ACCURACY: {acc:.4f}")
    
    report = classification_report(y_test, y_pred)
    print("\nClassification Report:")
    print(report)
    
    # Save Report
    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(os.path.join(REPORT_DIR, "real_world_results.txt"), "w") as f:
        f.write(f"Real-World Fingerprinting Evaluation\n")
        f.write(f"====================================\n")
        f.write(f"Accuracy: {acc:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(report)
    
    # Confusion Matrix Visualization
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(15, 12))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    fig, ax = plt.subplots(figsize=(15, 12))
    disp.plot(ax=ax, cmap='Blues', xticks_rotation='vertical', colorbar=True)
    plt.title(f"Real-World Confusion Matrix (Accuracy: {acc:.4f})")
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, "real_world_cm.png"))
    
    # Save Model
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "real_world_nb.pkl"))
    print(f"\nFinal evaluation complete. Model and reports saved in Task_3.")

if __name__ == "__main__":
    main()
