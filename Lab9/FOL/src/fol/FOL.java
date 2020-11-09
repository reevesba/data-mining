/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fol;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import static fol.Permutations.permutations;

/**
 *
 * @author REEVESBRA
 */
public class FOL {
    
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
    
    private static void printMetrics(double[] metrics) {
        String f = "%.2f";
        System.out.println("Accuracy: " + String.format(f , metrics[0]) + "%");
        System.out.println("Recall: " + String.format(f , metrics[1]) + "%");
        System.out.println("False Positive Rate: " + String.format(f , metrics[2]) + "%");
        System.out.println("True Negative Rate: " + String.format(f , metrics[3]) + "%");
        System.out.println("False Negative Rate: " + String.format(f , metrics[4]) + "%");
        System.out.println("Precision: " + String.format(f , metrics[5]) + "%");
    }
    
    private static double[] metrics(int[] matrix) {
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
    
    private static void printMatrix(int[] matrix) {
        System.out.println("Confusion Matrix:");
        System.out.println(" _______________________________________________________");
        System.out.println("|                         |__________Predicted__________|");
        System.out.println("|_________________________|___Negative___|___Positive___|");
        System.out.println(String.format("| Actual |____Negative____|_____%4d_____|_____%4d_____|", matrix[0], matrix[1]));
        System.out.println(String.format("|________|____Positive____|_____%4d_____|_____%4d_____|\n", matrix[2], matrix[3]));
    }
    
    private static int[] confusionMatrix(int[] targets, int[] predictions) {
        int a = 0, b = 0, c = 0, d = 0;
        
        for (int i = 0; i < targets.length; i++)
            if (targets[i] == 0)
                if (predictions[i] == 0) a++;
                else b++;
            else
                if (predictions[i] == 0) c++;
                else d++;
            
        return new int[]{a, b, c, d};
    }
    
    private static double[][] sample(double[][] dataset, int n) {
        double[][] samples = new double[n][dataset[0].length];
        
        // step one: shuffle the dataset
        List<double[]> list = Arrays.asList(dataset);
        Collections.shuffle(list);
        dataset = list.toArray(new double[0][0]);
        
        // step two: assign values to sample array
        for (int i = 0; i < samples.length; i++)
            System.arraycopy(dataset[i], 0, samples[i], 0, samples[i].length);
        
        return samples;
    }
    
    private static int computeR(Person x, Person y, Person z) {
        // R(x, y, z) = (N(x) & N(z) & N(y))
        boolean isNormal = x.getNormal() == 1 && y.getNormal() == 1 && z.getNormal() == 1;
        
        if (isNormal) return 1;
        else return 0;
    }
    
    private static int computeA2(Person x, Person y, Person z) {
        // A(x, y, z) = (H(x, y) & H(y, z) & W(x, y) & W(y, z)
        boolean height = (x.getHeight() >= y.getHeight()) && (y.getHeight() >= z.getHeight());
        boolean weight = (x.getWeight() >= y.getWeight()) && (y.getWeight() >= z.getWeight());
        
        if (height && weight) return 1;
        else return 0; 
    }
    
    private static int computeA1(Person x, Person y, Person z) {
        // A(x, y, z) = (H(x)>H(y)>H(z)) & (W(x)>W(y)>W(z))
        boolean height = (x.getHeight() > y.getHeight() && y.getHeight() > z.getHeight());
        boolean weight = (x.getWeight() > y.getWeight() && y.getWeight() > z.getWeight());
        
        if (height && weight) return 1;
        else return 0;     
    }
    
    private static List<int[]> execFOL(List<List<Person>> objects, int form) {
        List<int[]> results = new ArrayList<>();
        int[] As = new int[objects.size()];
        int[] Rs = new int[objects.size()];
        
        for (int i = 0; i < objects.size(); i++) {
            Person x = objects.get(i).get(0);
            Person y = objects.get(i).get(1);
            Person z = objects.get(i).get(2);
            
            switch (form) {
                case 1:
                    As[i] = computeA1(x, y, z);
                    break;
                case 2:
                    As[i] = computeA2(x, y, z);
                    break;
                default:
                    System.out.println("Invalid Form Number");
                    break;
            }
            Rs[i] = computeR(x, y, z);
        }
        
        results.add(As);
        results.add(Rs);
        return results;
    }

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        String fileName = "data/weight-height.csv";
        String[][] rawData = loadData(fileName);
        double[][] dataset = toDouble(removeHeaders(rawData));
        
        int N = dataset.length;
        
        // get random samples if not whole dataset
        if (N != dataset.length) dataset = sample(dataset, N);
        
        // create Person objects
        Person[] objects = new Person[N];
        for (int i = 0; i < dataset.length; i++)
            objects[i] = new Person(dataset[i][0], dataset[i][1], (int) dataset[i][2]);
        
        // get all permutations
        List<List<Person>> permutations = permutations(objects, 3);
                
        // compute results
        List <int[]> results;
        int[] matrix;
        
        System.out.println("Testing first FOL form...");
        results = execFOL(permutations, 1);
        matrix = confusionMatrix(results.get(1), results.get(0));
        printMatrix(matrix);
        printMetrics(metrics(matrix));
        
        System.out.println("\nTesting second FOL form...");
        results = execFOL(permutations, 2);
        matrix = confusionMatrix(results.get(1), results.get(0));
        printMatrix(matrix);
        printMetrics(metrics(matrix));
    }
}
