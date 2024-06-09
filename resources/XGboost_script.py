import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 

# dataset = pandas.DataFrame(Date, Product Name, Total Sales)
# dataset = dataset.drop_duplicates()

# Convert Date to numerical format
dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset['Date'] = dataset['Date'].astype('int64') // 10**9

# Extract features and target variable
X = dataset[['Date', 'Product Name']]
y = dataset['Total Sales']

# Define the preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('date', 'passthrough', ['Date']),
        ('product', OneHotEncoder(), ['Product Name'])
    ]
)

# Create a pipeline with StandardScaler (without mean centering) and XGBoost Regressor
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('scaler', StandardScaler(with_mean=False)),  # Set with_mean=False to handle sparse matrices
    ('xgb', xgb.XGBRegressor(objective='reg:squarederror', eval_metric='rmse'))
])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Predict on the entire dataset for end-user consumption
dataset['Predicted Sales'] = pipeline.predict(X)

# # Output the dataset with predictions
dataset
