/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package knnclustering;

import org.jzy3d.analysis.AbstractAnalysis;
import org.jzy3d.chart.factories.AWTChartComponentFactory;
import org.jzy3d.colors.Color;
import org.jzy3d.maths.Coord2d;
import org.jzy3d.plot2d.primitives.ScatterPointSerie2d;
import org.jzy3d.plot3d.rendering.canvas.Quality;

/**
 *
 * @author REEVESBRA
 */
public class Plot2D extends AbstractAnalysis {

    private final Coord2d[] points;
    private final Color[] colors;
    
    public Plot2D(Coord2d[] points, Color[] colors){
        this.points = points;
        this.colors = colors;
    }
    
    @Override
    public void init() {
        ScatterPointSerie2d scatter = new ScatterPointSerie2d("K Means Clustering");
        for (int i = 0; i < this.points.length; i++){
            scatter.add(this.points[i], this.colors[i]);
        }
        scatter.setWidth(4);
        
        chart = AWTChartComponentFactory.chart(Quality.Advanced, "newt");
        chart.getScene().add(scatter.getDrawable());
    }
}
