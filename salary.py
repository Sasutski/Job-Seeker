# https://www.kaggle.com/datasets/amirmahdiabbootalebi/salary-by-job-title-and-country 
# Using this dataset to get the salary of a particular job title in a particular country, age, gender, country, years of experience, and education level.
# https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Set display options for better readability
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)

data = pd.read_csv("data/Salary.csv")

# Print only the first 5 rows of the dataset
print(data.head()) 

# Print concise summary of the dataset
print(data.info()) 

# Print summary statistics of the dataset
print(data.describe())  

# Fill missing values with the mean of the numeric columns
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Separate features and target variable
x = data.drop('Salary', axis=1)
y = data['Salary']

# Identify categorical columns
categorical_columns = x.select_dtypes(include=['object']).columns

# Create a column transformer with one-hot encoding for categorical variables
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ],
    remainder='passthrough'  # Keep the remaining columns as they are
)

# Create a pipeline with the preprocessor and the model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Train the model
pipeline.fit(x_train, y_train)

# Make predictions on the testing set
predictions = pipeline.predict(x_test)
try: # Right now has a classification error due to multiclass and continuous targets
    print("Classification Report: ", classification_report(y_test, predictions))
    
except ValueError:
    pass

try: # Right now has a classification error due to multiclass and continuous targets
    print("Confusion Matrix: ", confusion_matrix(y_test, predictions))
except ValueError:
    pass

try: # Right now has a classification error due to multiclass and continuous targets
    print("Accuracy Score: ", accuracy_score(y_test, predictions))
except ValueError:
    pass

# Print the model's performance
print(f"Model R^2 score: {pipeline.score(x_test, y_test)}")



def predict_salary(age, gender, education_level, job_title, years_of_experience, country, race, senior):
    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'Age': [age],
        'Gender': [gender],
        'Education Level': [education_level],
        'Job Title': [job_title],
        'Years of Experience': [years_of_experience],
        'Country': [country],
        'Race': [race],
        'Senior': [senior]
    })

    # Use the pipeline to preprocess the input data and make a prediction
    predicted_salary = pipeline.predict(input_data)
    
    return predicted_salary[0]

# Example usage
age = 30
gender = 'Male'
education_level = 4
job_title = 'Software Engineer'
years_of_experience = 1
country = 'Korea'
race = 'Asian'
senior = 0

predicted_salary = predict_salary(age, gender, education_level, job_title, years_of_experience, country, race, senior)
print(f"Predicted Salary: ${predicted_salary:.0f}")
