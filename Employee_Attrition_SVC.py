import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import GridSearchCV, train_test_split    
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC

df = pd.DataFrame(pd.read_csv(r"D:\electronics\Agentic AI\WA_Fn-UseC_-HR-Employee-Attrition.csv"))
#print(df)
print("Dataset Shape:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nDataset Info:")
df.info()
print(df.isnull().sum())
print("Total Missing Values:", df.isnull().sum().sum())
print("Duplicate Rows:", df.duplicated().sum())
print("Statical Summary ",df.describe())
# check for unique values in each column
for column in df.columns:
    print(f"\nUnique Values in '{column}':")
    print(df[column].unique())

# Remove unnecessary columns
df = df.drop(
    columns=[
        'EmployeeCount',
        'EmployeeNumber',
        'Over18',
        'StandardHours'
    ]
)
print("New Dataset Shape:", df.shape)
print("\nRemaining Columns:")
#print(df.columns.tolist())
# -------Attrition data analayse------------
# Count employees based on Attrition
print(df['Attrition'].value_counts())
attrition_rate = (df['Attrition'].value_counts()['Yes'] / len(df)) * 100
print("Attrition Rate:", round(attrition_rate, 2), "%")
# plt.figure(figsize=(6, 4))
# sns.countplot(data=df, x='Attrition')
# plt.title("Employee Attrition Distribution")
# plt.xlabel("Attrition")
# plt.ylabel("Number of Employees")
# plt.show()
# print(pd.crosstab(df['Department'], df['Attrition']))
# pd.crosstab(
#     df['Department'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='Department',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Department vs Employee Attrition")
# plt.xlabel("Department")
# plt.ylabel("Number of Employees")

# plt.show()
# department_attrition = pd.crosstab(
#     df['Department'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(department_attrition, 2))
# #----------Job Role vs Attrition----------------
# print(pd.crosstab(df['JobRole'], df['Attrition']))
# pd.crosstab(
#     df['JobRole'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='JobRole',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Job Role vs Employee Attrition")
# plt.xlabel("Job Role")
# plt.ylabel("Number of Employees")
# plt.xticks(rotation=45)

# plt.show()
# JobRole_attrition = pd.crosstab(
#     df['JobRole'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(JobRole_attrition, 2))
# #----------YearsAtCompany vs Attrition----------------
# print(pd.crosstab(df['YearsAtCompany'], df['Attrition']))
# pd.crosstab(
#     df['YearsAtCompany'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.boxplot(
#     data=df,
#     x='YearsAtCompany',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Years at Company vs Employee Attrition")
# plt.xlabel("Years at Company")
# plt.ylabel("Number of Employees")

# plt.show()
# years_at_company_attrition = pd.crosstab(
#     df['YearsAtCompany'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(years_at_company_attrition, 2))

# #----------DistanceFromHome vs Attrition----------------

# print(pd.crosstab(df['DistanceFromHome'], df['Attrition']))
# pd.crosstab(
#     df['DistanceFromHome'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='DistanceFromHome',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Distance from Home vs Employee Attrition")
# plt.xlabel("Distance from Home")
# plt.ylabel("Number of Employees")

# plt.show()
# distance_from_home_attrition = pd.crosstab(
#     df['DistanceFromHome'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(distance_from_home_attrition, 2))

# #----------OverTime vs Attrition----------------
# print(pd.crosstab(df['OverTime'], df['Attrition']))
# pd.crosstab(
#     df['OverTime'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='OverTime',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("OverTime vs Employee Attrition")
# plt.xlabel("OverTime")
# plt.ylabel("Number of Employees")

# plt.show()
# overtime_attrition = pd.crosstab(
#     df['OverTime'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(overtime_attrition, 2))

# #-------------JobSatisfaction  vs Attrition----------------
# print(pd.crosstab(df['JobSatisfaction'], df['Attrition']))
# pd.crosstab(
#     df['JobSatisfaction'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='JobSatisfaction',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Job Satisfaction vs Employee Attrition")
# plt.xlabel("Job Satisfaction")
# plt.ylabel("Number of Employees")

# plt.show()
# job_satisfaction_attrition = pd.crosstab(
#     df['JobSatisfaction'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(job_satisfaction_attrition, 2))

# #------------- 'YearsSinceLastPromotion vs Attrition----------------
# print(pd.crosstab(df['YearsSinceLastPromotion'], df['Attrition']))
# pd.crosstab(
#     df['YearsSinceLastPromotion'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.countplot(
#     data=df,
#     x='YearsSinceLastPromotion',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Years Since Last Promotion vs Employee Attrition")
# plt.xlabel("Years Since Last Promotion")
# plt.ylabel("Number of Employees")

# plt.show()
# years_since_last_promotion_attrition = pd.crosstab(
#     df['YearsSinceLastPromotion'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(years_since_last_promotion_attrition, 2))

# #------------MonthlyIncome  vs Attrition----------------
# print(pd.crosstab(df['MonthlyIncome'], df['Attrition']))
# pd.crosstab(
#     df['MonthlyIncome'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.boxplot(
#     data=df,
#     x='MonthlyIncome',
#     hue='Attrition' # do alg alg graph to understand clearly for no or yes attrition
# )

# plt.title("Monthly Income vs Employee Attrition")
# plt.xlabel("Monthly Income")
# plt.ylabel("Number of Employees")

# plt.show()
# monthly_income_attrition = pd.crosstab(
#     df['MonthlyIncome'],
#     df['Attrition'],
#     normalize='index'
# ) * 100

# print(round(monthly_income_attrition, 2))

# #-------------Age vs Attrition----------------
# print(pd.crosstab(df['Age'], df['Attrition']))
# pd.crosstab(
#     df['Age'],
#     df['Attrition']
# )
# plt.figure(figsize=(8, 5))

# sns.boxplot(
#     data=df,
#     x='Age',
#     hue='Attrition'
# )

# plt.title("Age vs Employee Attrition")
# plt.xlabel("Age")
# plt.ylabel("Number of Employees")

# plt.show()
# age_attrition = pd.crosstab(
#     df['Age'],
#     df['Attrition'],
#     normalize='index'
# ) * 100
# print(round(age_attrition, 2))

#-------------Important Insights----------------
# 1. Overall Attrition Rate
print("Overall Attrition Rate:")
print((df['Attrition'].value_counts(normalize=True) * 100).round(2))


# 2. Department-wise Attrition Rate
print("\nDepartment-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['Department'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)

# 3. Job Role-wise Attrition Rate
print("\nJob Role-wise Attrition Rate:")
print(round(
    pd.crosstab(
        df['JobRole'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2
))

# 4. OverTime-wise Attrition Rate
print("\nOverTime-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['OverTime'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)
# 5. YearsAtCompany -wise Attrition Rate
print("\nYearsAtCompany-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['YearsAtCompany'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)
# 6. DistanceFromHome-wise Attrition Rate
print("\nDistanceFromHome-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['DistanceFromHome'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)

# 7. JobSatisfaction-wise Attrition Rate
print("\nJobSatisfaction-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['JobSatisfaction'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)

# 8. YearsSinceLastPromotion-wise Attrition Rate
print("\nYearsSinceLastPromotion-wise Attrition Rate:")
print(
      round(pd.crosstab(
        df['YearsSinceLastPromotion'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)
# 9. MonthlyIncome-wise Attrition Rate
print("\nMonthlyIncome-wise Attrition Rate:")
print(round(
    pd.crosstab(
        df['MonthlyIncome'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2
))

# 10. Age-wise Attrition Rate
print("\nAge-wise Attrition Rate:")
print(
    round(pd.crosstab(
        df['Age'],
        df['Attrition'],
        normalize='index'
    ) * 100, 2)
)

# 11. Average values
print("\nAverage Values by Attrition:")

average_values = df.groupby('Attrition')[
    [
        'Age',
        'MonthlyIncome',
        'YearsAtCompany',
        'DistanceFromHome',
        'JobSatisfaction',
        'YearsSinceLastPromotion'
    ]
].mean()
print(round(average_values, 2))

#----------------Data Preprocessing----------------
# Convert categorical variables to numerical using one-hot encoding
df_encoded = pd.get_dummies(df, drop_first=True)
X = df_encoded.drop('Attrition_Yes', axis=1)
y = df_encoded['Attrition_Yes']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)   
model = SVC(
    C=1,
    gamma='scale',
    kernel='rbf',
    class_weight='balanced',
    probability=True,
    random_state=42
)
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.01, 0.1],
    'kernel': ['rbf', 'linear']
}

grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("Best Parameters:")
print(grid_search.best_params_)

print("\nBest CV Score:")
print(grid_search.best_score_)
model.fit(X_train, y_train)
grid = grid_search.best_estimator_
predictions= grid.predict(X_test)
print(predictions)
print("\nActual Attrition:")
print(y_test.values)
print("\nPredicted Attrition:")
print(predictions)

# ROC-AUC Score
roc_score = roc_auc_score(y_test, predictions)

print("ROC-AUC Score:", roc_score)
#-----------------Accuracy Score----------------------------
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", round(accuracy, 2))
# --------------- Confusion Matrix--------------------------
cm = confusion_matrix(y_test, predictions)#prediction  or actual me diffrence
print("Confusion Matrix:")
print(cm)
#-----------------Classification Report---------------------
print("\nClassification Report:")
print(classification_report(y_test, predictions))


