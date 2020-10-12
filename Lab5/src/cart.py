"""
Decision Tree Classifier
Uses gini index

adapted from https://github.com/random-forests/tutorials/blob/master/decision_tree.ipynb 
"""

import csv
from numpy import asarray
from random import randrange

# holds a dictionary of class
class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

# this holds a reference to the question, and to the two child nodes
class Decision_Node:
    def __init__(self,  question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

# used to partition a dataset
# records a column number and value
class Question:
    def __init__(self, column, value, header):
        self.column = column
        self.value = value
        self.header = header

    # compare the feature value in an example to the
    # feature value in this question
    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    # print question in a readable format
    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            self.header[self.column], condition, str(self.value))

### tree functions ###

# find the unique values for a column in a dataset
def unique_vals(rows, col):
    return set([row[col] for row in rows])

# test if value is numeric
def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)

# partitions a dataset
def partition(rows, question):
    # for each row in the dataset, check if it matches the question
    # if so, add it to 'true rows', otherwise, add it to 'false rows'
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

# counts the number of each type of class in a dataset
def class_counts(rows):
    counts = {}
    for row in rows:
        # in our dataset, the target is the last column
        lbl = row[-1]
        if lbl not in counts:
            counts[lbl] = 0
        counts[lbl] += 1
    return counts

# gini index = 1 - sum of squared probabilities of each group
def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        p = counts[lbl]/float(len(rows))
        impurity -= p**2
    return impurity

# uncertainty of the starting node, minus the weighted impurity 
# of two child nodes.
def info_gain(left, right, current_uncertainty):
    p_left = float(len(left))/(len(left) + len(right))
    p_right = 1 - p_left
    return current_uncertainty - (p_left*gini(left) + p_right*gini(right))

# find the best question to ask by iterating over every feature/value
# and calculating the information gain
def find_best_split(rows, header):
    # set defaults
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1

    # check every row value of every column
    for col in range(n_features):
        # first step, get the unique values in column
        # prevents duplicating work
        values = set([row[col] for row in rows])
        for val in values:
            # create question object
            question = Question(col, val, header)

            # split rows based on question
            true_rows, false_rows = partition(rows, question)

            # skip this split if it doesn't divide the dataset
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question

def build_tree(rows, max_depth, header, depth=0):
    # return the question that produces the highest gain
    gain, question = find_best_split(rows, header)

    # base case 1: no further info gain
    if gain == 0:
        return Leaf(rows)

    # base case 2: reached max depth
    if depth >= max_depth:
        return Leaf(rows)

    # if we reach here, we have found a useful feature/value
    # to partition on and haven't reached max depth
    true_rows, false_rows = partition(rows, question)

    # recursively build the true branch
    true_branch = build_tree(true_rows, max_depth, header, depth + 1)

    # recursively build the false branch
    false_branch = build_tree(false_rows, max_depth, header, depth + 1)

    # returns question node and branches to follow
    return Decision_Node(question, true_branch, false_branch)


def print_tree(node, spacing=""):
   # base case: we've reached a leaf
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return

    # print the question at this node
    print(spacing + str(node.question))

    # call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # call this function recursively on the false branch
    print(spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

def classify(row, node):
    # base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # decide whether to follow the true-branch or the false-branch
    # compare the feature/value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def print_leaf(counts):
    # print predictions at leaf
    total = sum(counts.values())*1.0
    probs = {}
    for lbl in counts.keys():
        # format probabilites as percentages
        probs[lbl] = str(int(counts[lbl]/total*100)) + "%"
    return probs

### data utility functions ###

def get_data(datafile):
    return list(csv.reader(open(datafile)))

# use only if all data should be float
def to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

def train_test_split(dataset, split=0.20):
    test = list()
    train_size = split * len(dataset)
    train = list(dataset)
    while len(test) < train_size:
        index = randrange(len(train))
        test.append(train.pop(index))
    return train, test

def predict(testing_data, my_tree):
    for row in testing_data:
        print ("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, my_tree))))

def confusion_matrix(testing_data, my_tree):
    # create a confusion matrix
    TN, FP, FN, TP = 0, 0, 0, 0
    
    for row in testing_data:
        counts = classify(row, my_tree)

        actual = row[-1]
        prediction = max(counts, key=counts.get)
        
        # 0 is malignant (positive), 1 is benign (negative)
        if actual == 1.0:
            if prediction == 1.0:
                TN += 1
            else:
                FP += 1
        else:
            if prediction == 0.0:
                TP += 1
            else:
                FN += 1

    return TN, FP, FN, TP

### main program ###

def main():
    # load raw data
    datafile = 'dat/breast_cancer.csv'
    raw_data = get_data(datafile)

    # split the header from the values
    header = raw_data[0]
    data = raw_data[1:]

    # for this dataset, make sure all values are floats
    for i in range(len(data[0])):
        to_float(data, i)

    # create training and testing data
    training_data, testing_data = train_test_split(data, 0.4)

    # build decision tree with training data
    # parameter 1: training dataset
    # parameter 2: max depth
    # parameter 3: feature names
    my_tree = build_tree(training_data, 1, header)

    # view the tree structure
    #print_tree(my_tree)

    # print predictions
    #predict(testing_data, my_tree)

    # get the confusion matrix
    a, b, c, d = confusion_matrix(testing_data, my_tree)
    #print(asarray([[a, b],[c, d]]))

    # calculate accuracy
    accuracy = (a + d)/(a + b + c + d)*100.00
    print('Accuracy: %2.2f%%' % accuracy)

if __name__ == '__main__':
    main()