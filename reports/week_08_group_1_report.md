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

1. Encoding categorical variables: Holiday was transformed to be binary and weather_main was hot encoded.

2. Temperature was converted from farenheit to celcius

3. Tiime date was encoded from linear to a cyclic representation

4. Outliers for rain and temperature were removed, as they did not make any sense (f.e. -273.15 degree celcius)

### 4. Descriptive Statistics

| Variable        | Count    | Mean    | Std     | Min     | 25%     | 50%     | 75%     | Max      | Variance     | Dispersion Index |
|----------------|----------|---------|---------|---------|---------|---------|---------|----------|--------------|------------------|
| **traffic_volume** | 45634.0 | 3263.11 | 1986.52 | 0.00    | 1194.00 | 3389.00 | 4931.75 | 7280.00  | 3946253.31   | 1209.35          |
| rain_1h        | 45634.0 | 0.14    | 1.03    | 0.00    | 0.00    | 0.00    | 0.00    | 55.63    | 1.06         | 7.72             |
| snow_1h        | 45634.0 | 0.00    | 0.01    | 0.00    | 0.00    | 0.00    | 0.00    | 0.51     | 0.00         | 0.30             |
| clouds_all     | 45634.0 | 48.48   | 39.06   | 0.00    | 10.00   | 64.00   | 90.00   | 100.00   | 1525.84      | 31.47            |
| holiday_binary | 45634.0 | 0.00    | 0.04    | 0.00    | 0.00    | 0.00    | 0.00    | 1.00     | 0.00         | 1.00             |
| temp_c         | 45634.0 | 8.47    | 12.84   | -29.76  | -0.73   | 10.38   | 19.03   | 36.92    | 164.76       | 19.46            |
| day_of_week    | 45634.0 | 2.98    | 2.00    | 0.00    | 1.00    | 3.00    | 5.00    | 6.00     | 4.02         | 1.35             |
| hour_sin       | 45634.0 | 0.00    | 0.71    | -1.00   | -0.71   | 0.00    | 0.71    | 1.00     | 0.50         | 35.79            |
| hour_cos       | 45634.0 | 0.01    | 0.71    | -1.00   | -0.71   | 0.00    | 0.71    | 1.00     | 0.50         | 62.57            |
| day_sin        | 45634.0 | 0.00    | 0.71    | -0.97   | -0.78   | 0.00    | 0.78    | 0.97     | 0.50         | 169.36           |
| day_cos        | 45634.0 | 0.01    | 0.71    | -0.90   | -0.22   | 0.62    | 1.00    | 1.00     | 0.50         | 92.68            |
| month_sin      | 45634.0 | 0.02    | 0.71    | -1.00   | -0.50   | 0.00    | 0.87    | 1.00     | 0.50         | 23.50            |
| month_cos      | 45634.0 | -0.08   | 0.70    | -1.00   | -0.87   | 0.50    | 1.00    | 1.00     | 0.49         | -6.04            |
