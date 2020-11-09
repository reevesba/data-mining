/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package fol;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author REEVESBRA
 */
public class Permutations {
    
    private static final List<List<Person>> PERMUTATIONS = new ArrayList<>();

    public static List<List<Person>> permutations(Person[] objects, int k) {
        getPermutations(objects, objects.length, k);
        return PERMUTATIONS;
    }

    private static void getPermutations(Person[] objects, int n, int k) {
        if (k == 0) {
            List<Person> permutation = new ArrayList<>();
            for (int i = n; i < objects.length; i++)
                permutation.add(objects[i]);
            PERMUTATIONS.add(permutation);
            return;
        }

        for (int i = 0; i < n; i++) {
            swap(objects, i, n - 1);
            getPermutations(objects, n - 1, k - 1);
            swap(objects, i, n - 1);
        }
    }  

    public static void swap(Person[] objects, int i, int j) {
        Person temp = objects[i];
        objects[i] = objects[j];
        objects[j] = temp;
    }
}
