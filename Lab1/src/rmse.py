import pandas
import numpy as np
 
# Calculate root mean squared error
def rmse(predicted, actual):
	return np.sqrt(((predicted - actual)**2).mean())

def main():
    # Create dataframe
    wh_df = pandas.read_csv('dat/Weight-Height data.csv', skiprows=1)

    # Test RMSE
    res = rmse(np.asarray(wh_df["kg"].tolist()), np.asarray(wh_df["kg.1"].tolist()))
    print(res)

if __name__ == '__main__':
    main()