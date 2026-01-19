#  Wine Color Classification Analysis Project Report 

## 0. Authors of the report

| Name | Contribution |
|------|--------------|
| Shreyas Krishnamurthy     |  |
| Daniel Lichtmannecker     |   |
|  Tobias Demming    |    |
| Ranjit Singh     | |

## 1. Dataset Overview

| Item                | Description                                                                                                                                                                   |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Number of rows      | 4157                                                                                                                                                                        |
| Number of columns   |     13                                                                                                                                                                     |
| Format file (.csv, .txt, etc) | .csv                                                                                                                                                                        |
| Creator of the dataset | Same as the authors of the report                                                                                                                                             |
| Source (name)       | wine_development(in).csv                                                                                                                                                                |
| Source (link)       | [Final Dataset](../datasets/wine_development(in).csv) 
| Date/Time | 12.01.2026/ 11.20 am   


## 2. Dataset Structure & Descriptive Statistics

| Data type | Variable | Number of unique values | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
|----------|----------|-------------------------|-------|------|-----|-----|-----|-----|-----|-----|
| float64 | fixed acidity | 103 | 4157 | 7.208 | 1.298 | 3.9 | 6.4 | 7.0 | 7.7 | 15.9 |
| float64 | volatile acidity | 173 | 4157 | 0.339 | 0.166 | 0.08 | 0.23 | 0.29 | 0.40 | 1.58 |
| float64 | citric acid | 87 | 4157 | 0.319 | 0.144 | 0.00 | 0.25 | 0.31 | 0.39 | 1.66 |
| float64 | residual sugar | 288 | 4157 | 5.400 | 4.733 | 0.6 | 1.8 | 3.0 | 8.1 | 65.8 |
| float64 | chlorides | 183 | 4157 | 0.056 | 0.035 | 0.012 | 0.038 | 0.047 | 0.065 | 0.611 |
| float64 | free sulfur dioxide | 121 | 4157 | 30.416 | 17.992 | 1.0 | 17.0 | 29.0 | 41.0 | 289.0 |
| float64 | total sulfur dioxide | 264 | 4157 | 115.485 | 56.850 | 6.0 | 77.0 | 118.0 | 155.0 | 440.0 |
| float64 | density | 876 | 4157 | 0.9947 | 0.0030 | 0.9871 | 0.9923 | 0.9948 | 0.9969 | 1.0390 |
| float64 | pH | 100 | 4157 | 3.220 | 0.160 | 2.74 | 3.11 | 3.21 | 3.32 | 3.90 |
| float64 | sulphates | 100 | 4157 | 0.530 | 0.146 | 0.22 | 0.43 | 0.51 | 0.60 | 1.95 |
| float64 | alcohol | 100 | 4157 | 10.491 | 1.193 | 8.0 | 9.5 | 10.3 | 11.3 | 14.9 |
| int64 | quality | 7 | 4157 | 5.822 | 0.882 | 3 | 5 | 6 | 6 | 9 |
| object | color | 2 |  |  |  |  |  |  |  |  |

