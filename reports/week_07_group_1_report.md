# Fish Dataset Regression Analysis Project Report 

## 0. Authors of the report

| Name | Contribution |
|------|--------------|
| Shreyas Krishnamurthy     |    Analysis + Report       |
| Daniel Lichtmannecker     |    Analysis + Report       |
|  Tobias Demming    |          Analysis + Report      |
| Ranjit Singh     |         Analysis + Report       |


---

## 1. Dataset Overview

| Item | Description |
|------|-------------|
| Dataset name | Fish Market |
| Number of rows | 159 |
| Number of columns | 7 |
| Format file (.csv, .txt, etc.) |.csv |
| Authors of the dataset | Vipul L Rathod |
| Source (name) | Fish Market  |
| Source (link) | https://www.kaggle.com/datasets/vipullrathod/fish-market/data |
| Date/ Time | 30.11.2025, 22:30|

## 2. Dataset Structure

| Feature/variable | Data type | Description | Number of Unique values | Example values |
| ---------------- | --------- | ----------- | ----------------------- | -------------- |
|                  |           |             |                         |                |
|                  |           |             |                         |                |
|                  |           |             |                         |                |

## 3. Descriptive statistics

|             | Count | Mean   | Std    | Min  | 25%    | 50%    | 75%    | Max     |
| ----------- | ----- | ------ | ------ | ---- | ------ | ------ | ------ | ------- |
| **Weight**  | 159   | 398.33 | 357.98 | 0.00 | 120.00 | 273.00 | 650.00 | 1650.00 |
| **Length1** | 159   | 26.25  | 10.00  | 7.50 | 19.05  | 25.20  | 32.70  | 59.00   |
| **Length2** | 159   | 28.42  | 10.72  | 8.40 | 21.00  | 27.30  | 35.50  | 63.40   |
| **Length3** | 159   | 31.23  | 11.61  | 8.80 | 23.15  | 29.40  | 39.65  | 68.00   |
| **Height**  | 159   | 8.97   | 4.83   | 1.73 | 5.94   | 7.79   | 12.37  | 18.96   |
| **Width**   | 159   | 4.42   | 1.69   | 1.05 | 3.39   | 4.25   | 5.58   | 8.14    |


|                                      | Species   |
| ------------------------------------ | --------- |
| **Count**                            | 159       |
| **Number of unique values**          | 7         |
| **Most frequent value**              | Perch     |
| **Most frequent value (frequency)**  | 56        |
| **Least frequent value**             | Whitefish |
| **Least frequent value (frequency)** | 6         |


## 4. Analysis

Our research focuses on finding out, whether you can predict fish weight based on the length of a fish. 

The hypothesis is: There is a linear relationship between fish length and fish weights.

1. To check, we first square transformed the weight (dependent variable) to get a rather normally distribution.

![alt text](image.png)

2. We then checked which length to use (as there are three different ones). For that we created a correlation heatmap. 

![alt text](image-1.png)

The lengths are exremely highly correlated. After computing the variance inflation factor we decised to use length 2 for our model.

3. We then split the data into test and training data. 127 rows (80%) were in in the training data and 32 rows (20%) in the test data. 
Our model had as independent variables: Length, Height, Width and all Species types (which we dummy coded)
Our model has as dependent variable: Weight of fish
-> The independent variables of our models should try to predict the dependent variable!

Our linear regression showed the following plot: 

![alt text](image-2.png)

4. Test values showed the following results: 
- RMSE: 54.62
- MAI: 34.88
- R-squared: 97.90
- MAPE: 11.98

5. We then looked at our residuals:

![alt text](image-3.png)

The histogram of residuals showes that they are approximately normally distributed: 

![alt text](image-4.png)
