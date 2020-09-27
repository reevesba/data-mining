# Implement a two-class confusion matrix using your own code with 
# computing  FP, FN, TP, TN, AC (accuracy), P (precision), R (recall).

# decision tree with rpart
library(rpart)
library(rpart.plot)
library(caret)

# Set working directory
setwd("~/git/data-mining/Lab3/src")

# load dataframe
wine_df = read.csv("../dat/wine-data.csv", header=TRUE)

# remove unneccesay columns
wine_df = subset(wine_df, select = -c(X, class))

# split into training/testing sets
set.seed(509)

# train percentage
train <- sample(1:nrow(wine_df), size = ceiling(0.8*nrow(wine_df)), replace = FALSE)

training_df <- wine_df[train,]
testing_df <- wine_df[-train,]

# grow tree
my_tree <- rpart(target~., data = training_df, method = "class")

# visualize tree
rpart.plot(my_tree, nn = TRUE)


# testing model
predictions <-  predict(object = my_tree, testing_df[1:length(testing_df) - 1], type = "class")

# create a confusion matrix
my_table <- table(testing_df$target, predictions)

a <- my_table[1, "0"]
b <- my_table[1, "1"]
c <- my_table[2, "0"]
d <- my_table[2, "1"]

# final calculations based on confusion matrix values

# accuracy
AC = (a + d)/(a + b + c + d)
print(paste0("AC: ", formatC(100*AC, digits = 2, format = "f"), "%"))

# true positive rate (recall)
TP = d/(c + d)
print(paste0("TP (R): ", TP))

# false positive rate
FP = b/(a + b)
print(paste0("FP: ", FP))

# true negative rate
TN = a/(a + b)
print(paste0("TN: ", TN))

# false negative rate
FN = c/(c + d)
print(paste0("FN: ", FN))

# precision
P = d/(b + d)
print(paste0("P: ", P))



