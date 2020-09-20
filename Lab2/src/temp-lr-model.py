import pandas as pd
import math as m
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, median_absolute_error, mean_squared_error

# add attributes to dataframe
def add_attr(df, attr, N):
    rows = df.shape[0]
    nth_prior_values = [None]*N + [df[attr][i - N] for i in range(N, rows)]
    col_name = "{}_{}".format(attr, N)
    df.insert(N + 2, col_name, nth_prior_values, True)

# create dataframe
def get_df():
    df = pd.read_csv('dat/eburg-temp.csv').set_index('DATE')
    df = df[['PRCP', 'TMAX', 'TMIN']]

    for attr in df:
        if attr != 'DATE':
            for N in range(1, 5):
                add_attr(df, attr, N)

    return df.dropna()

def build_lm(X, y):
    # split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # build linear model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # make a prediction set using the test set
    prediction = model.predict(X_test)

    # evaluate the prediction accuracy of the model
    print(y.name + " Temp Linear Model:")
    print("Explained Variance: %.2f" % model.score(X_test, y_test))
    print("Mean Absolute Error: %.2f\N{DEGREE SIGN}F" % mean_absolute_error(y_test, prediction))
    print("Median Absolute Error: %.2f\N{DEGREE SIGN}F" % median_absolute_error(y_test, prediction))
    print("Root Mean Square Error: %.2f\n" % m.sqrt(mean_squared_error(y_test, prediction)))

def max_temp_model(df):
    predictors = ['PRCP', 'PRCP_1', 'PRCP_2', 'PRCP_3', 'PRCP_4', 
                  'TMIN', 'TMIN_1', 'TMIN_2', 'TMIN_3', 'TMIN_4', 
                  'TMAX_1', 'TMAX_2', 'TMAX_3', 'TMAX_4']

    X = df[predictors]
    y = df['TMAX']

    build_lm(X, y)

def min_temp_model(df):
    predictors = ['PRCP', 'PRCP_1', 'PRCP_2', 'PRCP_3', 'PRCP_4', 
                  'TMIN_1', 'TMIN_2', 'TMIN_3', 'TMIN_4', 
                  'TMAX', 'TMAX_1', 'TMAX_2', 'TMAX_3', 'TMAX_4']

    X = df[predictors]
    y = df['TMIN']

    build_lm(X, y)

def main():
    df = get_df()
    max_temp_model(df)
    min_temp_model(df)

if __name__ == '__main__':
    main()


