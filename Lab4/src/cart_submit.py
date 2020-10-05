# CART using SKLEARN

import pandas as pd
import graphviz
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn import metrics as m
from sklearn import tree
from numpy import asarray

def load_data(datafile):
    return pd.read_csv(datafile)

def plot_tree(my_tree, feature_names, class_names, splits):
    # DOT data
    dot_data = tree.export_graphviz(my_tree, out_file=None, 
                                feature_names=feature_names,  
                                class_names=class_names,
                                filled=True,
                                rounded=True)

    # draw graph
    graph = graphviz.Source(dot_data, format="png")
    graph.render("out/decision_tree_graphivz_" + splits)

def plot_matrix(my_tree, X_test, y_test, class_names, splits):
    title = "Confusion Matrix"
    disp = m.plot_confusion_matrix(my_tree, X_test, y_test, display_labels=class_names, cmap=plt.cm.Greys)
    disp.ax_.set_title(title)
    plt.savefig("out/" + title + "_" + splits + ".png")

def main():
    # file for saving output
    f = open("out/cart_results.txt", "w+")
    f.write("<---Decision Tree Results--->\n\n")
    f.close

    # load raw data
    my_file = 'dat/breast_cancer.csv'
    df = load_data(my_file)

    # use all features for prediction
    features = df.columns[:len(df.columns) - 1]

    X = df[features]
    y = df['target']

    # save the feature names for plotting
    feature_names = list(X.columns)
    class_names = [str(c) for c in y.unique()]

    # split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    ### using one splitting parameter ###
    f = open("out/cart_results.txt", "a+")
    f.write("One Splitting Parameter\n")

    n_split_nodes = 1
    max_leaf_nodes = n_split_nodes + 1

    my_tree = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)
    my_tree.fit(X_train, y_train)
    plot_tree(my_tree, feature_names, class_names, "1_split")

    y_pred = my_tree.predict(X_test)
    a, b, c, d = m.confusion_matrix(y_test, y_pred).ravel()
    plot_matrix(my_tree, X_test, y_test, class_names, "1_split")

    f.write("Confusion Matrix:\n")
    f.write(str(asarray([[a, b],[c, d]])) + "\n")
    
    AC = (a + d)/(a + b + c + d)*100.00
    f.write("Accuracy: %2.2f%%\n\n" % AC)

    ### using two splitting parameters ###
    f = open("out/cart_results.txt", "a+")
    f.write("Two Splitting Parameters\n")

    n_split_nodes = 2
    max_leaf_nodes = n_split_nodes + 1

    my_tree = tree.DecisionTreeClassifier(max_leaf_nodes=max_leaf_nodes)
    my_tree.fit(X_train, y_train)
    plot_tree(my_tree, feature_names, class_names, "2_split")

    y_pred = my_tree.predict(X_test)
    a, b, c, d = m.confusion_matrix(y_test, y_pred).ravel()
    plot_matrix(my_tree, X_test, y_test, class_names, "2_split")

    f.write("Confusion Matrix:\n")
    f.write(str(asarray([[a, b],[c, d]])) + "\n")

    AC = (a + d)/(a + b + c + d)*100.00
    f.write("Accuracy: %2.2f%%" % AC)

    f.close()

if __name__ == '__main__':
    main()