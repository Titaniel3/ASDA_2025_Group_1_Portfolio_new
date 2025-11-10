## Airbnb Report Group 1

**Project Report Suggested Structure**

**Scenario**

You are a team of data analysts working for the **European Commission for Sustainable Cities**. Your task is to explore Airbnb data from ten European cities and write a **clear, data-driven report** about the current state of the Airbnb market and its possible connections to **gentrification**.

This is an **exploratory analysis**, not a full scientific study. You are not expected to run statistical tests or build models. Instead, focus on describing what the data shows — for example, how Airbnb listings, prices, and guest satisfaction differ across cities, and whether some of these patterns might suggest housing pressure or early signs of gentrification.

Support your discussion with **figures or plots** that help illustrate your points. Each figure should be:

* properly labeled and titled,  
* briefly described in a caption, and  
* clearly mentioned in the text where it’s relevant.

Your report should be **concise, factual, and readable** — avoid long theoretical discussions or unnecessary text. The goal is to communicate insights that a city planner or policymaker could easily understand.

**Important:** Do **not** include code in the report. All code and data analysis belong in your Jupyter notebook.

0\. **Authors of the report**

| Name | Contribution |
| :---- | :---- |
| Shreyas Krishnamurthy | 1\. **Dataset Overview**  2\. **Dataset Structure**  4\. **Descriptive statistics**    |
|  |   |
|  |   |
|  |   |
|  |   |

1\. **Dataset Overview** 

| Item | Description |
| :---- | :---- |
| Dataset name | Airbnb European Cities Dataset |
| Number of rows | 1104  |
| Number of columns | 19 (excluding an unlabelled row index column), 20 (including an unlabelled row index column)  |
| Format file (.csv, .txt, etc) | CSV (.csv)  |
| Authors of the dataset | Original Data Scraped by AirDNA (A commercial data provider)  |
| Source (name) | AirDNA  |
| Source (link) | https://docs.google.com/spreadsheets/d/1ecopK6oyyb4d_7-QLrCr8YlgFrCetHU7-VQfnYej7JY/edit?usp=sharing  |

   
   
2\. **Dataset Structure** 

| Feature/variable | Data type | Description | Number of Unique values | Example values |
| :---- | :---- | :---- | :---- | :---- |
| Price   | float64  | The final price for the booking (typically a two-night stay for two guests) in Euros (€).  | 10497  | 194.0336981  |
| room_type      | object (String)  | The type of space offered: 'Entire home/apt', 'Private room', or 'Shared room'.  | 3  | Private room  |
| room_shared    | bool  | Indicates if the room is a shared space (e.g., dormitory bed).  | 2  | False  |
| room_private   | bool  | Indicates if the room is a private room within a shared unit.  | 2  | True  |
| person_capacity   | float64  | The maximum number of guests the listing can accommodate.  | 5  | 2  |
| host_is_superhost  | bool  | True if the host has Superhost status, False otherwise.  | 2  | False  |
| multi     | int64  | Binary indicator (1/0) for hosts managing multiple listings (often >5 in the original study).  | 5 | 1  |
| biz    | int64  | Binary indicator (1/0) for listings marked as suitable for business travel.  | 2  | 0  |
| cleanliness_rating   | int64  | The listing's cleanliness rating score, typically on a 5-10 scale.  | 9  | 10  |
| guest_satisfaction_overall  | int64  | The overall guest satisfaction rating, typically on a 0-100 scale.  | 51707  | 53  |
| bedrooms   | float64  | The number of bedrooms in the listing (e.g, 0 for studio apartments).  | 51707  | 10  |
| dist  | float64  | The distance from the listing to the city center (units depend on the source, often kilometers).  | 51707  | 5.022963798  |
| metro_dist  | float64  | The distance from the listing to the nearest metro/subway station.  | 51707  | 2.539380003  |
| attr_index   | float64  | Attraction Index: A raw score reflecting the attractiveness (cultural, historical sites) of the area.  | 51707   | 78.69037927  |
| attr_index_norm  | float64  | The Normalized Attraction Index, scaled to a 0-100 range.  | 51688  | 4.166707868  |
| rest_index     | float64  | Restaurant Index: A raw score reflecting the availability of dining options in the vicinity.  | 51707  | 98.25389587  |
| rest_index_norm     | float64  | The Normalized Restaurant Index, scaled to a 0-100 range.  | 51688  | 6.846472824  |
| lng    | float64  | Geographical coordinates (Longitude).  | 23600  | 4.90569  |
| lat  | float64  | Geographical coordinates (Latitude).  | 21484  | 52.41772  |
| city     | object (String)  | The European city where the listing is located.  | 10  | london  |
| day_type    | object (String)  | Categorization of the booking period: 'weekdays' or 'weekends'.  | 2  | weekend  |
| country  | object (String)  | The country where the city is located (newly engineered column).  | 10  | France  |
 

3\. **Data cleaning** 

| Issue | Names of Columns affected | Description of the Issue | Action Taken |
| :---- | :---- | :---- | :---- |
| Inconsistent column labeling |   |   |   |
| Wrong data types |   |   |   |
| Missing values |   |   |   |
| Duplicates |   |   |   |
| Inconsistent categories |   |   |   |
| Other |  |  |  |

4\. **Descriptive statistics**   
Numeric columns

|   | Price | person_capacity | cleanliness_rating | guest_satisfaction_overall  | bedrooms | dist | metro_dist | attr_index | attr_index_norm  | rest_index | rest_index_norm | lng | lat | log_Price |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Count | 51707.00  |  51707.00     | 51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |  51707.00  |
| Mean | 279.87   | 3.16  | 9.39  | 92.62 | 1.15  | 3.19 | 0.68   | 294.20  | 13.42  | 626.85  | 22.78   | 7.42   | 45.67    | 5.42   |
| Standard deviation | 327.94    | 1.29   | 0.95  |8.94    | 0.62    | 2.39   | 0.85    | 224.75    | 9.80  |  497.92   | 17.80   |  9.79  |   5.24  |    0.59   |
| Min | 34.77     |  2.00  | 2.00  | 20.00  |    0.00   |   0.01  |    0.005 |  15.15   |     0.92   |  19.57    |     0.59    |  -9.22   |  37.95  |   3.57    |
| 25% | 148.75  |  2.00  | 9.00     | 90.00   |   1.00   |   1.45  |    0.24  |   136.79    |     6.38   | 250.85   |     8.75  |  -0.07  |   41.39   |  5.00    | 
| 50% | 211.34  |  3.00  | 10.00     |     95.00    |  1.00   |   2.61 |    0.41   |  234.33     |   11.46  |  522.05  |     17.54   |   4.87   | 47.50   |   5.35  |
| 75% | 319.69  |  4.00  | 10.00     |  99.00    |  1.00  |    4.26  |    0.73    |   385.75  |      17.41  |  832.62   |     32.96 |   13.518   |  51.47   |   5.77   |
| Max | 18545.45  | 6.00  | 10.00     | 100.00   |  10.00  |   25.284557  |   14.27  | 4513.56   |  100.00 |  6696.15  |     100.00  | 23.78 |   52.64|    9.82   |

Category columns

|   | Column 1 | Column 2 | Column 3 |
| :---- | :---- | :---- | :---- |
| Count |   |   |   |
| Number of unique values |   |   |   |
| Most frequent value |   |   |   |
| Most frequent value (frequency) |   |   |   |
| Least frequent value |   |   |   |
| Least frequent value (frequency) |   |   |   |

 

**5\. Analysis \- Research question**

