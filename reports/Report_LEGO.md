# 🧱 Lego Inventory Dataset Cleaning — Project Report

## 1. Dataset Overview (Clean Version)

Information is for the clean version of the dataset, so the final dataset we received after cleaning it.

| Item | Description |
|------|--------------|
| **Dataset Name** | Lego Inventory Dataset  |
| **Authors** | Tobias Demming, Ranjit Singh, Daniel Lichtmannecker, Saddam Kham, Shreyas Krishnamurthy |
| **Number of Entries** |  185 |
| **Number of Features/Variables** | 10 ("Transparent" was deleted, as only one group used it) |
| **Format File** | .csv |
| **Date/time**| 30-10-2025 / 10.30 am (Date of downloading the original data)|

**Description:** This dataset contains an inventory description of various Lego pieces, detailing their physical and geometric properties.

---
## 2. Dataset Structure (Clean Version)

| Feature/Variable | Data Type | Description |  Unique Values | Example Values |
|------------------|-----------|--------------|-----------------|----------------|
| id          |      Integer | Unique identifier for the Lego piece.|  185 |[1, ..., 185]       |1,2,3
| color         | String|Color names of the pieces.|63 | Blue, Light Blue, Transparent Sky Blue
| is duplo? | Boolean| This indicates whether the piece belongs to the larger Duplo system or not.|2| True, False
| size type | String |The physical type of the piece.|2 | Plate, Brick
| base shape| String|The geometric shape of the base of the piece. | 5|Circle, Triangle, Trapezium, Square, Rectangle
| base dimensions| String|The physical length and width of the piece in units.|12 | 2x2, 2x4, 1x1
| number of studs| Integer|The total count of studs on the piece's surface.|10  | 24, 6, 8
| has slope?| Boolean| This indicates if the piece features an angled or sloped surface.| 2| True, False
|slope degree| Integer|The specific degree of the slope.| 4 | 0, 15, 30, 45
|in stock|Integer|This indicates the number of available pieces in stock | 3 |1, 2, 3
---

## 3. Descriptive Statistics (Clean Version)

### Numeric Columns

| Statistic | Number of Studs | Slope Degree | In Stock |
|------------|-----------|-----------|-----------|
| **Count** |  185|185  | 185 |
| **Mean** | 4.75 |  5.59| 1.10 |
| **Standard Deviation** |5.11  | 14.72 |0.36  |
| **Min** | 0 | 0 | 1 |
| **25%** | 2 | 0 | 1 |
| **50% (Median)** | 4 |0  | 1 |
| **75%** |6  | 0 | 1 |
| **Max** |  24|45  | 3 |

---

### Categorical / Object Columns

| Statistic | Color | Size Type | Base Shape | Base Dimension
|------------|-----------|-----------|-----------|-----------|
| **Most Frequent Value** | Grey | Plate | Rectangle |2x2|
| **Most Frequent Value (Frequency)** |12  | 103 | 97 |41|
| **Least Frequent Value** |  Many, f.e. "Transparent Orange"| Brick | Triangle |4x4|
| **Least Frequent Value (Frequency)** | 1 | 82 | 2 |3|

---

## 4. Exploratory Plots (Optional)

Here are some basic plots of our dataset
<img width="845" height="365" alt="Screenshot 2025-11-03 153141" src="https://github.com/user-attachments/assets/1d33806e-d6a8-4544-823f-84dc1e49120f" />
<img width="820" height="355" alt="Screenshot 2025-11-03 153254" src="https://github.com/user-attachments/assets/3588bbab-07df-4965-9258-7bbbeed98447" />
<img width="826" height="364" alt="Screenshot 2025-11-03 153505" src="https://github.com/user-attachments/assets/f1dbf7e5-1f76-4372-934a-74eb14065f9f" />
<img width="840" height="358" alt="Screenshot 2025-11-03 153528" src="https://github.com/user-attachments/assets/fd4627d2-b297-4a9f-bab9-0a55431e28c7" />
<img width="855" height="359" alt="Screenshot 2025-11-03 153611" src="https://github.com/user-attachments/assets/42dfee9a-6b5b-472f-be2d-d349f385ddf9" />
<img width="851" height="731" alt="Screenshot 2025-11-03 153646" src="https://github.com/user-attachments/assets/6c9cdead-4f6e-429c-b4bc-9ff74f4e80ee" />
<img width="966" height="732" alt="Screenshot 2025-11-03 153801" src="https://github.com/user-attachments/assets/a6d4f6a7-7ce8-4ffe-b47e-93f0c9f0fe5c" />








---

## 5. Data Cleaning Procedure

### 5.1 Major Data Inconsistencies

| Issue | Columns Affected | Description of the Issue | Action Taken |
|--------|------------------|---------------------------|---------------|
| Inconsistent column labeling |  |  |  |
| Wrong data types |  |  |  |
| Missing values |  |  |  |
| Duplicates |  |  |  |
| Inconsistent categories |  |  |  |

---

### 5.2 Minor Data Inconsistencies

List any small or secondary issues that couldn’t be included above but were addressed or noted.

---

## 6. Recommendations for Good Practices

Summarize best practices for future data collection and entry to prevent inconsistencies or data loss.

---

## 7. AI Disclaimer

If any part of the work (e.g., code, visualization, cleaning logic) was assisted or generated with AI tools, describe **which parts** and **how** they were used.

---

## Suggested Notebook Structure (for y
