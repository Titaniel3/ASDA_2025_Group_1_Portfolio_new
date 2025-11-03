# 🧱 Lego Inventory Dataset Cleaning — Project Report

## 1. Dataset Overview (Clean Version)

| Item | Description |
|------|--------------|
| **Dataset Name** | Lego Inventory Dataset  |
| **Authors** | Group 1 , Group 2, Group 3, Group 4, Group 5 |
| **Number of Entries** |  204 |
| **Number of Features/Variables** | 10 + 1 (One additional feature (Transparent) had added by Group 4) |
| **Format File** | .xlsx |
| **Date/time**| 30-10-2025 / 10.30 am |

**Description:** This dataset contains an inventory description of various Lego pieces, detailing their physical and geometric properties.

---
## 2. Dataset Structure (Clean Version)

| Feature/Variable | Data Type | Description |  Unique Values | Example Values |
|------------------|-----------|--------------|-----------------|----------------|
| id          |      Integer | Unique identifier for the Lego piece.|  1 to 204               |         |
| color         | String|Color names of the pieces.|63|
| is duplo? | Boolean| This indicates whether the piece belongs to the larger Duplo system or not.|2|
| size type | String |The physical type of the piece.|
| base shape| String|The geometric shape of the base of the piece.
| base dimensions| Integer|The physical length and width of the piece in units.|
| number of studs| Integer|The total count of studs on the piece's surface.|
| has slope?| Boolean| This indicates if the piece features an angled or sloped surface.|
|slope degree| Integer|The specific degree of the slope.|
|in stock| Boolean|This indicates the availability of the piece|
---

## 3. Descriptive Statistics (Clean Version)

### Numeric Columns

| Statistic | number of studs | slope degree | in stock |
|------------|-----------|-----------|-----------|
| **Count** | 204 |204  | 204 |
| **Mean** | 4.90 | 5.07 |1.0  |
| **Standard Deviation** |4.99  | 14.11 | 0 |
| **Min** |0  |  0|1.0  |
| **25%** | 2.00 | 0 |1.0  |
| **50% (Median)** | 4.00 |0  | 1.0 |
| **75%** |6.00  | 0 | 1.0 |
| **Max** | 24.00 | 45 | 1.0 |

---

### Categorical / Object Columns

| Statistic | Color | Size type | Base shape  | Base dimensions |
|------------|-----------|-----------|-----------|--------------|
| **Count** | 204 |204  |204  |204|
| **Number of Unique Values** | 63 |2  |5  |21|
| **Most Frequent Value** | Yellow |Plate  |Rectangle  |2x2|
| **Most Frequent Value (Frequency)** | 16 |108  |109  |47|
| **Least Frequent Value** | Transparent sky blue |Brick  |Triangle  |3x1|
| **Least Frequent Value (Frequency)** |1  |96  |2  |1|

---

## 4. Exploratory Plots (Optional)

Include any relevant basic plots (e.g., histograms, boxplots, barplots) that help understand the dataset.

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


