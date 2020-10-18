/*
 * Implement a method of k nearest neighbors (k-NN) with a confusion matrix
 * 2020/10/16
 */

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package knn;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 *
 * @author Bradley Reeves
 */
public class KNN {
    private static String[][] loadData(String fileName) throws FileNotFoundException, IOException{
        List<String[]> rows = new ArrayList<>();
        String row;
        
        FileInputStream csv = new FileInputStream(fileName);
        DataInputStream in = new DataInputStream(csv);
        
        while ((row = in.readLine()) != null){
            rows.add(row.split(","));
        }
        String[][] dataset = new String[rows.size()][0];
        rows.toArray(dataset);
        
        return dataset;
    }
    
    private static String[][] removeHeaders(String[][] arr){
        String[][] dataset = new String[arr.length - 1][arr[0].length];
        
        for (int i = 0; i < arr.length - 1; i++){
            System.arraycopy(arr[i + 1], 0, dataset[i], 0, arr[i].length);
        }
        return dataset;
    }
    
    private static double[][] toDouble(String[][] arr){
        double[][] dataset = new double[arr.length][arr[0].length];
        
        for (int i = 0; i < arr.length; i++){
            for (int j = 0; j < arr[i].length; j++){
                dataset[i][j] = Double.parseDouble(arr[i][j]);
            }
        }
        return dataset;
    }
    
    private static int randRange(int min, int max){
        Random random = new Random();
        return random.ints(min, max).findFirst().getAsInt();
    }
    
    private static double[][] insertRow(double[][] train, double[][] test, int row){
        double[][] newTest = new double[test.length][train[0].length];
        
        for (int i = 0; i < newTest.length - 1; i++){
            System.arraycopy(test[i], 0, newTest[i], 0, newTest[i].length);
        }
        System.arraycopy(train[row], 0, newTest[test.length - 1], 0, train[row].length);

        return newTest;
    }
    
    private static double[][] deleteRow(double[][] train, int row){
        double[][] newTrain = new double[train.length][train[0].length];
        
        for (int i = 0; i < newTrain.length; i++){
            for (int j = 0; j < newTrain[i].length; j++){
                if (i < row){
                    newTrain[i][j] = train[i][j];
                } else if ((i + 1) < newTrain.length) {
                    newTrain[i][j] = train[i + 1][j];
                }
            }
        }
        return newTrain;
    }
    
    private static void print2dArray(double [][] rows){
        System.out.print("[");
        for (int i = 0; i < rows.length; i++){
            System.out.print("[");
            for (int j = 0; j < rows[i].length; j++){
                System.out.print(String.valueOf(rows[i][j]));
                if (j != rows[i].length - 1){
                    System.out.print(", ");
                }
            }
            if (i == rows.length - 1){
                System.out.print("]");
            }
            System.out.print("]\n");
        }
    }
    
    private static void printMatrix(int[] matrix){
        System.out.println("Confusion Matrix:");
        System.out.println(" _____________________________________________________");
        System.out.println("|                         |_________Predicted_________|");
        System.out.println("|_________________________|___Negative__|__Positive___|");
        System.out.println(String.format("| Actual |____Negative____|_____%3d_____|_____%3d_____|", matrix[0], matrix[1]));
        System.out.println(String.format("|________|____Positive____|_____%3d_____|_____%3d_____|\n", matrix[2], matrix[3]));
    }
    
    private static List<double[][]> trainTestSplit(double[][] dataset, double split){
        List<double[][]> list = new ArrayList<>();
        int trainSize = (int)(split*dataset.length);
        double[][] test = new double[0][dataset[0].length];
        double[][] train = new double[dataset.length][dataset[0].length];
        
        for (int i = 0; i < dataset.length; i++){
            System.arraycopy(dataset[i], 0, train[i], 0, dataset[i].length);
        }
        while (test.length < trainSize){
            int row = randRange(1, train.length);
            test = insertRow(train, Arrays.copyOf(test, test.length + 1), row);
            train = Arrays.copyOf(deleteRow(train, row), train.length - 1);
        }
        list.add(train);
        list.add(test);
        
        return list;
    }
    
    private static double getAccuracy(int[] matrix){
        double correct = matrix[0] + matrix[3];
        double total = matrix[0] + matrix[1] + matrix[2] + matrix[3];
       
        return correct/total*100.00;
    }
    
    private static int[] confusionMatrix(int[] targets, int[] predictions){
        int a = 0, b = 0, c = 0, d = 0;
        
        for (int i = 0; i < targets.length; i++){
            if (targets[i] == 0){
                if (predictions[i] == 0){
                    a++;
                } else {
                    b++;
                }
            } else {
                if (predictions[i] == 0){
                    c++;
                } else {
                    d++;
                }
            }
        }
        return new int[]{a, b, c, d};
    }
    
    private static double[] push(double[] arr, double value){
        double[] newArr = new double[arr.length + 1];
        System.arraycopy(arr, 0, newArr, 0, arr.length);
        newArr[newArr.length - 1] = value;
    
        return newArr;
    }
    
    private static double[] pop(double[] arr){
        double[] newArr = new double[arr.length - 1];
        System.arraycopy(arr, 0, newArr, 0, arr.length - 1);
        
        return newArr;
    }
    
    private static double minkowskiDistance(double[] row1, double[] row2, int p){
        /*
         * p = 1: manhattan
         * p = 2: euclidean
         * p = inf: chebyshev
         */
        double distance = 0.0;
        
        for (int i = 0; i < row1.length; i++){
            distance += Math.pow(Math.abs(row1[i] - row2[i]), p);
        }
        return Math.pow(distance, 1.0/p);
    }
   
    private static double[][] findNeighbors(double[][] train, double[] testRow, int k, int p){
        List<double[]> list = new ArrayList<>();
        double distance;
       
        for (double[] train1 : train) {
            distance = minkowskiDistance(testRow, train1, p);
            list.add(push(train1, distance));
        }
        // convert to 2d array
        double[][] distances = new double[list.size()][];
        distances = list.toArray(distances);
                
        Arrays.sort(distances, (a, b) -> Double.compare(a[a.length - 1], b[b.length - 1]));
                
        for (int i = 0; i < distances.length; i++){
            distances[i] = pop(distances[i]);
        }
        // return k-NN
        double[][] neighbors = new double[k][distances[0].length];
        for (int i = 0; i < k; i++){
            System.arraycopy(distances[i], 0, neighbors[i], 0, neighbors[i].length);
        }
        return neighbors;
    }
    
    private static int mostFrequent(int[] arr){
        HashMap<Integer, Integer> map = new HashMap<>();
        int mostFrequentValue = 0;
        int mostOccurances = 0;
        
        for (int value : arr){
            if (map.containsKey(value)){
                map.put(value, map.get(value) + 1);
                if (map.get(value) > mostOccurances){
                    mostFrequentValue = value;
                    mostOccurances = map.get(value);
                }
            } else {
                map.put(value, 1);
            }
        }
        return mostFrequentValue;
    }
        
    private static int predict(double[][] train, double[] testRow, int k, int p){
        double[][] neighbors = findNeighbors(train, testRow, k, p);        
        int[] classes = new int[k];
        
        for (int i = 0; i < neighbors.length; i++){
            classes[i] = (int)neighbors[i][neighbors[i].length - 1];
        }
        return mostFrequent(classes);
    }
    
    private static int[] knn(double[][] train, double[][] test, int k, int p){
        int[] predictions = new int[test.length];

        for (int i = 0; i < predictions.length; i++){
            predictions[i] = predict(train, test[i], k, p);
        }
        return predictions;
    }
    
    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        String fileName = "test/breast_cancer.csv";
        String[][] rawData = loadData(fileName);
        rawData = removeHeaders(rawData);
        
        double[][] dataset = toDouble(rawData);
        
        // get train and test sets as list
        List<double[][]> list = trainTestSplit(dataset, 0.20);
        double[][] train = list.get(0);
        double[][] test = list.get(1);
                
        int k = 5;
        int p = 2;      // 1: manhattan distance 2: euclidean distance
        
        int[] predictions = knn(train, test, k, p);
        int[] targets = new int[test.length];
        
        for (int i = 0; i < targets.length; i++){
            targets[i] = (int) test[i][test[i].length - 1];
        }
                
        int[] matrix = confusionMatrix(targets, predictions);
        printMatrix(matrix);
        
        double accuracy = getAccuracy(matrix);
        System.out.println("Accuracy: " + String.format("%.2f" , accuracy) + "%");
    }
}
