/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package knnclustering;

import org.jzy3d.colors.Color;

/**
 *
 * @author REEVESBRA
 */
public class KMeans {
    private double[][] points;
    private Color[] colors;
    private int numClusters;
    
    public KMeans(double[][] points, Color[] colors, int numClusters){
        this.points = points;
        this.colors = colors;
        this.numClusters = numClusters;
    }
    
    public double[][] getPoints(){
        return this.points;
    }
    
    public Color[] getColors(){
        return this.colors;
    }
    
    public int getNumClusters(){
        return this.numClusters;
    }
    
    public void setPoints(double[][] points){
        this.points = points;
    }
    
    public void setColors(Color[] colors){
        this.colors = colors;
    }
    
    public void setNumClusters(int numClusters){
        this.numClusters = numClusters;
    }
}
