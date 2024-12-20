import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR

# Step 1: Load the dataset
data = pd.read_csv('Fuel_cell_performance_data-Full.csv')
print("Dataset Loaded Successfully!")

# Step 2: Select Target5 and drop other targets
target_col = 'Target5'
data = data[[target_col] + [col for col in data.columns if col != target_col]]
print(f"Data filtered to keep only {target_col}")

# Step 3: Split the dataset into 70% training and 30% testing
X = data.drop(columns=[target_col])  # Features
y = data[target_col]  # Target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print("Data split into training and testing sets.")

# Step 4: Placeholder for storing results
results = []

# Step 5: Function to train and evaluate models
def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    results.append({'Model': name, 'MSE': mse, 'R2 Score': r2})

# Step 6: Train and evaluate multiple models
# (a) Linear Regression
lr_model = LinearRegression()
evaluate_model('Linear Regression', lr_model, X_train, X_test, y_train, y_test)

# (b) Random Forest
rf_model = RandomForestRegressor(random_state=42)
evaluate_model('Random Forest', rf_model, X_train, X_test, y_train, y_test)

# (c) Gradient Boosting
gb_model = GradientBoostingRegressor(random_state=42)
evaluate_model('Gradient Boosting', gb_model, X_train, X_test, y_train, y_test)

# (d) Support Vector Machine
svr_model = SVR()
evaluate_model('Support Vector Machine', svr_model, X_train, X_test, y_train, y_test)

# Step 7: Create a DataFrame for results
results_df = pd.DataFrame(results)

# Step 8: Display the results in tabular form
print("\nModel Evaluation Results:")
print(results_df)

# Step 9: Save results to a CSV file
results_df.to_csv('model_results.csv', index=False)
print("\nResults saved to 'model_results.csv'")