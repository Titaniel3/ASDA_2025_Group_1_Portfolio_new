# World Bank Correlation Report

- We extend the research from last week by now looking in-depth in different variables and seeing if they are correlated with each other
- We cluster the dataset into four different areas: 
    - Governance and institutional quality (Shreyas)
    - Environmental sustainability (Tobias)
    - Economic performance and poverty reduction (Ranjit)
    - Human well-being and health (Daniel)

**Table of Contents**:
 1. Introduction and research question
 2. Results

    2.1 Governance and institutional quality

    2.2 Environmental sustainability

    2.3 Economic performance and poverty reduction

    2.4 Human well-being and health

3. Conclusion

**Table of figures**:

Figure 1: Correlation Heat Map for governance and institutional quality

Figure 2: Scatter Plot Map for governance and institutional quality

Figure 3: Correlation Heat Map for environmental sustainabilty

Figure 4: Scatter Plot for gdp per capita vs. electric power consumption per capita

Figure 5: Correlation Heat map for economic performance and poverty reduction

Figure 6: Scatter Plot for Human Capital vs. Poverty

Figure 7: Scatter Plot for Human Capital vs. Life Expectancy at birth

Figure 8: Scatter Plot for Tax revenue vs. Expenses by government

Figure 9: Mixed plot for correlations of human well-being and health

Figure 10: Histogram and Boxplot for birth rate and GDP per capita

Figure 11: Scatter Plot for GDP per capita vs. birth rate



## 1. Introduction and research question

xxxx (Daniel)

## 2. Results

In this chapter we will provide our results for the different categories.

### 2.1 Governance and institutional quality

Hypothesis: They are all highly correlated, xxx

![alt text](../additional_material\Plots\week05_image-10.png)<p>Figure 1: Correlation Heat Map for governance and institutional quality</p>

Results show that they all are highly correlated, all correlations are significant

![alt text](../additional_material\Plots\week05_image-12.png)<p>Figure 2: Scatter Plot Map for governance and institutional quality</p>

This image shows clear pattern that high income countries are on the upper right and low income on the low left side for all the variables

### 2.2 Environmental sustainability

Overview over relevant variables:

![alt text](image-1.png)<p>Figure 3: Correlation Heat Map for environmental sustainabilty</p>

Hypothesis: Higher GDP per capita is correlated with higher Electric Power Consumption

![alt text](image-2.png)<p>Figure 4: Scatter Plot for gdp per capita vs. electric power consumption per capita</p>

**Shorten this**: (DANIEL)

r = 0.69, p-value = 0.00

The scatter plot suggests a **general upward trend**: countries with higher electric
power consumption per capita tend to have higher GDP per capita. The correlation
coefficient quantifies this relationship. A positive and statistically significant
correlation indicates a strong direction: as electricity consumption increases, GDP
per capita tends to increase as well.

However, **correlation does NOT imply causation.** This analysis does not tell us whether
electricity consumption causes higher GDP, whether GDP growth increases energy use,
or whether both are influenced by other structural factors (e.g., industrialization,
infrastructure, climate, policy, or geography).

### 2.3 Economic performance and poverty reduction

Overview over the variables

![alt text](image-4.png)<p>Figure 5: Correlation Heat map for economic performance and poverty reduction</p>

**Correlation 1**: Human Capital vs. Poverty
Hypothesis: Higher human capital is correlated with low poverty rates

![alt text](image-7.png)<p>Figure 6: Scatter Plot for Human Capital vs. Poverty</p>

Inspiration: This is  Negative corraltion(Spearman r ≈ -0.64, p-value = 0.00)which tells as the human capital index increases, the poverty headcount decreases. It means  the Countries with higher education, skills, and health levels (high human capital) , tend to have much lower poverty rates.

**Correlation 2**: Human Capital vs. Life Expectancy at Birth

Hypothesis: Higher Human Capital correlates with higher Life Expecancy at Birth

![alt text](image-9.png)<p>Figure 7: Scatter Plot for Human Capital vs. Life Expectancy at birth</p>

Inspiration: The results show a very strong positive correlation (Spearman r ≈ 0.90, p-value = 0.00) between Human Capital Index and Life Expectancy. It means countries with higher HCI (health, education, skills) almost always have higher life expectancy.

**Correlation 3**: Tax revenue vs. expenses

Hypothesis: Higher tax revenues (%) correlate with higher expeneses (%) by government

![alt text](image-10.png)<p>Figure 8: Scatter Plot for Tax revenue vs. Expenses by government</p>

Inspiration: The results show a moderate positive correlation (Spearman r ≈ 0.68, p-value 0.00) between Tax Revenue and Government Expenses. It means more tax revenue leads to more government spending.This suggests that countries with higher tax revenue tend to also exhibit higher levels of government spending. The relationship is statistically significant (p < 0.001), and the 95% confidence interval [0.67, 0.70] shows that the correlation is both stable and precise due to the large sample size (n = 4014).

### 2.4 Human well-being and health

Overview: 

![alt text](image-12.png)<p>Figure 9: Mixed plot for correlations of human well-being and health</p>

**Correlation: Birth rate and GDP per Capita
![alt text](image-13.png)<p>Figure 10: Histogram and Boxplot for birth rate and GDP per capita</p>

Hypothesis: Higher GDP per Capita correlates with a lower birth rate
![alt text](image-14.png)<p>Figure 11: Scatter Plot for GDP per capita vs. birth rate</p>

r = -0.819, p-value: 0.00







