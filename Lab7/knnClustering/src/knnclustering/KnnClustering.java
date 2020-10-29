/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package knnclustering;

import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

import org.jzy3d.analysis.AnalysisLauncher;
import org.jzy3d.colors.Color;
import org.jzy3d.maths.Coord3d;
import org.jzy3d.maths.Coord2d;

/**
 *
 * @author REEVESBRA
 */

public class KnnClustering {
    
    private static double[][] allDistances;
    
    private static final Color[] KELLY_COLORS = {
        // only 20 colors, may need to add more
        new Color(255, 179, 0),     //vivid yellow
        new Color(128, 62, 117),    //string purple
        new Color(255, 104, 0),     //vivid orange
        new Color(166, 189, 215),   //very light blue
        new Color(193, 0, 32),      //vivid red
        new Color(206, 162, 98),    //grayish yellow
        new Color(129, 112, 102),   //medium gray

        // these aren't good for people with defective color vision:
        new Color(0, 125, 52),      //vivid green
        new Color(246, 118, 142),   //strong purplish pink
        new Color(0, 83, 138),      //strong blue
        new Color(255, 122, 92),    //strong yellowish pink
        new Color(83, 55, 122),     //strong violet
        new Color(255, 142, 0),     //vivid orange yellow
        new Color(179, 40, 81),     //strong purplish red
        new Color(244, 200, 0),     //vivid greenish yellow
        new Color(127, 24, 13),     //strong reddish brown
        new Color(147, 170, 0),     //vivid yellowish green
        new Color(89, 51, 21),      //deep yellowish brown
        new Color(241, 58, 19),     //vivid reddish orange
        new Color(35, 44, 22)       //dark olive green
    };
    
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
    
    private static double[][] toDouble(String[][] arr){
        double[][] dataset = new double[arr.length][arr[0].length];
        
        for (int i = 0; i < arr.length; i++){
            for (int j = 0; j < arr[i].length; j++){
                dataset[i][j] = Double.parseDouble(arr[i][j]);
            }
        }
        return dataset;
    }
    
    private static void writeData(double[][] dataset) throws IOException{
        StringBuilder builder = new StringBuilder();
        
        for (double[] row : dataset) {
            for (int j = 0; j < row.length; j++) {
                builder.append(row[j]).append("");
                if (j < row.length - 1) {
                    builder.append(",");
                }
            }
            builder.append("\n");
        }
        
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("test/3dPoints.csv"))) {
            writer.write(builder.toString());
        }
    }
    
    private static void plot2d(double[][] dataset, Color[] colors) throws Exception {
        double x = 0, y = 0;
        
        Coord2d[] coords = new Coord2d[dataset.length];
        
        for(int i = 0; i < dataset.length; i++){
            for (int j = 0; j < 1; j++){
                x = dataset[i][j];
                y = dataset[i][j + 1];
            }
            coords[i] = new Coord2d(x, y);
        }
        AnalysisLauncher.open(new Plot2D(coords, colors));
    }
    
    private static void plot3d(double[][] dataset, Color[] colors) throws Exception {
        double x = 0, y = 0, z = 0;
        
        Coord3d[] coords = new Coord3d[dataset.length];
        
        for(int i = 0; i < dataset.length; i++){
            for (int j = 0; j < 1; j++){
                x = dataset[i][j];
                y = dataset[i][j + 1];
                z = dataset[i][j + 2];
            }
            coords[i] = new Coord3d(x, y, z);
        }
        AnalysisLauncher.open(new Plot3D(coords, colors));
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
    
    public static int randInt(int min, int max){
        return (int) ((Math.random()*(max - min)) + min);
    }
    
    public static double[] generate3dPoint(double meanX, double meanY, double meanZ, double devX, double devY, double devZ){
        Random r = new Random();
        double[] point = new double[3];
        point[0] = r.nextGaussian()*devX + meanX;
        point[1] = r.nextGaussian()*devY + meanY;
        point[2] = r.nextGaussian()*devZ + meanZ;
        return point;
    }
    
    public static double[][] generate3dPoints(int numSamples, int numFeatures){
        int clMeanX = 100, clMeanY = 100, clMeanZ = 100;
        int clDevX = 60, clDevY = 60, clDevZ = 60;
        int ptDevX = 7, ptDevY = 7, ptDevZ = 7;
        int numClusters = 5;
   
        double[][] centroids = new double[numClusters][numFeatures];
        for (int i = 0; i < centroids.length; i++){
            centroids[i] = generate3dPoint(clMeanX, clMeanY, clMeanZ, clDevX, clDevY, clDevZ);
        }
        
        double[][] dataset = new double[numSamples][numFeatures];
        double[] centroid;
        for (int i = 0; i < dataset.length; i++){
                centroid = centroids[randInt(0, numClusters)];
                dataset[i] = generate3dPoint(centroid[0], centroid[1], centroid[2], ptDevX, ptDevY, ptDevZ);
        }
        return dataset;
    }
    
    private static double[][] insertRow(double[][] dataset, double[] row){
        double[][] newDataset = new double[dataset.length + 1][row.length];
        
        for (int i = 0; i < newDataset.length - 1; i++){
            System.arraycopy(dataset[i], 0, newDataset[i], 0, newDataset[i].length);
        }
        newDataset[newDataset.length - 1] = row;

        return newDataset;
    }
    
    private static Color[] pushColor(Color[] colors, Color color){
        Color[] newArr = new Color[colors.length + 1];
        System.arraycopy(colors, 0, newArr, 0, colors.length);
        newArr[newArr.length - 1] = color;

        return newArr;
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
       
        for (double[] trainRow : train) {
            distance = minkowskiDistance(testRow, trainRow, p);
            list.add(push(trainRow, distance));
        }
        // convert to 2d array
        double[][] distances = new double[list.size()][];
        distances = list.toArray(distances);
        Arrays.sort(distances, (a, b) -> Double.compare(a[a.length - 1], b[b.length - 1]));

        KnnClustering.allDistances = distances;
        if (distances.length < k) k = distances.length;
        
        double[][] neighbors = new double[k][distances[0].length];
        for (int i = 0; i < k; i++){
            System.arraycopy(distances[i], 0, neighbors[i], 0, neighbors[i].length);
        }
        return neighbors;
    }
    
    private static boolean inCluster(double[] row, double[][] cluster){
        boolean inCluster = false;
        
        for (double[] clusterRow : cluster) {
            if (Arrays.equals(row, pop(clusterRow)) == true) {
                inCluster = true;
            }
        }
        return inCluster;
    }
    
    private static double[][] removeCluster(double[][] dataset, double[][] cluster){
        double[][] newDataset = new double[0][0];
        
        for (double[] row : dataset) {
            if (inCluster(row, cluster) == false) {
                newDataset = insertRow(newDataset, row);
            }
        }
        return newDataset;
    }
    
    private static KMeans kMeans(double[][] dataset, int k, int p, double scale){
        double[][] points = new double[0][0];
        Color[] colors = new Color[0];
        int numClusters = 0;
        
        while (dataset.length > 0){
            double[] centroid = dataset[randInt(0, dataset.length - 1)];
            double[][] neighbors = findNeighbors(dataset, centroid, k, p);

            double sumDistance = 0.0;
            for (double[] neighbor : neighbors) {
                sumDistance += neighbor[neighbor.length - 1];
            }
            double meanDistance = sumDistance/neighbors.length;

            double threshold = scale*meanDistance;

            // create cluster
            double[][] cluster = new double[0][0];
            for (double[] distance : KnnClustering.allDistances) {
                if (distance[distance.length - 1] <= threshold) {
                    cluster = insertRow(cluster, distance);
                }
            }
            
            for (double[] row : cluster) {
                points = insertRow(points, row);
                if (Arrays.equals(pop(row), centroid) == true){
                    // make centroid hot pink
                    colors = pushColor(colors, new Color(255, 105, 180));
                }
                colors = pushColor(colors, KELLY_COLORS[numClusters]);
            }
            
            numClusters++;
            KnnClustering.allDistances = null;
            dataset = removeCluster(dataset, cluster);
        }
        return new KMeans(points, colors, numClusters);
    }

    /**
     * @param args the command line arguments
     * @throws java.lang.Exception
     */
    public static void main(String[] args) throws Exception {
        //final int numSamples = 1000;
        final int numFeatures = 3;
        final int k = 50;           //100 works good for the 3d dataset, 60 for 2d
        final int p = 2;
        final double scale = 2.0;   //3.5 works good for the 2d dataset, 2.0 for 2d
        
        // create a new 3d dataset
        //double[][] dataset = generate3dPoints(numSamples, numFeatures);
        //writeData(dataset);
        
        //String[][] rawData = loadData("test/3dPoints.csv");
        String[][] rawData = loadData("test/Accelerometer-walk.csv");
        //String[][] rawData = loadData("test/2dPoints.csv");
        
        double[][] dataset = toDouble(rawData);
        
        // plot the initial dataset
        Color[] allBlack = new Color[dataset.length];
        for (int i = 0; i < allBlack.length; i++){
            allBlack[i] = new Color(0, 0, 0);
        }
        if (dataset[0].length == 3) plot3d(dataset, allBlack);
        if (dataset[0].length == 2) plot2d(dataset, allBlack);
        
        // perform kmeans clustering
        KMeans km = kMeans(dataset, k, p, scale);
        double[][] points = km.getPoints();
        Color[] colors = km.getColors();
        
        // plot the final groupings
        if (dataset[0].length == 3) plot3d(points, colors);
        if (dataset[0].length == 2) plot2d(dataset, colors);
        System.out.println(km.getNumClusters());        
    }
}
