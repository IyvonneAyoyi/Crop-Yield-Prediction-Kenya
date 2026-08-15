# Crop Yield Estimation System for Kenya
Overview

This project develops a machine learning system for estimating crop yield at county level for eight food crops in Kenya using historical agricultural production data and environmental variables derived from geospatial and satellite data.

The project combines agricultural production records with environmental indicators such as rainfall, vegetation and other remotely sensed variables to estimate crop yield in tonnes per hectare. Four regression models — Linear Regression, Random Forest, Gradient Boosting and XGBoost — were trained and evaluated against a mean-yield baseline. Random Forest achieved the strongest overall performance, with an R² of 0.863, MAE of 0.859 t/ha, and RMSE of 1.623 t/ha.

Importantly, model performance varied substantially across the eight crops, demonstrating that the overall model score should not be interpreted as equal reliability for every crop.

# Problem Statement

Agricultural planning in Kenya requires reliable information about crop productivity. However, crop yields vary across locations and seasons due to differences in environmental and agricultural conditions.

This project investigates whether historical agricultural production data combined with environmental variables derived from geospatial and satellite data can be used to estimate crop yield at county level for selected food crops.

The system focuses on:

Beans
Cowpeas
Irish Potatoes
Maize
Pigeon Peas
Sorghum
Sweet Potatoes
Wheat

The intended users include agricultural planners, county agricultural officers, researchers and other stakeholders who require data-driven estimates of crop productivity.

# Dataset
Agricultural Production Data

The primary agricultural dataset used in this project is the National Agricultural Production Data 2024, containing county-level agricultural production information for 2019–2023.

| Property         | Details                                    |
| ---------------- | ------------------------------------------ |
| Name             | National Agricultural Production Data 2024 |
| Years            | 2019–2023                                  |
| Geographic level | County                                     |
| Target           | Crop yield (tonnes/hectare)                |
| Crops            | 8 food crops                               |
| Source           | `[INSERT OFFICIAL SOURCE URL]`             |
| Licence          | `[INSERT LICENCE / USAGE INFORMATION]`     |

The agricultural production data were used to establish the observed yield values against which the machine learning models were evaluated.

Geospatial and Environmental Data

The project also uses spatial and satellite-derived variables to represent environmental conditions associated with agricultural productivity.

These include environmental indicators derived using Google Earth Engine, together with crop spatial information from farm/crop maps.

The project uses crop maps for the eight selected crops to support the spatial analysis.

# Target Variable

The target variable is:

Crop Yield (tonnes/hectare)

Yield represents agricultural productivity relative to the cultivated area and is used as the continuous target for the regression models.

This makes the task a supervised regression problem rather than a classification problem.

# Methods
1. Exploratory Data Analysis

The dataset was explored to:

Examine crop and county distributions
Identify trends in crop production and yield
Examine relationships between environmental variables and yield
Identify missing or inconsistent observations
Understand differences between crops and counties

2. Data Preprocessing

The preprocessing pipeline included the preparation of agricultural and environmental variables for machine learning.

The exact preprocessing steps should be documented here according to your final notebook, including:

Missing-value handling
Feature selection
Categorical encoding
Numerical transformations/scaling, where applicable
Train/test splitting

Do not add scaling or imputation here unless your actual notebook performs those operations.

3. Machine Learning Models

Four regression algorithms were trained and compared:

Linear Regression

Used as a simple linear modelling approach and provides an interpretable reference for the relationship between the input variables and crop yield.

Random Forest

An ensemble tree-based regression model capable of capturing nonlinear relationships between environmental conditions and crop yield.

Gradient Boosting

An ensemble method that sequentially builds decision trees to improve prediction errors.

XGBoost

A gradient-boosted tree algorithm used as another nonlinear ensemble model for comparison.

The models were evaluated using the same evaluation framework to determine which approach performed best.

4. Baseline

A mean-yield baseline was used for comparison.

The baseline predicts the mean training yield for every observation rather than learning relationships between environmental variables and yield.

The mean training yield was:

3.7533 t/ha

The baseline provides a reference point for determining whether the machine learning models provide useful predictive information beyond simply using the average yield.

## Evaluation Metrics

Four regression metrics were used:

Mean Absolute Error (MAE)

Measures the average absolute difference between observed and estimated yield.

Lower values indicate better performance.

Root Mean Squared Error (RMSE)

Measures prediction error while giving greater weight to larger errors.

Lower values indicate better performance.

R² — Coefficient of Determination

Measures how much of the variation in observed yield is explained by the model.

Higher values indicate better performance.

An R² below zero indicates that the model performs worse than the mean-yield baseline for that evaluation group.

Mean Absolute Percentage Error (MAPE)

Measures prediction error as a percentage of the observed yield.

MAPE was reported as a complementary metric but is interpreted cautiously because percentage-based errors can become disproportionately large when observed yield values are small.

# Results
## Overall Model Performance

| Model               |     MAE   |    RMSE   |      R²   |    MAPE   |
| ------------------- | --------: | --------: | --------: | --------: |
| Mean Yield Baseline |     3.566 |     4.391 |    -0.004 |    334.4% |
| Linear Regression   |     1.333 |     1.960 |     0.800 |    113.0% |
| Gradient Boosting   |     0.917 |     1.719 |     0.846 |     50.8% |
| XGBoost             |     0.887 |     1.677 |     0.854 |     40.3% |
| **Random Forest**   | **0.859** | **1.623** | **0.863** | **41.5%** |


## Best-performing model

Random Forest
R²: 0.863
MAE: 0.859 t/ha
RMSE: 1.623 t/ha
MAPE: 41.5%

Random Forest achieved the strongest overall R² and the lowest MAE and RMSE among the four machine learning models evaluated.

The model also substantially outperformed the mean-yield baseline.

## Crop-Level Performance

The Random Forest model was also evaluated separately across the eight crops.

| Crop           |  N |    MAE | MAPE (%) |   RMSE |          R² |
| -------------- | -: | -----: | -------: | -----: | ----------: |
| Beans          | 40 | 0.2263 |    47.20 | 0.3216 |      0.0168 |
| Cowpeas        | 40 | 0.2191 |    38.76 | 0.2750 |      0.1060 |
| Irish Potatoes | 40 | 1.9124 |    29.82 | 2.2690 |      0.3268 |
| Maize          | 40 | 0.3627 |    27.68 | 0.4634 |  **0.7553** |
| Pigeon Peas    | 35 | 0.2715 |    56.44 | 0.3587 | **-0.5834** |
| Sorghum        | 40 | 0.3477 |    50.32 | 0.5178 |      0.0905 |
| Sweet Potatoes | 40 | 2.8200 |    48.92 | 3.7052 |      0.2509 |
| Wheat          | 28 | 0.5434 |    31.77 | 0.6676 |  **0.5636** |


## Key finding

Performance varied substantially across crops.

The strongest crop-level R² values were observed for:

Maize - 0.7553
Wheat - 0.5636
Irish Potatoes - 0.3268

Several crops had considerably weaker performance, while Pigeon Peas produced a negative R² (-0.5834).

This demonstrates that the overall R² of 0.863 should not be interpreted as meaning that the model performs equally well for all eight crops.

# Limitations
The model estimates yield based on historical agricultural and environmental relationships; it does not guarantee actual future harvests.
Model performance depends on the quality, coverage and representativeness of the available historical data.
Performance varies considerably across crops.
Some crops have relatively weak crop-level performance.
The negative R² for Pigeon Peas indicates that the model did not outperform the mean-yield baseline for that crop.
The overall model performance may therefore mask important differences between individual crops.
Additional agricultural observations would be valuable for improving model robustness, particularly for crops with weaker performance.

Responsible AI

The system is intended as a decision-support and estimation tool rather than an autonomous decision-maker.

**Potentially affected groups include**:

Farmers and agricultural planners who may use yield estimates
County agricultural officers
Communities that may be underrepresented in the available agricultural data

**Fairness consideration**:
The project considers Individual Fairness, where similar agricultural conditions should produce similar estimates without unjustified differences based solely on county identity.

**Responsible deployment**

A responsible deployment should:

Monitor prediction errors by crop and county
Investigate substantial performance differences
Retrain the model as new agricultural data become available
Avoid treating the model as equally reliable across all eight crops
Maintain human oversight for high-impact agricultural decisions

For the complete Responsible AI assessment, see:
reports/responsible_ai_statement.pdf