# Metro Interstate Traffic Volume Dataset Generalized Linear Models Analysis Project Report 

## 0. Authors of the report

| Name | Contribution |
|------|--------------|
| Shreyas Krishnamurthy     |    Analysis of GLMs      |
| Daniel Lichtmannecker     |   Data Cleaning and Preparation of Variables, Report        |
|  Tobias Demming    |   Comparing the GLMs          |
| Ranjit Singh     |        Analysis of GLMs        |

### 1. Dataset Overview

| Item                | Description |
|---------------------|-------------|
| Dataset name        |         traffic_final_new    |
| Time Period         |   2013 - 2018          |
| Sampling Frequency  |             |
| Number of rows      |      45635       |
| Number of columns   |          28   |
| Format file (.csv, .txt, etc) |  .xlsx |
| Creator of the dataset |   Same as the authors of the report      |
| Source (name)       |             |
| Source (link)       |             |

### 2. Dataset Structure

| Feature / Variable         | Data type      | Description | Number of unique values | Example values                     |
|----------------------------|----------------|-------------|--------------------------|------------------------------------|
| rain_1h                    | float64        |             | 371                      | [0.0, 0.25, 0.57]                   |
| snow_1h                    | float64        |             | 12                       | [0.0, 0.51, 0.32]                   |
| clouds_all                 | int64          |             | 50                       | [58.0, 40.0, 75.0]                  |
| weather_description        | object         |             | 38                       | ['broken clouds', 'scattered clouds', 'heavy snow'] |
| date_time                  | datetime64[ns] |             | 38461                    | [Timestamp('2013-01-01 00:00:00'), Timestamp('2013-01-01 01:00:00'), Timestamp('2013-01-01 02:00:00')] |
| traffic_volume             | int64          |             | 6669                     | [1439.0, 1502.0, 933.0]             |
| year                       | int32          |             | 6                        | [2013.0, 2014.0, 2015.0]            |
| month                      | int32          |             | 12                       | [1.0, 2.0, 3.0]                     |
| holiday_binary             | int64          |             | 2                        | [1.0, 0.0]                          |
| weather_main_Clouds        | bool           |             | 2                        | [np.True_, np.False_]              |
| weather_main_Drizzle       | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Fog           | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Haze          | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Mist          | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Rain          | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Smoke         | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Snow          | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Squall        | bool           |             | 2                        | [np.False_, np.True_]              |
| weather_main_Thunderstorm  | bool           |             | 2                        | [np.False_, np.True_]              |
| temp_c                     | float64        |             | 5795                     | [-9.66, -9.37, -8.99]               |
| hour                       | int32          |             | 24                       | [0.0, 1.0, 2.0]                     |
| day_of_week                | int32          |             | 7                        | [1.0, 2.0, 3.0]                     |
| hour_sin                   | float64        |             | 21                       | [0.0, 0.26, 0.5]                    |
| hour_cos                   | float64        |             | 22                       | [1.0, 0.97, 0.87]                   |
| day_sin                    | float64        |             | 7                        | [0.78, 0.97, 0.43]                  |
| day_cos                    | float64        |             | 7                        | [0.62, -0.22, -0.9]                 |
| month_sin                  | float64        |             | 11                       | [0.5, 0.87, 1.0]                    |
| month_cos                  | float64        |             | 11                       | [0.87, 0.5, 0.0]                    |



### 3. Data Cleaning

| Issue                       | Names of Columns affected | Description of the Issue | Action Taken |
|----------------------------|----------------------------|---------------------------|--------------|
| Inconsistent column labeling |                            |                           |              |
| Wrong data types             |                            |                           |              |
| Time Gaps                    | date_time                  |                           |              |
| Duplicates                   |                            |                           |              |
| Inconsistent categories      |                            |                           |              |
| Other                        |                            |                           |              |

### 4. Descriptive Statistics

Numeric columns

| Statistic        | Target Variable | Predictor 1 | Predictor 2 | Predictor 3 | ... |
|------------------|-----------------|-------------|-------------|-------------|-----|
| Count            |                 |             |             |             |     |
| Mean             |                 |             |             |             |     |
| Standard deviation |              |             |             |             |     |
| Min              |                 |             |             |             |     |
| 25%              |                 |             |             |             |     |
| 50% (Median)     |                 |             |             |             |     |
| 75%              |                 |             |             |             |     |
| Max              |                 |             |             |             |     |
| Variance         |                 |             |             |             |     |
| Dispersion index (= Variance / Mean) | |         |             |             |     |
