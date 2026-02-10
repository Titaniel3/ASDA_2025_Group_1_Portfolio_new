# 🧱 Lego Inventory Dataset Cleaning — Project Report
## 0. Authors of the report

| Name | Contribution |
| :---- | :---- |
| Shreyas Krishnamurthy | Data collection,Graph plotting   |
|Daniel Lichtmannecker  | Data collection, Data cleaning, reporting, Graph plotting    |
| Tobias Demming |  Reporting , analysis,Graph plotting     |
| Ranjit Singh |  Data collection, Analysis, graph plotting  |
| Saddam Khan| Data collection|


## 1. Dataset Overview (Clean Version)

Information is for the clean version of the dataset, so the final dataset we received after cleaning it. 

The cleaned LEGO dataset used for this analysis can be found [here](../additional_material/Lego_cleaned_dataset.csv).


| Item | Description |
|------|--------------|
| **Dataset Name** | Lego Inventory Dataset  |
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
![top20_colors](https://github.com/user-attachments/assets/ebc660a8-7998-4e16-85ec-268620c2ca0e)
![categorical_distributions_2x2](https://github.com/user-attachments/assets/bf89e4b7-b0ff-4f45-a917-960a80208e0c)


<img width="851" height="731" alt="Screenshot 2025-11-03 153646" src="https://github.com/user-attachments/assets/6c9cdead-4f6e-429c-b4bc-9ff74f4e80ee" />
<img width="966" height="732" alt="Screenshot 2025-11-03 153801" src="https://github.com/user-attachments/assets/a6d4f6a7-7ce8-4ffe-b47e-93f0c9f0fe5c" />









---

## 5. Data Cleaning Procedure

### 5.1 Major Data Inconsistencies


First, there was the column "Transparent", which only group 4 used. As the goal was to find duplicate Lego pieces, we deleted this column, as there was no data regarding this for the other groups which made finding duplicates more difficult.

For most of the categories, all groups used different formats. For example, Base Dimension was sometimes "2x2", "2 x 2" or "2*2". As this all means the same, the major challenge was to merge them all into the same format (here: "2x2"). This problem affected most of the columns: "is duplo?", "size type", "base shape", "base dimensions", "has slope?" and "in stock" (one group used "yes" for this variable instead of "1").

Especially challenging was the color variable, because some groups wrote them with capital letters ("Blue"), some did not ("blue"). There were also differences with more complex colors ("lightblue" vs. "light blue"). All of these different formats were merged into the same format (f.e."Light Blue"), with capital letters starting each word and a space between each word. This was done by using code which defined modifiers (f.e. "light" or "dark") and bases (f.e. "blue" or "red") for each possible color, then splitted them (if necessary) and capitalized the first letter of each word.

---

### 5.2 Minor Data Inconsistencies

When reviewing the final data set in Excel, we realised that slope degree was wrong (f.e. 450 instead of 45). So we had to fix the code to fix this issue. 

## 6. Recommendations for Good Practices

Before starting the data collection process, each group should have agreed on one data format for each variable, because this way the data cleaning process would have been way easier. Especially for the colors, this would have been extremely helpful, as there are probably more duplicates in the dataset which cannot be found due to different color namings.

For visualization we found that box plots should be viewed independently for each category as using the same scale for each category might be misleading. 

---

## 7. AI Disclaimer

We used AI for visualization. We first did it ourselves but the visuals did not look so great so we optimized the color schema and the general look of the plots using ChatGPT by prompting what we wanted our plots to look like and providing our code and asking ChatGPT to optimize it.

For the Data cleaning process, we asked ChatGPT to help us with the code for cleaning the colors, as this was quite difficult and even after excessive research we could not figure it out ourselves. So we wrote a prompt with the excact description of the problem and the solution we wanted to implement (with modifiers, bases and the capitalization of the first letters) and received ready-to-use code.

---

