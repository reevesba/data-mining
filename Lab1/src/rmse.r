library(Metrics) 

# Create dataframe
wh_df<-read.csv("../dat/Weight-Height data.csv", skip=1, header=TRUE)

# Test RMSE   
res = rmse(wh_df$kg, wh_df$kg.1) 
print(res)