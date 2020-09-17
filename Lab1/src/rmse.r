library(Metrics)
library(data.table)

# Set working directory
setwd("~/git/data-mining/Lab1/src")

# run validation
test_df = read.csv("../dat/Weight-Height data.csv",skip=1, header=TRUE)
print(rmse(test_df[["kg"]], test_df[["kg.1"]]))
print(sqrt(mean((mean(test_df[["kg.1"]]) - test_df[["kg"]])^2)))

# Create dataframe array for the files
dataFiles <- lapply(Sys.glob("../dat/Weight-Height data_*.csv"),skip=1, header=TRUE, read.csv)
View(dataFiles)

res = vector()
r_times = vector()

# Test for General RMSE   
for(i in 1:length(dataFiles))
{
  startTime = Sys.time()
  res[i] = rmse(dataFiles[[i]][["kg"]], dataFiles[[i]][["kg.1"]])
  r_times[i] =  Sys.time() - startTime
  
}

print(res)
print(r_times)

fwrite(list(c("Time (Sec)", r_times)), "../dat/r-benchmark.csv")

#plotting graph
num_rows = c(100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000)
plot(num_rows, r_times,type = "o", xlab= "Number of Rows", ylab="Run Time(s)")
