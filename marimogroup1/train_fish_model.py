"""
train_fish_model.py
==================
Trainiert ein Logistic Regression Modell zur Vorhersage von Fischarten
und exportiert die Gewichte als JSON für die HTML-WASM Nutzung.
"""

import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ============================================================================
# 1. DATEN LADEN
# ============================================================================
print("📁 Loading data...")
df = pd.read_csv("../datasets/Fish.csv")
print(f"✓ Loaded {len(df)} samples")
print(f"  Species: {df['Species'].unique()}")

# ============================================================================
# 2. DATEN VORBEREITEN
# ============================================================================
print("\n🔧 Preparing features...")
df_clean = df.drop(["Length1", "Length3"], axis=1)

y = df_clean["Species"]
X = df_clean[["Length2", "Height", "Width", "Weight"]]

print(f"✓ Features: {list(X.columns)}")
print(f"✓ Classes: {sorted(y.unique())}")

# ============================================================================
# 3. MODELL TRAINIEREN
# ============================================================================
print("\n🚀 Training model...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_scaled, y)

# ============================================================================
# 4. MODELL EVALUIEREN
# ============================================================================
print("\n📊 Evaluation:")
y_pred = model.predict(X_scaled)
accuracy = accuracy_score(y, y_pred)
print(f"✓ Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y, y_pred))

# ============================================================================
# 5. GEWICHTE EXTRAHIEREN
# ============================================================================
print("\n💾 Extracting model weights...")
weights_dict = {
    "coef": model.coef_.tolist(),
    "intercept": model.intercept_.tolist(),
    "classes": model.classes_.tolist(),
    "scaler_mean": scaler.mean_.tolist(),
    "scaler_scale": scaler.scale_.tolist()
}

print(f"✓ Coef shape: {np.array(weights_dict['coef']).shape}")
print(f"✓ Intercept: {len(weights_dict['intercept'])} values")
print(f"✓ Scaler mean: {len(weights_dict['scaler_mean'])} values")
print(f"✓ Classes: {weights_dict['classes']}")

# ============================================================================
# 6. AUSGABE
# ============================================================================
print("\n📤 Model weights as Python dict:")
print("=" * 70)
print("model_weights = " + json.dumps(weights_dict, indent=4))
print("=" * 70)

# Optional: Speichern als JSON-Datei
with open("model_weights.json", "w") as f:
    json.dump(weights_dict, f, indent=4)
print(f"\n✓ Weights saved to: model_weights.json")
print(f"  Size: {len(json.dumps(weights_dict)) / 1024:.2f} KB")
