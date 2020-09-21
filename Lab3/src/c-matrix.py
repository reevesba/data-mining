# Implement a two-class confusion matrix using your own code with computing  FP, FN, TP, TN, AC (accuracy), P (precision), R (recall).

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

raw_data = load_wine()

df = pd.DataFrame(data=raw_data['data'], columns=raw_data['feature_names'])

df['target'] = raw_data['target']
df['class'] = df['target'].map(lambda i: raw_data['target_names'][i])

# convert to binary classifier: in class_0 (class_0), not in class_0 (class_1)
df.loc[df['target'] == 2, 'target'] = 1
df.loc[df['class'] == 'class_2', 'class'] = 'class_1'

df.to_csv('dat/wine-data.csv')
predictors = df.columns[:len(df.columns) - 2]
X = df[predictors]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = DecisionTreeClassifier()

# train Decision Tree Classifer
clf = clf.fit(X_train, y_train)

# predict the response for test dataset
y_pred = clf.predict(X_test)

a, b, c, d = metrics.confusion_matrix(y_test, y_pred).ravel()

# accuracy
AC = (a + d)/(a + b + c + d)
print("AC:", AC)

# true positive rate (recall)
TP = d/(c + d)
print("TP (R):", TP)

# false positive rate
FP = b/(a + b)
print("FP:", FP)

# true negative rate
TN = a/(a + b)
print("TN:", TN)

# false negative rate
FN = c/(c + d)
print("FN:", FN)

# precision
P = d/(b + d)
print("P:", P)

