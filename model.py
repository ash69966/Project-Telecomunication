# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZMqN0q39TnXhhFhXaJwgiM8-D8hgP22w
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import warnings
warnings.filterwarnings(action='ignore')

df1 = pd.read_excel("/content/train (1).xlsx")
df2 = pd.read_excel("/content/test (1).xlsx")

df1

df2

df2.shape

df1.columns

df2.columns

df1 = df1.drop(columns = 'customerID')

df1.isnull().sum()

df2.isnull().sum()

df1.nunique()

df2.nunique()

df1.info()

for col in df1.columns:
    print(col)
    print(df1[f'{col}'].unique())
    print('*'*75)

for col in df2.columns:
    print(col)
    print(df2[f'{col}'].unique())
    print('*'*75)

df1['TotalCharges'] = pd.to_numeric(df1['TotalCharges'], errors='coerce')
df2['TotalCharges'] = pd.to_numeric(df2['TotalCharges'], errors='coerce')

df1['MonthlyCharges'] = pd.to_numeric(df1['MonthlyCharges'], errors='coerce')
df2['MonthlyCharges'] = pd.to_numeric(df2['MonthlyCharges'], errors='coerce')

df1.isnull().sum()

df2.isnull().sum()

df2.info()

df3 = pd.DataFrame(df1, columns = ['MonthlyCharges','TotalCharges'])  
plt.figure(figsize = (10, 20)) 
  
df3.boxplot()

df1['TotalCharges'].fillna(value=df1['TotalCharges'].mean(), inplace=True)

df1.isnull().sum()

df1.info()

df1['SeniorCitizen'].value_counts()

df2['SeniorCitizen'].value_counts()

df1['SeniorCitizen'] = df1['SeniorCitizen'].astype(object)
df2['SeniorCitizen'] = df2['SeniorCitizen'].astype(object)

df1['DeviceProtection'] = df1['DeviceProtection'].replace('yes','Yes')
df2['DeviceProtection'] = df2['DeviceProtection'].replace('yes','Yes')
df1['OnlineBackup'] = df1['OnlineBackup'].replace('no','No')
df2['OnlineBackup'] = df2['OnlineBackup'].replace('no','No')

# loop through each categorical variable and display its value counts
for col in df1.columns:
    if df1[col].dtype == 'object':  # check if column is categorical
        print(f"\nValue counts for {col}:")
        print(df1[col].value_counts())

#create a new column for the "Red" category
df1['No Internet Service'] = df1['InternetService'].apply(lambda x: 1 if x == 'No' else 0)
df2['No Internet Service'] = df2['InternetService'].apply(lambda x: 1 if x == 'No' else 0)

df1.info()

df1[df1['InternetService'] == 'No']

# replace the "No internet service" category with "no"
df1['OnlineSecurity'] = df1['OnlineSecurity'].replace('No internet service', 'No')
df2['OnlineSecurity'] = df2['OnlineSecurity'].replace('No internet service', 'No')

df1['OnlineBackup'] = df1['OnlineBackup'].replace('No internet service', 'No')
df2['OnlineBackup'] = df2['OnlineBackup'].replace('No internet service', 'No')

df1['DeviceProtection'] = df1['DeviceProtection'].replace('No internet service', 'No')
df2['DeviceProtection'] = df2['DeviceProtection'].replace('No internet service', 'No')

df1['TechSupport'] = df1['TechSupport'].replace('No internet service', 'No')
df2['TechSupport'] = df2['TechSupport'].replace('No internet service', 'No')

df1['StreamingTV'] = df1['StreamingTV'].replace('No internet service', 'No')
df2['StreamingTV'] = df2['StreamingTV'].replace('No internet service', 'No')

df1['StreamingMovies'] = df1['StreamingMovies'].replace('No internet service', 'No')
df2['StreamingMovies'] = df2['StreamingMovies'].replace('No internet service', 'No')

# loop through each categorical variable and display its value counts
for col in df1.columns:
    if df1[col].dtype == 'object':  # check if column is categorical
        print(f"\nValue counts for {col}:")
        print(df1[col].value_counts())

df1[(df1['PhoneService'] == 'No') & (df1['InternetService'] == 'No')]

df1['No Internet Service'] = df1['No Internet Service'].astype(object)
df2['No Internet Service'] = df2['No Internet Service'].astype(object)

CategoricalFeatures = [feature for feature in df1.columns if df1[feature].dtypes =='O']
NumericalFeatures = [feature for feature in df1.columns if feature not in CategoricalFeatures]

CategoricalFeatures

NumericalFeatures

for col in df2.columns:
    print(col)
    print(df2[f'{col}'].unique())
    print('*'*75)

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Select features for encoding
label_features = ['Partner','gender','MultipleLines','InternetService','Contract','PaymentMethod','PaperlessBilling','DeviceProtection','OnlineBackup']
one_hot_features = ['InternetService', 'Contract','SeniorCitizen','No Internet Service','StreamingMovies','StreamingTV','TechSupport','OnlineSecurity','PhoneService','Dependents']

# Encode features using LabelEncoder
le = LabelEncoder()
for feature in label_features:
    df1[feature] = le.fit_transform(df1[feature])

# Encode features using OneHotEncoder
ohe = OneHotEncoder(sparse=False, drop='first')
one_hot_encoded = pd.DataFrame(ohe.fit_transform(df1[one_hot_features]))
one_hot_encoded.columns = [feature + '_' + str(cat) for feature, cats in zip(one_hot_features, ohe.categories_) for cat in cats[1:]]
df1 = pd.concat([df1, one_hot_encoded], axis=1)
df1 = df1.drop(columns=one_hot_features)

df1

df1.info()

# Encode features using LabelEncoder
le = LabelEncoder()
for feature in label_features:
    df2[feature] = le.fit_transform(df2[feature])

# Encode features using OneHotEncoder
ohe = OneHotEncoder(sparse=False, drop='first')
one_hot_encoded = pd.DataFrame(ohe.fit_transform(df2[one_hot_features]))
one_hot_encoded.columns = [feature + '_' + str(cat) for feature, cats in zip(one_hot_features, ohe.categories_) for cat in cats[1:]]
df2 = pd.concat([df2, one_hot_encoded], axis=1)
df2 = df2.drop(columns=one_hot_features)

df1.columns



from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

# Select only categorical variables
cat_vars = ['gender', 'Partner', 'MultipleLines', 'OnlineBackup',
       'DeviceProtection', 'PaperlessBilling', 'PaymentMethod',  'InternetService_1',
       'InternetService_2', 'Contract_1', 'Contract_2', 'SeniorCitizen_1',
       'No Internet Service_1', 'StreamingMovies_Yes', 'StreamingTV_Yes',
       'TechSupport_Yes', 'OnlineSecurity_Yes', 'PhoneService_Yes',
       'Dependents_Yes']

X_cat = df1[cat_vars]
y = df1['Churn']

# Convert categorical variables to numerical using one-hot encoding
X_cat = pd.get_dummies(X_cat, drop_first=True)

# Select top 10 categorical features using chi-square test
selector = SelectKBest(score_func=chi2, k=10)
selector.fit(X_cat, y)

# Get the indices of the top 10 features
top_indices = selector.get_support(indices=True)

# Get the feature names of the top 10 features
top_features = [X_cat.columns[i] for i in top_indices]

print("Top 10 categorical features selected using chi-square test:")
print(top_features)

num_vars = ['tenure', 'MonthlyCharges', 'TotalCharges']

# Check for non-numeric values in continuous variables
for col in num_vars:
    mask = pd.to_numeric(df1[col], errors='coerce').isna()
    if mask.any():
        print(f"Rows with non-numeric values in {col}:\n")
        print(df1[mask][col])

df1.isnull().sum()

# Import the necessary libraries
from sklearn.feature_selection import f_classif

# Select only continuous variables
num_vars = ['tenure', 'MonthlyCharges', 'TotalCharges']

X_num = df1[num_vars]
y = df1['Churn']

# Perform ANOVA F-test for feature selection
f_values, p_values = f_classif(X_num, y)

# Create a DataFrame of the feature names, F-values, and p-values
results = pd.DataFrame({'Feature': num_vars, 'F-value': f_values, 'p-value': p_values})
results.sort_values('p-value', inplace=True)
print(results)

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Select the relevant features from the dataframe
X = df1[['InternetService_1', 'InternetService_2', 'Contract_1', 'Contract_2', 'SeniorCitizen_1', 'No Internet Service_1', 'TechSupport_Yes', 'OnlineSecurity_Yes', 'Dependents_Yes','tenure', 'MonthlyCharges', 'TotalCharges']]
y = df1['Churn']

# Convert categorical features to numerical using one-hot encoding
#X_encoded = pd.get_dummies(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Instantiate the decision tree classifier
tree = DecisionTreeClassifier(random_state=42)

# Fit the model to the training data
tree.fit(X_train, y_train)

# Make predictions on the test data
y_pred = tree.predict(X_test)

# Calculate the accuracy score of the model
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Instantiate a random forest classifier with 100 trees
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Fit the model to the training data
rf.fit(X_train, y_train)

# Predict the classes of the test set
y_pred = rf.predict(X_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

#Import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier

# Create a KNN classifier with k=5
knn = KNeighborsClassifier(n_neighbors=5)

# Fit the model on the training data
knn.fit(X_train, y_train)

# Predict the classes of the test data
y_pred = knn.predict(X_test)

# Calculate the accuracy of the model
accuracy = knn.score(X_test, y_test)

# Print the accuracy of the model
print("Accuracy:", accuracy)

df2.info()

selected_cols = ['InternetService_1', 'InternetService_2', 'Contract_1', 'Contract_2', 'No Internet Service_1', 'TechSupport_Yes', 'OnlineSecurity_Yes', 'Dependents_Yes','tenure', 'MonthlyCharges', 'TotalCharges']

df2 = df2[selected_cols].copy()

df2

pickle.dump(knn, open('model.pkl','wb'))

# Instantiate the KNN classifier with best parameters
knn = KNeighborsClassifier(n_neighbors=7, weights='uniform')

X_train = X_train.drop('SeniorCitizen_1', axis=1)
# Fit the KNN classifier on the training data
knn.fit(X_train, y_train)

# Make predictions on the test data
y_pred = knn.predict(df2)

# Print the predicted churn values
print(y_pred)

