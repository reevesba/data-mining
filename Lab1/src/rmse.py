import pandas
import numpy as np
import time
import matplotlib.pyplot as plot

# test function
def validate_rmse():
    wh_df = pandas.read_csv('dat/Weight-Height data.csv', skiprows=1)
    print("RMSE = " + str(rmse(np.asarray(wh_df["kg"].tolist()), np.asarray(wh_df["kg.1"].tolist()))))
    print("Mean RMSE = " + str(rmse_mean(np.asarray(wh_df["kg"].tolist()), np.asarray(wh_df["kg.1"].tolist()))))

# Calculate root mean squared error
def rmse(actual, predicted):
	return np.sqrt(((predicted - actual)**2).mean())

def rmse_mean(actual, predicted):
    p_mean = predicted.mean()
    return np.sqrt(((p_mean - actual)**2).mean())

def plot_times(times):
    # input range
    num_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]

    # runtimes for each program
    python_times = times
    r_times = pandas.read_csv('dat/r-benchmark.csv')["Time (Sec)"].tolist()
    excel_times = pandas.read_csv('dat/excel-benchmark.csv')["Time (Sec)"].tolist()

    # curve fittings
    py_coefs = np.polynomial.polynomial.polyfit(num_rows, python_times, 1)
    py_ffit = np.polynomial.polynomial.polyval(num_rows, py_coefs)
    r_coefs = np.polynomial.polynomial.polyfit(num_rows, r_times, 1)
    r_ffit = np.polynomial.polynomial.polyval(num_rows, r_coefs)
    ex_coefs = np.polynomial.polynomial.polyfit(num_rows, excel_times, 1)
    ex_ffit = np.polynomial.polynomial.polyval(num_rows, ex_coefs)

    # plot each line
    line1, = plot.plot(num_rows, py_ffit, color='#AB0032', label='Python')
    line2, = plot.plot(num_rows, r_ffit, color='#000000', label='R')
    line3, = plot.plot(num_rows, ex_ffit, color='#BFBFBF', label='Excel')

    # add legend
    plot.legend(handles=[line1, line2, line3], title='Programs')

    # set labels
    plot.xlabel('Number of Rows')
    plot.ylabel('Run Time (s)')
    plot.title('Calculating RMSE')

    # generate plot
    plot.savefig('out/run_times.png')

def main():
    validate_rmse()

    # test different size dataframes
    times = []
    for i in range(1, 11):
        wh_df = pandas.read_csv('dat/Weight-Height data_' + str(i) + '.csv', skiprows=1)
        start = time.time()
        res = rmse(np.asarray(wh_df["kg"].tolist()), np.asarray(wh_df["kg.1"].tolist()))
        times.append(time.time() - start)

    plot_times(times)

if __name__ == '__main__':
    main()