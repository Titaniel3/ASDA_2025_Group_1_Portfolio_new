# HTML-WASM Optimierung: Fischarten-Klassifizierer

## Zusammenfassung

Dieses Dokument erläutert, wie das ursprüngliche Marimo-Notebook `fish_analysis_ranjit.py` für den Export als HTML-WASM optimiert wurde und welche Änderungen dafür notwendig waren.

---

## Probleme des Original-Notebooks

Das ursprüngliche Notebook war **nicht WASM-kompatibel**, da es folgende Abhängigkeiten nutzte:

### 1. **scikit-learn (sklearn)** ❌
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
```

**Problem:** sklearn kann nicht im Browser/WASM ausgeführt werden, weil:
- Es C/C++-Extensions nutzt (nicht in WASM kompilierbar)
- Model-Training im Browser ist technisch unmöglich
- Serialisierte Modelle können nicht geladen werden

### 2. **Relative Dateipfade** ❌
```python
df = pd.read_csv("../datasets/Fish.csv")
```

**Problem:** Im HTML-WASM Export existieren relative Dateipfade nicht

### 3. **Lokale Bildpfade** ❌
```python
fish_images = {
    "Bream": "images/Bream.jpg",
    ...
}
```

**Problem:** Lokale Dateipfade funktionieren nicht im Export

---

## Lösungsansatz: Pre-trained Weights

Statt das Modell im Browser zu trainieren, werden die Gewichte **einmalig lokal trainiert** und dann direkt im Notebook eingebettet.

### Workflow:

```
┌─────────────────────────────────────┐
│ 1. train_fish_model.py              │
│    • Lädt Fish.csv                  │
│    • Trainiert LogisticRegression   │
│    • Extrahiert Gewichte als JSON   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Gewichte kopieren in:            │
│    fish_analysis_wasm.py            │
│    • @app.cell mit model_weights    │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Export als HTML-WASM             │
│    marimo export html ... --wasm    │
│    ✓ Funktioniert 100% im Browser   │
└─────────────────────────────────────┘
```

---

## Implementierte Änderungen

### A. Modellgewichte eingebettet (statt Training)

**Vorher:**
```python
from sklearn.linear_model import LogisticRegression
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)
```

**Nachher:**
```python
model_weights = {
    "coef": [[...], [...], ...],        # 7×4 Matrix
    "intercept": [...],                 # 7 Werte
    "classes": [...],                   # Klassennamen
    "scaler_mean": [...],               # 4 Werte
    "scaler_scale": [...]               # 4 Werte
}
```

**Größe:** ~1 KB JSON (problemlos einbettbar)

### B. Manuelle Vorhersage-Funktion (ohne sklearn)

**Vorher:**
```python
prediction = model.predict(input_data)[0]
probs = model.predict_proba(input_data)[0]
```

**Nachher:**
```python
def predict_fish_species(length2, height, width, weight, model_weights):
    # 1. Normalisierung
    features = np.array([[length2, height, width, weight]])
    scaler_mean = np.array(model_weights["scaler_mean"])
    scaler_scale = np.array(model_weights["scaler_scale"])
    features_normalized = (features - scaler_mean) / scaler_scale
    
    # 2. Logistische Regression: z = X @ coef.T + intercept
    coef = np.array(model_weights["coef"])
    intercept = np.array(model_weights["intercept"])
    logits = features_normalized @ coef.T + intercept
    
    # 3. Softmax
    exp_logits = np.exp(logits - np.max(logits))
    probs = exp_logits / np.sum(exp_logits)
    
    # 4. Best class
    pred_idx = np.argmax(probs)
    prediction = model_weights["classes"][pred_idx]
    confidence = probs[0][pred_idx] * 100
    
    return prediction, confidence
```

**Vorteile:**
- Reine NumPy-Implementierung
- Keine sklearn-Abhängigkeit
- Funktioniert identisch im Browser

### C. Online-Bilder statt lokale Pfade

**Vorher:**
```python
fish_images = {
    "Bream": "images/Bream.jpg",  # ❌ Lokal
    ...
}
```

**Nachher:**
```python
fish_images = {
    "Bream": "https://upload.wikimedia.org/...",  # ✅ Online
    ...
}
```

### D. Bessere UI mit Validierung

**Neu hinzugefügt:**
- Eingebaute Grenzen-Validierung (Limit-Check)
- Farbcodierte Konfidenz-Scores
- Aussagekräftige Error-Meldungen
- Deutsche Labels und Anweisungen

---

## Modell-Performance

Trainiert auf 159 Fish-Samples:

| Klasse     | Precision | Recall | F1-Score | Support |
|-----------|-----------|--------|----------|---------|
| Bream     | 0.95      | 1.00   | 0.97     | 35      |
| Parkki    | 1.00      | 0.82   | 0.90     | 11      |
| Perch     | 0.68      | 0.96   | 0.80     | 56      |
| Pike      | 1.00      | 1.00   | 1.00     | 17      |
| Roach     | 1.00      | 0.05   | 0.10     | 20      |
| Smelt     | 0.88      | 1.00   | 0.93     | 14      |
| Whitefish | 0.00      | 0.00   | 0.00     | 6       |

**Gesamtgenauigkeit: 81.76%**

---

## Dateien

### 1. `train_fish_model.py`
- **Zweck:** Trainiert das Modell lokal
- **Output:** Modellgewichte als JSON
- **Wann laufen:** Einmalig beim Setup
- **Abhängigkeiten:** pandas, scikit-learn, numpy

```bash
python train_fish_model.py
```

### 2. `fish_analysis_wasm.py`
- **Zweck:** Marimo-Notebook mit eingebetteten Gewichten
- **Output:** HTML-WASM Datei
- **Laufzeit:** 100% im Browser
- **Abhängigkeiten:** Nur numpy, marimo, pandas

```bash
marimo export html fish_analysis_wasm.py --mode wasm
```

### 3. `WASM_OPTIMIERUNG.md` (diese Datei)
- Dokumentation der Änderungen
- Technische Erklärungen

---

## Verwendung im Browser

Nach dem Export als HTML-WASM:

1. **Download:** `fish_analysis_wasm.html`
2. **Öffnen:** Im Browser (Chrome, Firefox, Safari)
3. **Funktioniert:** Vollständig offline, keine Server nötig
4. **Deploy:** Auf GitHub Pages oder beliebigem Web-Server

---

## Technische Details: WASM-Kompatibilität

| Komponente | Original | WASM-Version | Status |
|-----------|----------|--------------|--------|
| **pandas** | ✓ | ✓ (limit) | Nur df.read_csv ✅ |
| **numpy** | ✓ | ✓ | Vollständig ✅ |
| **scikit-learn** | ✓ | ✗ | Manuell ersetzt ✅ |
| **marimo** | ✓ | ✓ | Vollständig ✅ |
| **plotly** | ✓ | ✓ | Optional |
| **Dateiakzess** | ✓ | ✗ | Eingebettet ✅ |
| **Training** | ✓ | ✗ | Pre-trained ✅ |

---

## Vorteile dieser Lösung

✅ **Funktioniert im Browser:** 100% WASM-kompatibel  
✅ **Schnell:** Keine Netzwerk-Abhängigkeiten für Vorhersage  
✅ **Offline:** Funktioniert ohne Internetverbindung (nach Load)  
✅ **Leicht:** Datei-Größe unter 100 KB  
✅ **Wartbar:** Gewichte sind einfach austauschbar  
✅ **Reproduzierbar:** Exakte Vorhersagen bei gleichen Inputs  

---

## Zukünftige Erweiterungen

Falls das Modell verbessert werden soll:

1. **Bessere Features:** Mehr oder andere Messwerte nutzen
2. **Mehr Daten:** Trainingsdaten erweitern
3. **Modell-Typ:** Zu RandomForest oder Neural Network wechseln
   - Dann entsprechende Gewichte & Funktionen exportieren
4. **Live-Training:** TensorFlow.js nutzen (komplexer)

---

## Fazit

Das Notebook ist nun **vollständig HTML-WASM-kompatibel** und funktioniert als interaktives Tool direkt im Browser, ohne dass Server-seitige Verarbeitung nötig ist.
