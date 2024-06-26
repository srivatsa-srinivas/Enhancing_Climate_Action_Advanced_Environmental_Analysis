# -*- coding: utf-8 -*-
"""Enhancing_Climate_Action_Advanced_Environmental_Data_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DjTY_-eeJaMXAjyAq7XwxUgedNOExSlz

## Enhancing Climate Action: Advanced Environmental Data Analysis

### Importing Essential Libraries for Data Analysis and Modeling

The script below imports necessary libraries and sets up a structured pipeline for data preprocessing, model training, and evaluation. It includes steps for feature standardization, dimensionality reduction, model fitting (Linear Regression and Ridge Regression), evaluation metrics calculation, and multicollinearity detection.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error
from statsmodels.stats.outliers_influence import variance_inflation_factor

"""### Dataset Loading

The code snippet below loads the dataset `AQI Data Set.csv` into a Pandas DataFrame named initial_df for further analysis and modeling. The dataset contains Air Quality Index (AQI) data, which is crucial for assessing air quality and its impact on public health.
"""

# Load the dataset
initial_df = pd.read_csv("AQI Data Set.csv")

"""### Visualization of Missing Values Before and After Filling

The below code segment visualizes missing values in the dataset `initial_df` before and after filling them with the median value of each numeric column. The left heatmap shows missing values before filling, while the right heatmap displays missing values after the filling process. This visualization helps assess the effectiveness of the imputation method and the extent of missing data in the dataset.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Visualize missing values before filling
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.heatmap(initial_df.isnull(), cbar=False, cmap='viridis', linewidths=0.5, linecolor='grey')
plt.title('Missing Values Before Filling', fontsize=16)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)
plt.tight_layout()

# Fill missing values
numeric_columns = initial_df.select_dtypes(include=np.number).columns
df = initial_df.copy()  # Create a copy of initial_df
for col in numeric_columns:
    df[col].fillna(value=df[col].median(), inplace=True)

# Visualize missing values after filling
plt.subplot(1, 2, 2)
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', linewidths=0.5, linecolor='grey')
plt.title('Missing Values After Filling', fontsize=16)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10, rotation=0)
plt.tight_layout()

plt.show()

"""The below lines of code also calculates and visualizes the distribution of missing values in `initial_df` before and after filling them. The bar plot compares missing values for each feature before (sky blue) and after (light green) filling. It helps assess imputation effectiveness and identifies features with significant missing data.



"""

# Calculate missing values counts for initial_df and df
missing_values_before = initial_df.isnull().sum()
missing_values_after = df.isnull().sum()

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(missing_values_before.index, missing_values_before.values, color='skyblue', label='Before Filling')
plt.bar(missing_values_after.index, missing_values_after.values, color='lightgreen', label='After Filling')
plt.xlabel('Features')
plt.ylabel('Number of Missing Values')
plt.title('Distribution of Missing Values Before and After Filling')
plt.xticks(rotation=90, ha='right')
plt.legend()
plt.tight_layout()
plt.show()

"""### Dropping Specified Columns and Handling Missing Valuess.

The code snippet below drops the specified columns [`Id`, `Mounths`, `O3   in æg/m3`, `AQI`] from the DataFrame `df` and handles missing values. Dropping irrelevant columns improves model performance and reduce noise, while handling missing values ensures data integrity and prevents bias in subsequent analysis.
"""

# Drop specified columns and handle missing values
df.drop(columns=["Id", "Mounths", "O3   in æg/m3", "AQI"], inplace=True)

"""### Multicollinearity Detection

In here, the code calculates the Variance Inflation Factor (VIF) for each feature in the DataFrame `df` to detect multicollinearity. Multicollinearity occurs when independent variables in a regression model are highly correlated, which can lead to unstable estimates. The VIF assesses the degree of multicollinearity by measuring how much the variance of an estimated regression coefficient is increased because of collinearity. The resulting `vif_data` DataFrame contains the features and their corresponding VIF values, providing insights into multicollinearity among the variables.
"""

# Detect multicollinearity
vif_data = pd.DataFrame()
vif_data["feature"] = df.columns
vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
print("VIF Data:")
print(vif_data)

"""### Visualization of VIF Before and After Dropping Columns

The below lines of code visualizes the Variance Inflation Factor (VIF) values for each feature before dropping columns. The bar plot displays the VIF values on the y-axis and the features on the x-axis. A higher VIF indicates stronger multicollinearity. This visualization helps in identifying features with high multicollinearity, guiding the decision-making process for dropping columns to improve model performance and stability.
"""

# Visualize VIF before dropping columns
plt.figure(figsize=(8, 5))
plt.bar(vif_data["feature"], vif_data["VIF"], color='skyblue')
plt.xlabel('Features')
plt.ylabel('VIF')
plt.title('VIF Before Dropping Columns')
plt.xticks(rotation=90)
plt.show()

"""
In thibelow s code snippet, variables with high Variance Inflation Factor (VIF) are dropped from the dataset, as indicated by the removal of the column "NOx in æg/m3" from the DataFrame `df`. The VIF quantifies the severity of multicollinearity, and dropping variables with high VIF values helps mitigate multicollinearity issues in the regression analysis.

Subsequently, the VIF is recalculated for the reduced dataset (`df_reduced`), and the results are stored in a DataFrame `vif_data_reduced`. This allows for the visualization and assessment of multicollinearity in the dataset after dropping the specified columns."""

# Drop the variables with high VIF
df_reduced = df.drop(columns=["NOx  in æg/m3"])

# Visualize VIF after dropping columns
vif_data_reduced = pd.DataFrame()
vif_data_reduced["feature"] = df_reduced.columns
vif_data_reduced["VIF"] = [variance_inflation_factor(df_reduced.values, i) for i in range(len(df_reduced.columns))]

"""Code below visualizes the Variance Inflation Factor (VIF) values for each feature after dropping columns with high multicollinearity. The bar plot displays the VIF values on the y-axis and the features on the x-axis. By dropping columns with high VIF, multicollinearity is reduced, leading to lower VIF values for the remaining features. This visualization helps confirm the effectiveness of the column dropping process in mitigating multicollinearity issues."""

plt.figure(figsize=(8, 6))
plt.bar(vif_data_reduced["feature"], vif_data_reduced["VIF"], color='lightgreen')
plt.xlabel('Features')
plt.ylabel('VIF')
plt.title('VIF After Dropping Columns')
plt.xticks(rotation=45)
plt.show()

"""### Correlation Heatmap of Remaining Features

This code snippet calculates the correlation matrix for the reduced DataFrame `df_reduced` and visualizes it as a heatmap. The heatmap displays the pairwise correlation coefficients between all remaining features, with annotations indicating the correlation values. This visualization helps identify patterns of association between features and assesses the strength and direction of their relationships.
"""

from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate correlation matrix
correlation_matrix = df_reduced.corr()

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f")
plt.title('Correlation Heatmap of All Existing Columns', fontsize=16)
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

"""### VIF Calculation After Dropping Columns

The below code calculates the Variance Inflation Factor (VIF) for each feature in the reduced DataFrame `df_reduced` after dropping columns with high multicollinearity. The resulting DataFrame `vif_data_reduced` contains the features and their corresponding VIF values. This step assesses the multicollinearity among the remaining features and helps confirm the effectiveness of the column dropping process in reducing multicollinearity.
"""

vif_data_reduced = pd.DataFrame()
vif_data_reduced["feature"] = df_reduced.columns
vif_data_reduced["VIF"] = [variance_inflation_factor(df_reduced.values, i) for i in range(len(df_reduced.columns))]

"""### Standardization and PCA Dimensionality Reduction

Following code standardizes the features in the reduced DataFrame `df_reduced` using StandardScaler and then applies Principal Component Analysis (PCA) to reduce dimensionality while retaining 95% of the variance. The scaled data is transformed using PCA, resulting in a new dataset `data_pca` with reduced dimensions. This preprocessing step is essential for reducing the computational complexity of the dataset while preserving most of its variance for subsequent analysis or modeling.
"""

# Standardize and apply PCA
scaler = StandardScaler()
data_scaled = scaler.fit_transform(df_reduced)
pca = PCA(n_components=0.95)  # Adjust components to explain 95% of variance
data_pca = pca.fit_transform(data_scaled)

"""### Data Preparation for Regression

Below code prepares the data for regression analysis by splitting the principal components (X) and the target variable `PM10 in æg/m3` (y) into training and testing sets. The data is split into 80% training and 20% testing sets using the train_test_split function with a specified random state for reproducibility. This step ensures that the model is trained on a subset of the data and evaluated on unseen data to assess its generalization performance.
"""

# Prepare data for regression
target_variable = df_reduced["PM10 in æg/m3"]
X_train, X_test, y_train, y_test = train_test_split(data_pca, target_variable, test_size=0.2, random_state=42)

"""### Linear Regression Modeling

The following code snippet fits a Linear Regression model to the training data using the principal components (`X_train`) and the target variable (`y_train`). After fitting the model, it predicts the target variable for the testing data (`X_test`) and calculates the coefficient of determination (`R-squared`) and Mean Squared Error (`MSE`) as performance metrics. This step evaluates the model's ability to explain the variance in the target variable and assesses its predictive accuracy.
"""

# Linear Regression Model
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred_linear = linear_model.predict(X_test)
r2_linear = r2_score(y_test, y_pred_linear)
mse_linear = mean_squared_error(y_test, y_pred_linear)

"""### Ridge Regression Modeling

The code below fits a Ridge Regression model to the training data using the principal components (`X_train`) and the target variable (`y_train`), with a regularization strength (`alpha`) set to 1.0. After fitting the model, it predicts the target variable for the testing data (`X_test`) and calculates the coefficient of determination (`R-squared`) and Mean Squared Error (`MSE`) as performance metrics. Ridge Regression introduces regularization to the Linear Regression model, aiming to reduce overfitting and improve generalization performance.
"""

# Ridge Regression Model
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
y_pred_ridge = ridge_model.predict(X_test)
r2_ridge = r2_score(y_test, y_pred_ridge)
mse_ridge = mean_squared_error(y_test, y_pred_ridge)

"""### Cross-validation for Model Evaluation

The following lines of code performs cross-validation for both Linear Regression and Ridge Regression models to evaluate their performance. The mean R-squared values and Mean Squared Error (`MSE`) are calculated using `5-fold cross-validation` on the training data. These metrics provide insights into the models' generalization capabilities and predictive accuracy. The performance metrics are printed before and after dropping columns, allowing for comparison and assessing the impact of feature reduction on model performance.

**Before Dropping Columns:**
Linear Regression achieved an `R-squared` of approximately `0.98` and a mean squared error (`MSE`) of `8.15`, indicating a strong predictive performance and good fit to the data. The mean cross-validation (`CV`) score for Linear Regression is `0.98`, suggesting consistent performance across different folds.

**After Dropping Columns:**
After applying Ridge Regression and dropping columns, the model's performance improved slightly with an `R-squared` of around `0.99` and a reduced `MSE` of `7.29`. The mean CV score for Ridge Regression is comparable to Linear Regression, indicating stable performance even after regularization.

**Analysis:**
The Ridge Regression model, which includes regularization to mitigate overfitting, demonstrates improved performance in terms of R-squared and MSE compared to the regular Linear Regression model. However, the difference in performance metrics between the two models is relatively small. This suggests that while dropping columns and applying regularization can lead to slight improvements in model performance, the original Linear Regression model already performs well on its own.urther.
"""

# Cross-validation for Linear Regression
cv_scores_linear = cross_val_score(linear_model, X_train, y_train, cv=5)
# Cross-validation for Ridge Regression
cv_scores_ridge = cross_val_score(ridge_model, X_train, y_train, cv=5)

# Collect metrics before and after dropping columns
r2_before = [r2_linear]
mse_before = [mse_linear]
cv_before = [np.mean(cv_scores_linear)]

r2_after = [r2_ridge]
mse_after = [mse_ridge]
cv_after = [np.mean(cv_scores_ridge)]

# Print performance metrics before dropping columns
print("Before Dropping Columns:")
print("Linear Regression R-squared:", r2_linear)
print("Linear Regression MSE:", mse_linear)
print("Mean CV Score for Linear Regression:", np.mean(cv_scores_linear))

# Print performance metrics after dropping columns
print("\nAfter Dropping Columns:")
print("Ridge Regression R-squared:", r2_ridge)
print("Ridge Regression MSE:", mse_ridge)
print("Mean CV Score for Ridge Regression:", np.mean(cv_scores_ridge))

"""### Visual Comparison of Performance Metrics Before and After Dropping Columns

The bar plot obtained below visually compares the performance metrics (R-squared, MSE, and Mean CV Score) before and after dropping columns. The blue bars represent the metrics before dropping columns, while the green bars represent the metrics after dropping columns. The plot allows for easy comparison of the model's performance improvements or deteriorations after feature reduction.
"""

# Visual comparison of performance metrics before and after dropping columns
labels = ['R-squared', 'MSE', 'Mean CV Score']
before_metrics = [r2_before[0], mse_before[0], cv_before[0]]
after_metrics = [r2_after[0], mse_after[0], cv_after[0]]

x = np.arange(len(labels))
width = 0.30

fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar(x - width/2, before_metrics, width, label='Before Dropping Columns', color='skyblue')
rects2 = ax.bar(x + width/2, after_metrics, width, label='After Dropping Columns', color='lightgreen')

ax.set_ylabel('Metrics')
ax.set_title('Comparison of Metrics Before and After Dropping Columns')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.show()

"""### Residual Plots for Linear and Ridge Regression

The following code creates side-by-side residual plots for both Linear Regression and Ridge Regression models. Each plot displays the residuals (the difference between the actual and predicted values) against the predicted values. The lowess curve represents the locally weighted scatterplot smoothing, providing insights into the relationship between the predicted values and residuals. The red horizontal line at y=0 indicates perfect prediction, where residuals are centered around zero. These plots help assess the models' performance and check for any patterns or heteroscedasticity in the residuals.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plotting residuals for Linear Regression
sns.residplot(x=y_pred_linear, y=y_test - y_pred_linear, lowess=True, color="g", ax=axes[0])
axes[0].axhline(y=0, color='r', linestyle='-')
axes[0].set_title("Residual Plot for Linear Regression")
axes[0].set_xlabel("Predicted Values")
axes[0].set_ylabel("Residuals")

# Plotting residuals for Ridge Regression
sns.residplot(x=y_pred_ridge, y=y_test - y_pred_ridge, lowess=True, color="b", ax=axes[1])
axes[1].axhline(y=0, color='r', linestyle='-')
axes[1].set_title("Residual Plot for Ridge Regression")
axes[1].set_xlabel("Predicted Values")
axes[1].set_ylabel("Residuals")

# Set overall title
plt.suptitle("Residual Plots for Linear and Ridge Regression", fontsize=22)

plt.tight_layout()
plt.show()

"""### Comparison of Actual vs. Predicted Values for Linear and Ridge Regression

The scatter plot code below compares the actual target values (`y_test`) with the predicted values (`y_pred`) for both Linear Regression (in green) and Ridge Regression (in blue) models. The diagonal red dashed line represents perfect prediction, where the actual and predicted values are identical. Comparing the distribution of points around this line allows us to visually assess the accuracy and performance of the regression models. Points closer to the diagonal line indicate better prediction accuracy, while deviations from the line suggest model errors or biases.s.
"""

# Visual comparison of Predicted vs Actual values for both models
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_linear, color="green", label="Linear")
plt.scatter(y_test, y_pred_ridge, color="blue", label="Ridge")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], linestyle='--', color='r')
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values for Linear and Ridge Regression")
plt.legend()

"""### Performance Metrics Overview

The following code snippet prints the performance metrics for both Linear Regression and Ridge Regression models. The metrics include R-squared (a measure of the proportion of variance explained by the model), Mean Squared Error (MSE), and cross-validation (CV) scores. Additionally, it calculates the mean CV score for each model, providing insights into their overall performance and generalization capabilities. These metrics serve as key indicators for assessing the accuracy and reliability of the regression models.

**Analysis**
Both Linear Regression and Ridge Regression models demonstrate strong performance in predicting the target variable, as evidenced by high R-squared values. However, Ridge Regression slightly outperforms Linear Regression, achieving a higher `R-squared value` of approximately `0.986` compared to `0.985` for Linear Regression. Similarly, Ridge Regression exhibits a lower `Mean Squared Error (MSE)` of approximately `7.29`, indicating better accuracy in prediction compared to the `MSE` of approximately `8.15` for Linear Regression.

The cross-validation (CV) scores further support the robustness of both models, with consistently high scores across different folds of the training data. The mean CV scores for Linear Regression and Ridge Regression are comparable, indicating stable performance and generalization capabilities for both models.

In conclusion, Ridge Regression shows a marginal improvement over Linear Regression in terms of R-squared and MSE, suggesting that the regularization introduced in Ridge Regression helps improve model performance and reduce prediction errors.rrors.s.
"""

# Print performance metrics
print("Linear Regression R-squared:", r2_linear)
print("Linear Regression MSE:", mse_linear)
print("Ridge Regression R-squared:", r2_ridge)
print("Ridge Regression MSE:", mse_ridge)
print("Linear Regression CV Scores:", cv_scores_linear)
print("Mean CV Score for Linear Regression:", np.mean(cv_scores_linear))
print("Ridge Regression CV Scores:", cv_scores_ridge)
print("Mean CV Score for Ridge Regression:", np.mean(cv_scores_ridge))