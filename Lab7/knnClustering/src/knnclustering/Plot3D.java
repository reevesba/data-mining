/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package knnclustering;

import org.jzy3d.analysis.AbstractAnalysis;
import org.jzy3d.chart.factories.AWTChartComponentFactory;
import org.jzy3d.colors.Color;
import org.jzy3d.maths.Coord3d;
import org.jzy3d.plot3d.primitives.Scatter;
import org.jzy3d.plot3d.rendering.canvas.Quality;

/**
 *
 * @author REEVESBRA
 */
public class Plot3D extends AbstractAnalysis {

    private final Coord3d[] plotPoints;
    private final Color[] plotColors;
    
    public Plot3D(Coord3d[] points, Color[] colors){
        this.plotPoints = points;
        this.plotColors = colors;
    }
    
    @Override
    public void init() {
        Scatter scatter = new Scatter(this.plotPoints, this.plotColors, 5f);
        chart = AWTChartComponentFactory.chart(Quality.Advanced, "newt");
        chart.getScene().add(scatter);
    }
}
