/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fol;

/**
 *
 * @author REEVESBRA
 */
public class Person {
    private double height;
    private double weight;
    private int normal;
    
    public Person(double height, double weight, int normal) {
        this.height = height;
        this.weight = weight;
        this.normal = normal;
    }
    
    public double getHeight() {
        return this.height;
    }
    
    public double getWeight() {
        return this.weight;
    }
    
    public int getNormal() {
        return this.normal;
    }
    
        public void setHeight(double height) {
        this.height = height;
    }
        
    public void setWeight(double weight) {
        this.weight = weight;
    }
    
    public void setNormal(int normal) {
        this.normal = normal;
    }
}
