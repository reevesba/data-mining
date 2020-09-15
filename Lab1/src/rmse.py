import pandas
import numpy as np
import time
import matplotlib.pyplot as plot
 
# Calculate root mean squared error
def rmse(predicted, actual):
	return np.sqrt(((predicted - actual)**2).mean())

def rmse_mean(predicted, actual):
	return np.sqrt(((predicted - actual)**2).mean())

def plot_times(times):
    #input range
    num_rows = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]

    #runtimes for each program
    python_times = times
    r_times = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    excel_times = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    m, b = np.polyfit(num_rows, python_times, 1)

    #plot each program
    line1, = plot.plot(num_rows, python_times, color='#AB0032', label='Python')
    line2, = plot.plot(num_rows, r_times, color='#000000', label='R')
    line3, = plot.plot(num_rows, excel_times, color='#BFBFBF', label='Excel')

    #add legend
    plot.legend(handles=[line1, line2, line3], title='Programs')

    #set labels
    plot.xlabel('Number of Rows')
    plot.ylabel('Run Time (s)')
    plot.title('Calculating RMSE')

    #generate plot
    plot.show()

def main():
    # test different size dataframes
    times = []
    for i in range(1, 11):
        wh_df = pandas.read_csv('dat/Weight-Height data_' + str(i) + '.csv', skiprows=1)
        start = time.time()
        res = rmse(np.asarray(wh_df["kg"].tolist()), np.asarray(wh_df["kg.1"].tolist()))
        times.append(time.time() - start)
        extra_rows = wh_df
        wh_df.append(extra_rows)

    plot_times(times)

if __name__ == '__main__':
    main()