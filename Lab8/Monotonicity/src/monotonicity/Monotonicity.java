/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package monotonicity;

import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Random;

/**
 *
 * @author REEVESBRA
 */
public class Monotonicity {
    
    private static final int NOT_FOUND = -1;
    
    private static String[][] loadData(String fileName) throws FileNotFoundException, IOException {
        List<String[]> rows = new ArrayList<>();
        String row;
        
        FileInputStream csv = new FileInputStream(fileName);
        DataInputStream in = new DataInputStream(csv);
        
        while ((row = in.readLine()) != null)
            rows.add(row.split(","));
        
        String[][] dataset = new String[rows.size()][0];
        rows.toArray(dataset);
        
        return dataset;
    }
    
    private static void writeData(double[][] dataset, String filename) throws IOException {
        StringBuilder builder = new StringBuilder();
        
        for (double[] row : dataset) {
            for (int j = 0; j < row.length; j++) {
                builder.append(row[j]).append("");
                if (j < row.length - 1)
                    builder.append(",");
            }
            builder.append("\n");
        }
        
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("test/" + filename + ".csv"))) {
            writer.write(builder.toString());
        }
    }
    
    private static String[][] removeHeaders(String[][] arr) {
        String[][] dataset = new String[arr.length - 1][arr[0].length];
        
        for (int i = 0; i < arr.length - 1; i++)
            System.arraycopy(arr[i + 1], 0, dataset[i], 0, arr[i].length);
        
        return dataset;
    }
    
    private static double[][] toDouble(String[][] arr) {
        double[][] dataset = new double[arr.length][arr[0].length];
        
        for (int i = 0; i < arr.length; i++)
            for (int j = 0; j < arr[i].length; j++)
                dataset[i][j] = Double.parseDouble(arr[i][j]);

        return dataset;
    }
    
    public static int randInt(int min, int max) {
        //Random r = new Random(509);
        Random r = new Random();
        return r.nextInt(max - min) + min;
    }
    
    private static double[][] insertRow(double[][] train, double[][] test, int row) {
        double[][] newTest = new double[test.length][train[0].length];
        
        for (int i = 0; i < newTest.length - 1; i++)
            System.arraycopy(test[i], 0, newTest[i], 0, newTest[i].length);
        
        System.arraycopy(train[row], 0, newTest[test.length - 1], 0, train[row].length);

        return newTest;
    }
    
    private static double[][] deleteRow(double[][] train, int row) {
        double[][] newTrain = new double[train.length][train[0].length];
        
        for (int i = 0; i < newTrain.length; i++)
            for (int j = 0; j < newTrain[i].length; j++)
                if (i < row)
                    newTrain[i][j] = train[i][j];
                else if ((i + 1) < newTrain.length)
                    newTrain[i][j] = train[i + 1][j];
                    
        return newTrain;
    }
    
    private static List<double[][]> trainTestSplit(double[][] dataset, double split) {
        List<double[][]> list = new ArrayList<>();
        int trainSize = (int)(split*dataset.length);
        double[][] test = new double[0][dataset[0].length];
        double[][] train = new double[dataset.length][dataset[0].length];
        
        for (int i = 0; i < dataset.length; i++)
            System.arraycopy(dataset[i], 0, train[i], 0, dataset[i].length);
        
        while (test.length < trainSize) {
            int row = randInt(1, train.length);
            test = insertRow(train, Arrays.copyOf(test, test.length + 1), row);
            train = Arrays.copyOf(deleteRow(train, row), train.length - 1);
        }
        list.add(train);
        list.add(test);
        
        return list;
    }
    
    public static String formatAsTable(List<List<String>> rows) {
        int[] maxLengths = new int[rows.get(0).size()];
        rows.forEach((row) -> {
            for (int i = 0; i < row.size(); i++)
                maxLengths[i] = Math.max(maxLengths[i], row.get(i).length());
        });

        StringBuilder formatBuilder = new StringBuilder();
        for (int maxLength : maxLengths)
            formatBuilder.append("%-").append(maxLength + 2).append("s");
        
        String format = formatBuilder.toString();

        StringBuilder result = new StringBuilder();
        rows.forEach((row) -> {
            result.append(String.format(format, row.toArray(new String[0]))).append("\n");
        });
        return result.toString();
    }
    
    public static void printTable(Integer[][] dataset) {
        String[][] strDataset = new String[dataset.length][dataset[0].length];
        for (int i = 0; i < dataset.length; i++)
            for (int j = 0; j < dataset[i].length; j++)
                strDataset[i][j] = dataset[i][j] + "";
                
        List<String> header = new ArrayList<>();
        List<List<String>> table = new ArrayList<>();
        
        header.add("");
        for (int i = 0; i < strDataset[0].length; i++)
            header.add("A" + (i));
        table.add(header);
        
        for (int i = 0; i < strDataset.length; i++) {
            table.add(new ArrayList<>(Arrays.asList(strDataset[i])));
            table.get(i + 1).add(0, "A" + (i));
        }
        System.out.println(formatAsTable(table));
    }
    
    private static void printMetrics(double[] metrics) {
        String f = "%.2f";
        System.out.println("Accuracy: " + String.format(f , metrics[0]) + "%");
        System.out.println("Recall: " + String.format(f , metrics[1]) + "%");
        System.out.println("False Positive Rate: " + String.format(f , metrics[2]) + "%");
        System.out.println("True Negative Rate: " + String.format(f , metrics[3]) + "%");
        System.out.println("False Negative Rate: " + String.format(f , metrics[4]) + "%");
        System.out.println("Precision: " + String.format(f , metrics[5]) + "%");
    }
    
    private static double[] metrics(int[] matrix){
        double[] metrics = new double[6];
        double a = matrix[0], b = matrix[1], c = matrix[2], d = matrix[3];
        
        metrics[0] = (a + d)/(a + b + c + d)*100.00;   // acc
        metrics[1] = d/(c + d)*100.00;                 // recall
        metrics[2] = b/(a + b)*100.00;                 // FP rate
        metrics[3] = a/(a + b)*100.00;                 // TN rate
        metrics[4] = c/(c + d)*100.00;                 // FN rate
        metrics[5] = d/(b + d)*100.00;                 // precision
       
        return metrics;
    }
    
    private static int[] confusionMatrix(double[] targets, double[] predictions){
        int a = 0, b = 0, c = 0, d = 0;
        
        for (int i = 0; i < targets.length; i++)
            if (targets[i] == 0)
                if (predictions[i] == 0.0) a++;
                else b++;
            else
                if (predictions[i] == 0.0) c++;
                else d++;
            
        return new int[]{a, b, c, d};
    }
    
    private static void printMatrix(int[] matrix) {
        System.out.println("Confusion Matrix:");
        System.out.println(" _____________________________________________________");
        System.out.println("|                         |_________Predicted_________|");
        System.out.println("|_________________________|___Negative__|__Positive___|");
        System.out.println(String.format("| Actual |____Negative____|_____%3d_____|_____%3d_____|", matrix[0], matrix[1]));
        System.out.println(String.format("|________|____Positive____|_____%3d_____|_____%3d_____|\n", matrix[2], matrix[3]));
    }
    
    private static void printArray(double[] arr) {
        System.out.print("[");
        for (int i = 0; i < arr.length; i++)
            if (i < arr.length - 1) System.out.print(arr[i] + ", ");
            else System.out.println(arr[i] + "]");
    }
    
    private static void printArray(Integer[] arr) {
        System.out.print("[");
        for (int i = 0; i < arr.length; i++)
            if (i < arr.length - 1) System.out.print(arr[i] + ", ");
            else System.out.println(arr[i] + "]");
    }
    
    private static void printChains(List<List<Integer>> chains) {
        for (int i = 0; i < chains.size(); i++) {
            for (int j = 0; j < chains.get(i).size(); j++)
                if (j != chains.get(i).size() - 1)
                    System.out.print(chains.get(i).get(j) + " < ");
                else System.out.print(chains.get(i).get(j));
            System.out.println();
        }
    }
    
    private static double[] pop(double[] arr) {
        double[] newArr = new double[arr.length - 1];
        System.arraycopy(arr, 0, newArr, 0, arr.length - 1);
        return newArr;
    }
    
    private static double[] getTargets(double[][] test) {
        double[] targets = new double[test.length];
        
        for (int i = 0; i < targets.length; i++)
            targets[i] = test[i][test[i].length - 1];
        
        return targets;
    }
    
    public static int nextIndex(Integer[][] train, int index) {
        int nextValue = NOT_FOUND;
        
        for (int i = index; i < train.length; i++) {
            for (int j = index; j < train[i].length; j++) {
                if (train[i][j] != null && train[i][j] == -1) {
                    nextValue = j;
                    break;
                }
            }
            break;
        }
        return nextValue;
    }
    
    public static List<List<Integer>> filterChains(List<List<Integer>> chains, double[][] dataset) {
        List<List<Integer>> invalidChains = new ArrayList<>();
        
        for (int i = 0; i < chains.size(); i++) {
            // filter 1: remove chains that contain different classes
            double target = dataset[chains.get(i).get(0)][dataset[i].length - 1];
            for (int j = 1; j < chains.get(i).size(); j++)
                if (dataset[chains.get(i).get(j)][dataset[i].length - 1] != target)
                    invalidChains.add(chains.get(i));
            
            // filter 2: remove singular chains
            if (chains.get(i).size() == 1) invalidChains.add(chains.get(i));
        }
        
        chains.removeAll(invalidChains);
        return chains;
    }

    public static List<List<Integer>> getChains(Integer[][] train, double[][] dataset) {
        List<List<Integer>> chains = new ArrayList<>();
        for (int i = 0; i < train.length; i++) {
            chains.add(new ArrayList<>());
            chains.get(i).add(i);
            
            int index = i;
            int nextIndex = nextIndex(train, index);
            while (nextIndex != -1) {
                chains.get(i).add(nextIndex);
                index = nextIndex;
                nextIndex = nextIndex(train, index);
            }
        }
        return filterChains(chains, dataset);
    }
    
    public static Integer getRelation(double[] sample1, double[] sample2) {
        boolean increasing = true;
        boolean decreasing = true;
        boolean equal = true;
        
        for (int i = 0; i < sample1.length; i++)
            if (sample1[i] < sample2[i]) {
                decreasing = false;
                equal = false;
            }
            else if (sample1[i] > sample2[i]) {
                increasing = false;
                equal = false;
            }
            else if (sample1[i] == sample2[i]) {
                increasing = false;
                decreasing = false;
            }
            
        if (increasing == true) return -1;
        else if (decreasing == true) return 1;
        else if (equal == true) return 0;
        else return null;
    }
    
    public static Integer[][] getRelations(double[][] train, double[][] test) {
        Integer[][] R = new Integer[test.length][train.length];
                
        for (int i = 0; i < R.length; i++)
            for (int j = 0; j < R[i].length; j++)
                R[i][j] = getRelation(pop(test[i]), pop(train[j]));

        return R;
    }
    
    public static Integer[][] fit(double[][] train) {
        // create nxn matrix
        Integer[][] R = new Integer[train.length][train.length];
        
        for (int i = 0; i < R.length; i++)
            for (int j = 0; j < R[i].length; j++)
                R[i][j] = getRelation(pop(train[i]), pop(train[j]));
        
        return R;
    }
    
    private static double mostFrequent(double[] arr) {
        HashMap<Double, Integer> map = new HashMap<>();
        double mostFrequentValue = (double) NOT_FOUND;
        double mostOccurances = (double) NOT_FOUND;
        
        for (double value : arr)
            if (map.containsKey(value)){
                map.put(value, map.get(value) + 1);
                if (map.get(value) > mostOccurances){
                    mostFrequentValue = value;
                    mostOccurances = map.get(value);
                }
            } else map.put(value, 1);        
 
        return mostFrequentValue;
    }
    
    public static int getNextLT(Integer[] row, int index) {
        int nextLT = NOT_FOUND;
        
        for (int i = index; i < row.length; i++)
            if (row[i] != null && row[i] == 1) {
                nextLT = i;
                break;
            }
        return nextLT;
    }
    
    public static int getNextGT(Integer[] row, int index) {
        int nextGT = NOT_FOUND;
                
        for (int i = index; i < row.length; i++)
            if (row[i] != null && row[i] == -1) {
                nextGT = i;
                break;
            }
        return nextGT;
    }
    
    public static double vote(Integer[] row, double[][] train) {
        List<Double> list = new ArrayList<>();
        for (int i = 0; i < row.length; i++)
            if (row[i] != null) list.add(train[i][train[i].length - 1]);
        
        double[] targets = new double[list.size()];
        for (int i = 0; i < targets.length; i++)
            targets[i] = list.get(i);

        return mostFrequent(targets);
    }
    
    public static boolean foundMatch(int index, List<List<Integer>> chains) {
        boolean foundMatch = false;

        for (int i = 0; i < chains.size(); i++)
            if (chains.get(i).contains(index))
                foundMatch = true;
        
        return foundMatch;
    }
    
    public static double matchOne(Integer[] row, List<List<Integer>> chains, double[][] train) {
        // since there could be multiple matches in different chains
        // let's take a vote on most popular class
        List<Double> list = new ArrayList<>();
        
        for (int i = 0; i < row.length; i++)
            if (row[i] != null && foundMatch(i, chains))
                list.add(train[i][train[i].length - 1]);
        
        double[] matches = new double[list.size()];
        for (int i = 0; i < matches.length; i++)
            matches[i] = list.get(i);
        
        return mostFrequent(matches);
    }
    
    public static boolean foundTwoMatches(int nextLT, int nextGT, List<List<Integer>> chains) {
        boolean foundMatch = false;
        
        for (int i = 0; i < chains.size(); i++)
            if (chains.get(i).contains(nextLT) && chains.get(i).contains(nextGT))
                foundMatch = true;
            
        return foundMatch;
    }
    
    public static double matchTwo(Integer[] row, List<List<Integer>> chains, double[][] train) {
        double match = (double) NOT_FOUND; // no match
        int nextLT = getNextLT(row, 0), nextGT = NOT_FOUND;
        double targetLT, targetGT;

        outerLoop:
        while (nextLT != NOT_FOUND) {
            nextGT = getNextGT(row, 0);
            while (nextGT != NOT_FOUND)
                if (foundTwoMatches(nextLT, nextGT, chains)) break outerLoop;
                else nextGT = getNextGT(row, nextGT + 1);
            nextLT = getNextLT(row, nextLT + 1);
        }
        
        if (nextLT != NOT_FOUND && nextGT != NOT_FOUND) {
            targetLT = train[nextLT][train[nextLT].length - 1];
            targetGT = train[nextGT][train[nextGT].length - 1];
            if (targetLT == targetGT) match = targetLT;
        }
        return match;
    }
    
    public static double[] predict(Integer[][] relations, List<List<Integer>> chains, double[][] train) {
        double[] predictions = new double[relations.length];
        
        for (int i = 0; i < relations.length; i++)
            if (matchTwo(relations[i], chains, train) != (double) NOT_FOUND)
                // use a size 3 chain built with a value less than and
                // a value greater than the test sample
                predictions[i] = matchTwo(relations[i], chains, train);
            else if (matchOne(relations[i], chains, train) != (double) NOT_FOUND)
                // use a size 2 chain built with a value either less than
                // or a value greater than the test sample
                predictions[i] = matchOne(relations[i], chains, train);
            // none of the training chain values are monotonically 
            // increasing or decreasing from the test sample.
            // for this reason, take a vote between ALL train values that are
            // either monotonically increasing or decreasing from test sample
            else predictions[i] = vote(relations[i], train);
        return predictions;
    }

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        // assumption: data is presorted
        String fileName = "test/iris_presorted.csv";
        String[][] rawData = loadData(fileName);
        double[][] dataset = toDouble(removeHeaders(rawData));
        
        // get train and test sets as list
        List<double[][]> split1 = trainTestSplit(dataset, 0.30);
        double[][] train = split1.get(0);
        double[][] test = split1.get(1);
        
        // get validation data
        List<double[][]> split2 = trainTestSplit(train, 0.20);
        train = split2.get(0);
        double[][] validation = split2.get(1);
        
        writeData(train, "iris_train_data");
        //writeData(test, "iris_test_data");
        
        // build a table of relations
        Integer[][] R = fit(train);
        //printTable(trainTbl);
        
        // create monotone chains
        List<List<Integer>> monoChains = getChains(R, train);
        printChains(monoChains);
        
        // experimenting with validation data
        Integer[][] validationTbl = getRelations(train, validation);
        //printTable(testTbl);        
        
        double[] valTargets = getTargets(validation);
        double[] valPredictions = predict(validationTbl, monoChains, train);
        
        System.out.println("Validation Metrics");
        
        int[] valMatrix = confusionMatrix(valTargets, valPredictions);
        printMatrix(valMatrix);
        
        double[] valMetrics = metrics(valMatrix);
        printMetrics(valMetrics);
        
        // experimenting with test data
        Integer[][] testTbl = getRelations(train, test);
        //printTable(testTbl);        
        
        double[] testTargets = getTargets(test);
        double[] testPredictions = predict(testTbl, monoChains, train);
        
        System.out.println("\nTest Metrics");
        
        int[] testMatrix = confusionMatrix(testTargets, testPredictions);
        printMatrix(testMatrix);
        
        double[] testMetrics = metrics(testMatrix);
        printMetrics(testMetrics);
    }
}
