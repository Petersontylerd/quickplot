
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

import sklearn.metrics as metrics
import sklearn.preprocessing as prepocessing

from statsmodels.stats.weightstats import ztest
from statsmodels.stats.proportion import proportions_ztest
from scipy import stats

import prettierplot.style as style
import prettierplot.util as util

class PrettierPlot():
    """
    Documentation:
        Description:
            PrettierPlot is a class that contain methods for creating data visualization.
            Initialization of this class creates a plotting object of a chosen size and
            orientation. Once the figure is initialized, the method makeCanvas is called
            to create the figure axis or chosen number of axes. If multiple axes are 
            specified, then multiple axes can be plotted on a single figure, or the 
            position variable can be utilized to create a subplot arrangement.        
    """        
    # Foundation
    def __init__(self, fig = plt.figure(), chartProp = 15, plotOrientation = None):
        """
        Documentation:
            Description: 
                Initialize PrettierPlot, create figure and determine chart proportions, orientation.        
            Parameters:
                fig : figure object, default = plt.figure()
                    matplotlib.pyplot figure object is a top level container for all plot elements.
                chartProp : float or int, default = 15
                    Chart proportionality control. Determines relative size of figure size, axis labels, 
                    chart title, tick labels, tick marks.
                orientation : string, default = None
                    Default value produces a plot that is wider than it is tall. Specifying 'tall' will 
                    produce a taller, less wide plot. 'square' produces a square plot. 'wide' produces a
                    plot that is much wide than it is tall.
        """
        self.chartProp = chartProp
        self.plotOrientation = plotOrientation
        self.fig = fig
        
        # Dynamically set chart width and height parameters.
        if plotOrientation == 'tall':
            chartWidth = self.chartProp * .7
            chartHeight = self.chartProp * .8
        elif plotOrientation == 'square':
            chartWidth = self.chartProp
            chartHeight = self.chartProp * .8
        elif plotOrientation == 'wide':
            chartWidth = self.chartProp * 1.7
            chartHeight = self.chartProp * .32
        else:            
            chartWidth = self.chartProp
            chartHeight = self.chartProp * .5
        self.fig.set_figheight(chartHeight)
        self.fig.set_figwidth(chartWidth)

    def makeCanvas(self, title = '', xLabel = '', yLabel = '', yShift = 0.8, position = 111):
        """
        Documentation:
            Description: 
                Create Axes object. Add descriptive attributes such as titles and axis labels,
                set font size and font color. Remove grid. Remove top and right spine. 
            Parameters:
                title : string, default = '' (blank)
                    The title for the chart.
                xLabel : string, default = '' (blank)
                    x-axis label.
                yLabel : string, default = '' (blank)
                    y-axis label.
                yShift : float, default = 0.8
                    Controls position of y-axis label. Higher values move label higher along axis. 
                    Intent is to align with top of axis.
                position int (nrows, ncols, index) : default = 111
                    Determine subplot position of plot.

            Returns 
                ax : Axes object
                    Contain figure elements
        """        
        ax = self.fig.add_subplot(position)
        
        # Add title.
        if len(title) >= 45:
            fontAdjust = 1.0
        elif len(title) >= 30 and len(title) < 45:
            fontAdjust = 1.25
        elif len(title) >= 20 and len(title) < 30:
            fontAdjust = 1.5
        else:
            fontAdjust = 1.75

        ax.set_title(title
                    ,fontsize = 2.0 * self.chartProp if position == 111 else fontAdjust * self.chartProp
                    ,color = style.styleGrey
                    ,loc = 'left'
                    ,pad = 0.4 * self.chartProp)
        
        # Remove grid line and right/top spines.
        ax.grid(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Add axis labels.
        plt.xlabel(xLabel, fontsize = 1.667 * self.chartProp, labelpad = 1.667 * self.chartProp, position = (0.5, 0.5))
        plt.ylabel(yLabel, fontsize = 1.667 * self.chartProp, labelpad = 1.667 * self.chartProp, position = (1.0, yShift))
        return ax

    # Standard visualization, matplotlib
    def pretty2dScatter(self, x, y, df = None, xUnits = 'f', yUnits = 'f', plotBuffer = True, size = 10
                    , axisLimits = True, color = style.styleGrey, facecolor = 'w', ax = None):
        """
        Documentation:
            Description: 
                Create 2-dimensional scatter plot.
            Parameters:
                x : array or string
                    Either 1-dimensional array of values or a column name in a Pandas DataFrame.
                y : array or string
                    Either 1-dimensional array of values or a column name in a Pandas DataFrame.
                df : Pandas DataFrame, default = None
                    Dataset containing data to be plotted. Can be any size - plotted columns will be 
                    chosen by columns names specified in x, y. 
                xUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                plotBuffer : boolean, default = True
                    Switch for determining whether dynamic plot buffer function is executed.
                size : int or float, default = 10
                    Determines scatter dot size
                axisLimits : boolean, default = True
                    Switch for determining whether dynamic axis limit setting function is executed.
                color : string (color code of some sort), default = style.styleGrey
                    Determine color of scatter dots
                facecolor : string (color code of some sort), default = 'w'
                    Determine face color of scatter dots
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # If a Pandas DataFrame is passed to function, create x, y arrays using columns names passed into function.
        if df is not None:
            x = df[x].values.reshape(-1,1)
            y = df[y].values.reshape(-1,1)
        # Else reshape arrays.
        else:
            x = x.reshape(-1,1)
            y = y.reshape(-1,1)
        
        # Plot 2-d scatter.
        plt.scatter(x = x
                    ,y = y
                    ,color = color
                    ,s = size * self.chartProp
                    ,alpha = 0.7
                    ,facecolor = facecolor
                    ,linewidth = 0.167 * self.chartProp
                   )
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)        
    
        # Dynamically set axis lower / upper limits.
        if axisLimits:
            xMin, xMax, yMin, yMax = util.utilSetAxes(x = x, y = y)        
            plt.axis([xMin, xMax, yMin, yMax])   

        # Create smaller buffer around plot area to prevent cutting off elements.
        if plotBuffer:
            util.utilPlotBuffer(ax = ax, x = 0.02, y = 0.02)

        # Show figure with tight layout.
        plt.tight_layout()
    
    def pretty2dScatterHue(self, x, y, target, label, df = None, xUnits = 'd', yUnits = 'd', plotBuffer = True
                        , size = 10, axisLimits = True, color = style.styleGrey, facecolor = 'w'
                        , bbox = (1.2, 0.9), ax = None):
        """
        Documentation:
            Description: 
                Create 2-dimensional scatter plot with a third dimension represented as a color hue in the
                scatter dots.
            Parameters:
                x : array or string
                    Either 1-dimensional array of values or a column name in a Pandas DataFrame.
                y : array or string
                    Either 1-dimensional array of values or a column name in a Pandas DataFrame.
                target : array or string
                    Either 1-dimensional array of values or a column name in a Pandas DataFrame.
                label : list
                    List of labels describing hue.
                df : Pandas DataFrame, default = None
                    Dataset containing data to be plotted. Can be any size - plotted columns will be 
                    chosen by columns names specified in x, y. 
                xUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                plotBuffer : boolean, default = True
                    Switch for determining whether dynamic plot buffer function is executed.
                size : int or float, default = 10
                    Determines scatter dot size
                axisLimits : boolean, default = True
                    Switch for determining whether dynamic axis limit setting function is executed.
                color : string (color code of some sort), default = style.styleGrey
                    Determine color of scatter dots
                facecolor : string (color code of some sort), default = 'w'
                    Determine face color of scatter dots
                bbox : tuple of floats, default = (1.2, 0.9)
                    Coordinates for determining legend position
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # If a Pandas DataFrame is passed to function, create x, y and target arrays using columns names 
        # passed into function. Also create X, which is a matrix containing the x, y and target columns.
        if df is not None:
            X = df[[x, y, target]].values
            x = df[x].values
            y = df[y].values
            target = df[target].values
        # Concatenate the x, y and target arrays.
        else:
            X = np.c_[x, y, target]

        # Unique target values.
        targetIds =  np.unique(X[:, 2])
            
        # Loop through sets of target values, labels and colors to create 2-d scatter with hue.
        for targetId, targetName, color in zip(targetIds, label, style.styleHexMid[:len(targetIds)]):
            plt.scatter(x = X[X[:,2] == targetId][:,0]
                        ,y = X[X[:,2] == targetId][:,1]
                        ,color = color
                        ,label = targetName
                        ,s = size * self.chartProp
                        ,alpha = 0.7
                        ,facecolor = 'w'
                        ,linewidth = 0.234 * self.chartProp
                    )
        
        # Add legend to figure.
        if label is not None:
            plt.legend(loc = 'upper right'
                       ,bbox_to_anchor = bbox
                       ,ncol = 1
                       ,frameon = True
                       ,fontsize = 1.1 * self.chartProp
                      )
            
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)

        # Dynamically set axis lower / upper limits.
        if axisLimits:
            xMin, xMax, yMin, yMax = util.utilSetAxes(x = x, y = y)
            plt.axis([xMin, xMax, yMin, yMax])   
        
        # Create smaller buffer around plot area to prevent cutting off elements.
        if plotBuffer:
            util.utilPlotBuffer(ax = ax, x = 0.02, y = 0.02)

        # Show figure with tight layout.
        plt.tight_layout()

    def prettyLine(self, x, y, label = None, df = None, linecolor = None, linestyle = None
                , bbox = (1.2, 0.9), yMultiVal = False, xUnits = 'f', yUnits = 'f', markerOn = False
                , plotBuffer = False, axisLimits = False, ax = None):
        """
        Documentation:
            Description: 
                Create line plot. Capable of plotting multile lines on the same figure. Also capable of
                adjusting which axis will have the same data for each line and which will have different
                data for each line.
            Parameters:
                x : array or string
                    Either 1-dimensional array of values, a multidimensional array of values, a list of columns 
                    in a Pandas DataFrame, or a column name in a Pandas DataFrame.
                y : array or string
                    Either 1-dimensional array of values, a multidimensional array of values, a list of columns 
                    in a Pandas DataFrame, or a column name in a Pandas DataFrame.
                label : list of strings : default = None
                    List of names of used to create legend entries for each line.
                df : Pandas DataFrame, default = None
                    Dataset containing data to be plotted. Can be any size, as plotted columns will be chosen 
                    by columns names specified in x, y. 
                linecolor : string, default = reference to list
                    Determine color of line.
                linestyle : string, default = reference to list
                    Determine style of line.
                bbox : tuple, default = (1.2, 0.9)
                    Override bbox value for legend
                yMultiVal : boolean : default = False
                    If a single x value is paired with multiple y values, set to True.
                xUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                markerOn : boolean, default = False
                    Determines whether to show line with markers at each element.
                plotBuffer : boolean, default = False
                    Switch for determining whether dynamic plot buffer function is executed.
                axisLimits : boolean, default = False
                    Switch for determining whether dynamic axis limit setting function is executed.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within `function.
        """
        # If a Pandas DataFrame is passed to function, create x, y arrays using columns names passed into function.
        if df is not None:
            x = df[x].values
            y = df[y].values
        else:
            x = x.reshape(-1,1) if len(x.shape) == 1 else x
            y = y.reshape(-1,1) if len(y.shape) == 1 else y
        
        # Add line 
        if not yMultiVal:
            for ix in np.arange(x.shape[1]):
                xCol = x[:, ix]
                plt.plot(xCol
                         ,y
                         ,color = linecolor if linecolor is not None else style.styleHexMid[ix]
                         ,linestyle = linestyle if linestyle is not None else style.styleLineStyle[0]
                         ,linewidth = 0.247 * self.chartProp
                         ,label = label[ix] if label is not None else None
                         ,marker = '.' if markerOn else None
                         ,markersize = 25 if markerOn else None
                         ,markerfacecolor = 'w' if markerOn else None
                         ,markeredgewidth = 2.5 if markerOn else None
                        )                
        else:
            for ix in np.arange(y.shape[1]):
                yCol = y[:, ix]
                plt.plot(x
                         ,yCol
                         ,color = linecolor if linecolor is not None else style.styleHexMid[ix]
                         ,linestyle = linestyle if linestyle is not None else style.styleLineStyle[0]
                         ,linewidth = 0.247 * self.chartProp
                         ,label = label[ix] if label is not None else None
                         ,marker = '.' if markerOn else None
                         ,markersize = 25 if markerOn else None
                         ,markerfacecolor = 'w' if markerOn else None
                         ,markeredgewidth = 2.5 if markerOn else None
                        )

        # Add legend to figure
        if label is not None:
            plt.legend(loc = 'upper right'
                       ,bbox_to_anchor = bbox
                       ,ncol = 1
                       ,frameon = True
                       ,fontsize = 1.1 * self.chartProp
                      )
            
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)

        # Dynamically set axis lower / upper limits
        if axisLimits:
            xMin, xMax, yMin, yMax = util.utilSetAxes(x = x, y = y)
            plt.axis([xMin, xMax, yMin, yMax])   
        
        # Create smaller buffer around plot area to prevent cutting off elements.
        if plotBuffer:
            util.utilPlotBuffer(ax = ax, x = 0.02, y = 0.02)

        # Show figure with tight layout.
        plt.tight_layout()    
    
    def prettyBarV(self, x, counts, color = style.styleHexMid[0], xLabels = None, labelRotate = 0, yUnits = 'f', ax = None):
        """
        Documentation:
            Description: 
                Create vertical bar plot.
            Parameters:
                x : array
                    1-dimensional array of values to be plotted on x-axis representing distinct categories.
                counts : array or string
                    1-dimensional array of value counts for categories.
                color : string (some sort of color code), default = style.styleHexMid[0]
                    Bar color.
                xLabels : list, default = None
                    Custom x-axis test labels
                labelRotate : float or int, default = 0
                    Degrees by which the xtick labels are rotated.
                yUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # Create vertical bar plot.
        plt.bar(x = x
                ,height = counts
                ,color = color
                # ,tick_label = x
                ,tick_label = xLabels if xLabels is not None else x
                ,alpha = 0.8
            )

        # Rotate x-tick labels.
        plt.xticks(rotation = labelRotate)
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, yUnits = yUnits)

        # Resize x-axis labels as needed
        if len(x) > 10 and len(x) <= 20:
            ax.tick_params(axis = 'x', colors = style.styleGrey, labelsize = 1.2 * self.chartProp)
        elif len(x) > 20:
            ax.tick_params(axis = 'x', colors = style.styleGrey, labelsize = 0.6 * self.chartProp)
        
    def prettyBarH(self, y, counts, color = style.styleHexMid[0], labelRotate = 45, xUnits = 'f', ax = None):
        """
        Documentation:
            Description: 
                Create vertical bar plot.
            Parameters:
                y : array
                    1-dimensional array of values to be plotted on x-axis representing distinct categories.
                counts : array or string
                    1-dimensional array of value counts for categories.
                color : string (some sort of color code), default = style.styleHexMid[0]
                    Bar color.
                labelRotate : float or int, default = 45
                    Degrees by which the xtick labels are rotated.
                xUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within `function.
        """
        # Plot horizontal bar plot.
        plt.barh(y = y
                ,width = counts
                ,color = color
                ,tick_label = y
                ,alpha = 0.8
            )
        
        # Rotate x-tick labels.
        plt.xticks(rotation = labelRotate)
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits)

    def prettyFacetNum(self, x, color, label, alpha = 0.8):
        """
        Documentation:
            Description:
                Create histogram of continuous variable. Simple function capable of easy
                iteration through several groupings of a continuous variable that is 
                separated out based on a categorical label. This results in several overlapping
                histograms and can reveal differences in distributions.
            Parameters:
                x : array
                    1-dimensional array of values to be plotted on x-axis.
                color : string (some sort of color code)
                    Determines color of histogram
                label : string
                    Category value label
                alpha : float, default = 0.8
                    Fades histogram bars to create transparent bars            
        """
        # Create histogram.
        plt.hist(x = x
                ,color = color
                ,label = label
                ,alpha = alpha
                )
            
    def prettyFacetCat(self, df, feature, labelRotate = 0, yUnits = 'f', xUnits = 's', bbox = (1.2, 0.9), ax = None):       
        """
        Documentation:
            Description:
                Creates a count plot of a categorical feature and facets that feature by a categorical label.
            Parameters:
                df : Pandas DataFrame
                    Pandas DataFrame
                feature : string
                    String describing column name containing target values
                labelRotate : float or int, default = 45
                    Degrees by which the xtick labels are rotated.
                xUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'd'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                bbox : tuple of floats, default = (1.2, 0.9)
                    Coordinates for determining legend position
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        ixs = np.arange(df.shape[0])
        bar_width = 0.35
        
        featureDict = {}
        for feature in df.columns[1:]:
            featureDict[feature] = df[feature].values.tolist()
        for featureIx, (k, v) in enumerate(featureDict.items()):
            plt.bar(ixs + (bar_width * featureIx)
                    ,featureDict[k]
                    ,bar_width
                    ,alpha = 0.75
                    ,color = style.styleHexMid[featureIx]
                    ,label = str(k)
                    )
        
        # Custom x-tick labels.
        plt.xticks(ixs[:df.shape[0]] + bar_width / 2, df.iloc[:,0].values)
        
        # Rotate x-tick labels.
        plt.xticks(rotation = labelRotate)
                
        # Add legend to figure.
        plt.legend(loc = 'upper right'
                    ,bbox_to_anchor = bbox
                    ,ncol = 1
                    ,frameon = True
                    ,fontsize = 1.1 * self.chartProp
                    )
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)
        
        # Resize x-axis labels as needed.
        if len(featureDict[feature]) > 10 and len(featureDict[feature]) <= 20:
            ax.tick_params(axis = 'x', colors = style.styleGrey, labelsize = 1.2 * self.chartProp)
            
        elif len(featureDict[feature]) > 20:
            ax.tick_params(axis = 'x', colors = style.styleGrey, labelsize = 0.6 * self.chartProp)

    def prettyProbPlot(self, x, plot):
        """
        Documentation:
            Description:
                Create plot that visualizes how well a continuous feature's distribution
                conforms to a normal distribution
            Parameters:
                x : array
                    1-dimensional array containing data of a continuous feature
                plot : plot object
                    Plotting object for applying additional formatting.
        """
        stats.probplot(x, plot = plot)
        
        # Override title and axis labels.
        plot.set_title('')
        plt.xlabel('')
        plt.ylabel('')
        
        # Format scatter dots.
        plot.get_lines()[0].set_markerfacecolor(style.styleWhite)
        plot.get_lines()[0].set_color(style.styleHexMid[2])
        plot.get_lines()[0].set_markersize(5.0)

        # Format line representing normality.
        plot.get_lines()[1].set_linewidth(3.0)
        plot.get_lines()[1].set_color(style.styleGrey)
    
    # Standard visualization, seaborn
    def prettyDist(self, x, color, yUnits = 'f', xUnits = 'f', fit = None, xRotate = None, ax = None):
        """
        Documentation:
            Description:
                Creates distribution plot for continuous variables, showing counts of a single
                variable. Also overlays a kernel density estimation curve.
            Parameters:
                x : array
                    Data to be plotted.
                color : string (some sort of color code)
                    Determines color of bars, KDE lines.
                xUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                xRotate : boolean, default = None
                    Rotates x-axis tick mark labels 45 degrees
                fit : random variabe object, default = None
                    Allows for the addition of another curve. Utilizing 'norm' overlays a normal distribution
                    over the distribution bar chart. Useful for seeing how well, or not, distribution tracks
                    with a normal distrbution.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        g = sns.distplot(a = x
                        ,kde = True
                        ,color = color
                        ,axlabel = False
                        ,fit = fit
                        ,ax = ax)

        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits, xRotate = xRotate)
        
    def prettyKde(self, x, color, yUnits = 'f', xUnits = 'f', ax = None):
        """
        Documentation:
            Description:
                Create kernel density curve for a feature.
            Parameters:
                x : array
                    Data to be plotted.
                color : string (some sort of color code)
                    Determines color of KDE lines.
                xUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                yUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # Create kernel density estimation line
        g = sns.kdeplot(data = x
                        ,shade = True
                        ,color = color
                        ,legend = None
                        ,ax = ax)
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)

    def prettyBoxPlotV(self, x, y, data, color, labelRotate = 0, yUnits = 'f', ax = None):
        """
        Documentation:
            Description:
                Create vertical box plots. Useful for evaluated a continuous target on the y-axis
                vs. several different category segments on the x-axis
            Parameters:
                x : string
                    Name of independent variable in dataframe. Represents a category
                y : string
                    Name of continuous target variable. 
                data : Pandas DataFrame
                    Pandas DataFrame including both indpedent variable and target variable.
                color : string
                    Determines color of box plot figures. Ideally this object is a color palette,
                    which can be a default seaborn palette, a custom seaborn palette, or a custom
                    matplotlib cmap.
                labelRotate : float or int, default = 45
                    Degrees by which the xtick labels are rotated.
                yUnits : string, default = 'f'
                    Determines units of y-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # Create vertical box plot.
        g = sns.boxplot(x = x
                        ,y = y
                        ,data = data
                        ,orient = 'v'
                        ,palette = color
                        ,ax = ax).set(
                                    xlabel = None
                                    ,ylabel = None
                                )
        
        # Resize x-axis labels as needed.
        unique = np.unique(data[x])
        if len(unique) > 10 and len(unique) <= 20:
            ax.tick_params(axis = 'x', labelsize = 1.2 * self.chartProp)
        elif len(unique) > 20:
            ax.tick_params(axis = 'x', labelsize = 0.6 * self.chartProp)
        
        # Fade box plot figures by reducing alpha.
        plt.setp(ax.artists, alpha = 0.8)
        
        # Rotate x-tick labels.
        plt.xticks(rotation = labelRotate)
        ax.yaxis.set_visible(False)

        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, yUnits = yUnits)
            
    def prettyBoxPlotH(self, x, y, data, color = style.styleHexMid, xUnits = 'f', ax = None):
        """
        Documentation:
            Description:
                Create horizontal box plots. Useful for evaluating a categorical target on the y-axis
                vs. a continuous independent variable on the x-axis
            Parameters:
                x : string
                    Name of independent variable in dataframe. Represents a category
                y : string
                    Name of continuous target variable. 
                data : Pandas DataFrame
                    Pandas DataFrame including both indpedent variable and target variable.
                color : string (some sort of color code), default = style.styleHexMid
                    Determines color of box plot figures. Ideally this object is a color palette,
                    which can be a default seaborn palette, a custom seaborn palette, or a custom
                    matplotlib cmap.
                xUnits : string, default = 'f'
                    Determines units of x-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # Create horizontal box plot.
        g = sns.boxplot(x = x
                        ,y = y
                        ,hue = y
                        ,data = data
                        ,orient = 'h'
                        ,palette = color
                        ,ax = ax).set(
                                    xlabel = None
                                    ,ylabel = None
                                )
        
        # Fade box plot figures by reducing alpha.
        plt.setp(ax.artists, alpha = 0.8)
        ax.yaxis.set_visible(False)
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits)
        plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0.)
    
    def prettyRegPlot(self, x, y, data, color = style.styleHexMid[0], x_jitter = None, xUnits = 'f', yUnits = 'f', ax = None):
        """
        Documentation:
            Description:

            Parameters:
                x : string
                    Name of independent variable in dataframe. Represents a category
                y : string
                    Name of continuous target variable. 
                data : Pandas DataFrame
                    Pandas DataFrame including both indepedent variable and target variable.
                color : string
                    Determines color of dots and regression line.
                labelRotate : float or int, default = 45
                    Degrees by which the xtick labels are rotated.
                yUnits : string, default = 'f'
                    Determines units of y-axis tick labels. 'f' displays float. '%' displays percentages, 
                    '$' displays dollars. 'd' displays real numbers.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # Create vertical box plot.
        g = sns.regplot(x = x
                        ,y = y
                        ,data = data
                        ,x_jitter = x_jitter
                        # ,color = color
                        ,scatter_kws = {'alpha' : 0.3
                                        ,'color' : style.styleHexMid[0]}
                        ,line_kws = {'color' : style.styleHexMid[1]}
                        ,ax = ax).set(
                                    xlabel = None
                                    ,ylabel = None
                                )        
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)
    
    def prettyPairPlot(self, df, cols = None, target = None, targetName = None, diag_kind = 'auto', legendLabels = None, bbox_to_anchor = None):
        """
        Documentation:
            Description: 
                Create pair plot that produces a grid of scatter plots for all unique pairs of
                continuous features.
            Parameters:
                df : Pandas DataFrame
                    Pandas DataFrame containing data of interest.
                vars : list, default = None
                    List of strings describing columns in Pandas DataFrame to be visualized.
                hue : string, default = None
                    Variable name to be used to introduce third dimension to scatter plots through
                    a color hue.
                diag_kind : string, default = 'auto.
                    Type of plot created along diagonal.
        """
        # Custom plot formatting settings for this particular chart.
        with plt.rc_context({'axes.titlesize' : 3.5 * self.chartProp
                            ,'axes.labelsize' : 1.5 * self.chartProp  # Axis title font size
                            ,'xtick.labelsize' : 1.2 * self.chartProp
                            ,'xtick.major.size' : 0.5 * self.chartProp
                            ,'xtick.major.width' : 0.05 * self.chartProp
                            ,'xtick.color' : style.styleGrey
                            ,'ytick.labelsize' : 1.2 * self.chartProp
                            ,'ytick.major.size' : 0.5 * self.chartProp
                            ,'ytick.major.width' : 0.05 * self.chartProp
                            ,'ytick.color' : style.styleGrey
                            ,'figure.facecolor' : style.styleWhite
                            ,'axes.facecolor': style.styleWhite
                            ,'axes.spines.left': False
                            ,'axes.spines.bottom': False
                            ,'axes.edgecolor': style.styleGrey
                            ,'axes.grid': False
                            }):
            
            # capture all predictor columns
            if cols is None:
                cols = df.select_dtypes(exclude = [object]).columns
                # cols = df.columns.tolist()
                # cols = [x for x in train.X_.columns if x is not targetName]
            
            if target is not None:
                df = pd.merge(df[cols]
                            ,pd.DataFrame(target
                                            ,columns = [targetName])
                        ,left_index = True
                        ,right_index = True)

            # Create pair plot.
            g = sns.pairplot(data = df.dropna()
                            ,vars = cols
                            ,hue = targetName
                            ,diag_kind = diag_kind
                            ,height = 0.2 * self.chartProp
                            ,plot_kws = {'s' : 2.0 * self.chartProp
                                         ,'edgecolor' : None
                                         ,'linewidth' : 1
                                         ,'alpha' : 0.7
                                         ,'marker' : 'o'
                                         ,'facecolor' : style.styleHexMid[0] if target is None else None
                                        }
                            ,diag_kws = {'facecolor' : style.styleHexMid[1] if target is None else None
                                        }
                            ,palette = style.styleHexMid
                            )
            
            g._legend.remove()

            for ax in g.axes.flat:
                _ = ax.set_ylabel(ax.get_ylabel(), rotation = 55)
                _ = ax.set_xlabel(ax.get_xlabel(), rotation = 55)
                _ = ax.xaxis.labelpad = 20
                _ = ax.yaxis.labelpad = 75
                _ = ax.xaxis.label.set_color(style.styleGrey)
                _ = ax.yaxis.label.set_color(style.styleGrey)            
            
            plt.subplots_adjust(hspace = 0.0, wspace = 0.0)
            
            # Add custom legend describing hue labels
            if target is not None:
                
                ## create custom legend
                # create labels
                if legendLabels is None:
                    legendLabels = np.unique(df[df[targetName].notnull()][targetName])
                else:
                    legendLabels = np.array(legendLabels)

                labelColor = {}
                for ix, i in enumerate(legendLabels):
                    labelColor[i] = style.styleHexMid[ix]

                # create patches
                patches = [matplotlib.patches.Patch(color = v, label = k) for k, v in labelColor.items()]
                
                # draw legend
                leg = plt.legend(handles = patches
                            ,fontsize = 1.0 * self.chartProp
                            ,loc = 'upper right'
                            ,markerscale = 0.5 * self.chartProp
                            ,ncol = 1
                            ,bbox_to_anchor = bbox_to_anchor
                )

                # label font color
                for text in leg.get_texts():
                    plt.setp(text, color = 'Grey')

                
    def prettyCorrHeatmap(self, df, target = None, targetName = None, annot = True, cols = None, ax = None, vmin = -1.0, vmax = 1.0):
        """
        Documentation:
            Description:
                Using continuous features, create correlation heatmap. Produces correlation
                with all numerical features, and can be limited to certain features using 'cols'.
            Parameters:
                df : Pandas DataFrame
                    Pandas DataFrame
                annot : boolean, default = True
                    Determines whether or not correlation table is annoted wil correlation
                    value or not.
                cols : list, default = None
                    List of strings describing dataframe column. Limits dataframe to select
                    columns.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
            Returns:
                corrSummDf : Pandas DataFrame
                    Pandas DataFrame summarizing highest correlation coefficients between 
                    features and target.
        """
        if target is not None:
            df = pd.merge(df, pd.DataFrame(target, columns = [targetName]), left_index = True, right_index = True)
        
        if cols is None:
            cols = df.columns
        
        # Create correlation matrix
        corrMatrix = df[cols].corr() if cols is not None else df.corr() 
        
        if len(cols) <= 5:
            fontAdjust = 1.25
        elif len(cols) > 5 and len(cols) <= 10:
            fontAdjust = 0.95
        elif len(cols) > 10 and len(cols) <= 20:
            fontAdjust = 0.85
        elif len(cols) > 20 and len(cols) <= 30:
            fontAdjust = 0.75
        elif len(cols) > 30 and len(cols) <= 40:
            fontAdjust = 0.65
        else:
            fontAdjust = 0.45

        # Create heatmap using correlation matrix
        g = sns.heatmap(corrMatrix
                    ,vmin = vmin
                    ,vmax = vmax
                    ,annot = annot
                    ,annot_kws = {'size' : fontAdjust * self.chartProp}
                    ,square = False
                    ,ax = ax
                    ,xticklabels = True
                    ,yticklabels = True
                    ,cmap = LinearSegmentedColormap.from_list(name = ''
                                                            ,colors = [style.styleHexMid[2], 'white', style.styleHexMid[0]])
                    )

        # Format x and y-tick labels
        g.set_yticklabels(g.get_yticklabels(), rotation = 0, fontsize = 1.0 * self.chartProp)
        g.set_xticklabels(g.get_xticklabels(), rotation = 90, fontsize = 1.0 * self.chartProp)

        # Customize color bar formatting
        cbar = g.collections[0].colorbar
        cbar.ax.tick_params(labelsize = fontAdjust * self.chartProp, colors = style.styleGrey, length = 0)
        cbar.set_ticks([1.0, 0.0, -1.0])

    def prettyCorrHeatmapRefine(self, df, target = None, targetName = None, annot = True, cols = None, thresh = 0.5, ax = None):
        """
        Documentation:
            Description:
                Using continuous features, create correlation heatmap. Capable of dropping 
                zeros in select features, where zeros potentially indicate a complete absence
                of the feature.
            Parameters:
                df : Pandas DataFrame
                    Pandas DataFrame
                annot : boolean, default = True
                    Determines whether or not correlation table is annoted wil correlation
                    value or not.
                cols : list, default = None
                    List of strings describing dataframe column. Limits dataframe to select
                    columns.
                corrFocus : string, default = self.target[0]
                    The feature of focus in the supplemental correlation visualization. Used
                    to determine the feature for which the nlargest correlation coefficients
                    are returned.
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
            Returns:
                corrSummDf : Pandas DataFrame
                    Pandas DataFrame summarizing highest correlation coefficients between 
                    features and target.
        """
        df = pd.merge(df, pd.DataFrame(target, columns = [targetName]), left_index = True, right_index = True)
                

        # Limit to top correlated features relative to targetName
        corrMatrix = df[cols].corr() if cols is not None else df.corr() 
        corrTop = corrMatrix[targetName]#[:-1]
        corrTop = corrTop[abs(corrTop) > thresh].sort_values(ascending = False)
        display(pd.DataFrame(corrTop))        
        
        if len(corrTop) <= 5:
            fontAdjust = 1.25
        elif len(corrTop) > 5 and len(corrTop) <= 10:
            fontAdjust = 1.15
        elif len(corrTop) > 10 and len(corrTop) <= 20:
            fontAdjust = 1.05
        elif len(corrTop) > 20 and len(corrTop) <= 30:
            fontAdjust = 0.95
        elif len(corrTop) > 30 and len(corrTop) <= 40:
            fontAdjust = 0.85
        else:
            fontAdjust = 0.65


        # Create heatmap using correlation matrix
        g = sns.heatmap(df[corrTop.index].corr()
                    ,vmin = -1.0
                    ,vmax = 1.0
                    ,annot = annot
                    ,annot_kws = {'size' : fontAdjust * self.chartProp}
                    ,square = False
                    ,ax = ax
                    ,xticklabels = True
                    ,yticklabels = True
                    ,cmap = LinearSegmentedColormap.from_list(name = ''
                                                            ,colors = [style.styleHexMid[2], 'white', style.styleHexMid[0]])
                    )

        # Format x and y-tick labels
        g.set_yticklabels(g.get_yticklabels(), rotation = 0, fontsize = fontAdjust * self.chartProp)
        g.set_xticklabels(g.get_xticklabels(), rotation = 90, fontsize = fontAdjust * self.chartProp)

        # Customize color bar formatting
        cbar = g.collections[0].colorbar
        cbar.ax.tick_params(labelsize = fontAdjust * self.chartProp, colors = style.styleGrey, length = 0)
        cbar.set_ticks([1.0, 0.0, -1.0])

        plt.show()          

    # Evaluation
    def prettyConfusionMatrix(self, yTest, yPred, ax = None):
        """
        Documentation:
            Description:
                yTest : array
                    1-dimensional array containing true values
                yPred : array
                    1-dimensional array containing predictions
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within `function.
        """
        # Create confution matrix.
        cm = pd.DataFrame(metrics.confusion_matrix(y_true = yTest
                                                    , y_pred = yPred)
                                                    )
        
        # Sort rows and columns in descending order
        cm.sort_index(axis = 1, ascending = False, inplace = True)
        cm.sort_index(axis = 0, ascending = False, inplace = True)
        
        # Apply heatmap styling to confusion matrix.
        sns.heatmap(data = cm
                    ,annot = True
                    ,square = True
                    ,cbar = False
                    ,cmap = 'Blues'
                    ,annot_kws = {'size' : 2.5 * self.chartProp})
        
        # Remove top tick marks and add labels
        ax.xaxis.tick_top()
        plt.xlabel('predicted', size = 40)
        plt.ylabel('actual', size = 40)
        
    def prettyRocCurve(self, model, xTrain, yTrain, xTest, yTest, linecolor, ax = None):
        """
        Documentation:
            Description:
                Plot ROC curve and report AUC
            Parameters:
                model : sklearn model or pipeline
                    model to fit
                xTrain : array
                    Training data to fit model
                yTrain : array
                    Training data to fit model
                xTest : array
                    Test data to return predict_probas
                yTest : array
                    Test data for creating roc_curve
                linecolor : str
                    line color
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within `function.
        """
        # Return prediction probabilities.
        probas = model.fit(xTrain, yTrain).predict_proba(xTest)
        
        # Return false positive rate, true positive rate and thresholds.
        fpr, tpr, thresholds = metrics.roc_curve(y_true = yTest, y_score = probas[:, 1], pos_label = 1)
        
        # Calculate area under the curve using FPR and TPR.
        roc_auc = metrics.auc(fpr, tpr)
        
        # Plot ROC curve.
        self.prettyLine(x = fpr
                        ,y = tpr
                        ,label = ['ROC AUC = {:.3f}'.format(roc_auc)]
                        ,linecolor = linecolor
                        ,xUnits = 'fff'
                        ,yUnits = 'fff'
                        ,bbox = (1.0, 0.8)
                        ,ax = ax
                    )
        
        # Plot 'random guess' line.
        self.prettyLine(x = np.array([0, 1])
                        ,y = np.array([0, 1])
                        ,linecolor = style.styleGrey
                        ,linestyle = '--'
                        ,xUnits = 'fff'
                        ,yUnits = 'fff'
                        ,ax = ax
                    )
        
        # Plot 'perfection' line.
        self.prettyLine(x = np.array([0, 0, 1])
                        ,y = np.array([0, 1, 1])
                        ,linecolor = style.styleGrey
                        ,linestyle = ':'
                        ,xUnits = 'fff'
                        ,yUnits = 'fff'
                        ,ax = ax
                    )

    def prettyDecisionRegion(self, x, y, classifier, testIdx = None, resolution = 0.1, bbox = (1.2, 0.9), ax = None):
        """
        Documentation:
            Description:
                Create 2-dimensional chart with shading used to highlight decision regions.
            Parameters:
                X : array
                    m x 2 array containing 2 features.
                y : array
                    m x 1 array containing labels for observations.
                classifier : sklearn model
                    Classifier used to create decision regions.
                testIdx :  tuple, default = None
                    Option parameter for specifying observations to be highlighted
                    as test examples.
                resolution : float, default = 0.001
                    Controls clarity of the graph by setting interval of the arrays 
                    passed into np.meshgrid.
                bbox : tuple of floats, default = (1.2, 0.9)
                    Coordinates for determining legend position
                ax : Axes object, default = None
                    Axes object containing figure elements to be adjusted within function.
        """
        # objects for marker generator and color map
        cmap = ListedColormap(style.styleHexLight[:len(np.unique(y))])
        
        # plot decision surface
        x1Min, x1Max = x[:, 0].min() - 1, x[:, 0].max() + 1
        x2Min, x2Max = x[:, 1].min() - 1, x[:, 1].max() + 1
        
        xx1, xx2 = np.meshgrid(np.arange(x1Min, x1Max, resolution)
                            ,np.arange(x2Min, x2Max, resolution))
        
        Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
        Z = Z.reshape(xx1.shape)
        plt.contourf(xx1, xx2, Z, alpha = 0.3, cmap = cmap)
        plt.xlim(xx1.min(), xx1.max())
        plt.ylim(xx2.min(), xx2.max())
        
        # Plot samples
        for idx, cl in enumerate(np.unique(y)):
            plt.scatter(x = x[y == cl, 0]
                    ,y = x[y == cl, 1]
                    ,alpha = 1.0
                    ,c = style.styleHexMid[idx]
                    ,marker = style.styleMarkers[1]
                    ,label = cl
                    ,s = 12.5 * self.chartProp
                    ,edgecolor = style.styleHexMidDark[idx]
                    )
        
        # Highlight test samples
        if testIdx:
            xTest = x[testIdx, :]
            plt.scatter(xTest[:,0]
                        ,xTest[:,1]
                        ,facecolor = 'none'
                        ,edgecolor = 'white'
                        ,alpha = 1.0
                        ,linewidth = 1.4
                        ,marker = 'o'
                        ,s = 12.75 * self.chartProp
                        ,label = 'test set'                   
                    )
        # Add legend to figure
        plt.legend(loc = 'upper right'
                    ,bbox_to_anchor = bbox
                    ,ncol = 1
                    ,frameon = True
                    ,fontsize = 1.1 * self.chartProp
                    )
        plt.tight_layout()

    def prettyResidualPlot(self):
        pass

    def prettyTwoCatBar(self, df, x, hue, target, targetName, xUnits = None, yUnits = None, bbox_to_anchor = None, legendLabels = None, ax = None):
        """
        Documentation:
            Description:
                desc
            Parameters:
        """
        df = pd.merge(df[[x, hue]]
                            ,pd.DataFrame(target * 100
                                         ,columns = [targetName])
                        ,left_index = True
                        ,right_index = True)
        
        g = sns.barplot(x = x
                        ,y = targetName
                        ,hue = hue
                        ,data = df
                        ,palette = style.styleHexMid
                        ,ax = ax
                        ,ci = None)
        
        # Format x and y-tick labels
        g.set_yticklabels(g.get_yticklabels(), rotation = 0, fontsize = 1.25 * self.chartProp, color = style.styleGrey)
        g.set_xticklabels(g.get_xticklabels(), rotation = 0, fontsize = 1.25 * self.chartProp, color = style.styleGrey)
        g.set_ylabel(g.get_ylabel(), rotation = 90, fontsize = 1.75 * self.chartProp, color = style.styleGrey)
        g.set_xlabel(g.get_xlabel(), rotation = 0, fontsize = 1.75 * self.chartProp, color = style.styleGrey)
        

        ## create custom legend
        # create labels
        if legendLabels is None:
            legendLabels = np.unique(df[df[hue].notnull()][hue])
        else:
            legendLabels = np.array(legendLabels)

        labelColor = {}
        for ix, i in enumerate(legendLabels):
            labelColor[i] = style.styleHexMid[ix]

        # create patches
        patches = [matplotlib.patches.Patch(color = v, label = k) for k, v in labelColor.items()]
        
        # draw legend
        leg = plt.legend(handles = patches
                    ,fontsize = 1.0 * self.chartProp
                    ,loc = 'upper right'
                    ,markerscale = 0.5 * self.chartProp
                    ,ncol = 1
                    ,bbox_to_anchor = bbox_to_anchor
        )

        # label font color
        for text in leg.get_texts():
            plt.setp(text, color = 'Grey')
        
        # Axis tick label formatting.
        util.utilLabelFormatter(ax = ax, xUnits = xUnits, yUnits = yUnits)            

    def prettyCatNumHistFacet(self, df, target, targetName, catRow, catCol, numCol, bbox_to_anchor = None, aspect = 1, height = 4, legendLabels = None):
        """
        Documentation:
            Description:
                desc
            Parameters:
                df : Pandas DataFrame
                    desc
                target : 
                    desc
                targetName : 
                    desc
                catRow : 
                    desc
                catCol : 
                    desc
                numCol : 
                    desc
                bbox_to_anchor : 
                    desc
                aspect : float, default = 1 
                    desc
                height : float, default = 4
                    desc
                legendLabels : list, default = None
                    desc
        """
        df = pd.merge(df[[catRow, catCol, numCol]]
                        ,pd.DataFrame(target
                                        ,columns = [targetName])
                    ,left_index = True
                    ,right_index = True)
        
        g = sns.FacetGrid(df
                          ,row = catRow
                          ,col = catCol
                          ,hue = targetName
                          ,palette = style.styleHexMid
                          ,despine = True
                          ,height = height
                          ,aspect = aspect)
        g.map(plt.hist, numCol, alpha = .75)
        
        for ax in g.axes.flat:
            _ = ax.set_ylabel(ax.get_ylabel(), rotation = 0, fontsize = 1.75 * self.chartProp, color = style.styleGrey)
            _ = ax.set_xlabel(ax.get_xlabel(), rotation = 0, fontsize = 1.25 * self.chartProp, color = style.styleGrey)
            # _ = ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, fontsize = 1.05 * self.chartProp, color = style.styleGrey)
            # _ = ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, fontsize = 1.05 * self.chartProp, color = style.styleGrey)
            _ = ax.set_title(ax.get_title(), rotation = 0, fontsize = 1.05 * self.chartProp, color = style.styleGrey)
        
        ## create custom legend
        # create labels
        if legendLabels is None:
            legendLabels = np.unique(target)
        else:
            legendLabels = np.array(legendLabels)

        labelColor = {}
        for ix, i in enumerate(legendLabels):
            labelColor[i] = style.styleHexMid[ix]

        # create patches
        patches = [matplotlib.patches.Patch(color = v, label = k) for k, v in labelColor.items()]
        
        # draw legend
        leg = plt.legend(handles = patches
                    ,fontsize = 1.0 * self.chartProp
                    ,loc = 'upper right'
                    ,markerscale = 0.5 * self.chartProp
                    ,ncol = 1
                    ,bbox_to_anchor = bbox_to_anchor
        )

        # label font color
        for text in leg.get_texts():
            plt.setp(text, color = 'Grey')
        
    def prettyTwoCatPointFacet(self, df, target, targetName, catLine, catPoint, catGrid, bbox_to_anchor = None, aspect = 1, height = 4, legendLabels = None):
        """
        Documentation:
            Description:
                desc
            Parameters:
        """
        df = pd.merge(df[[catLine, catPoint, catGrid]]
                        ,pd.DataFrame(target
                                        ,columns = [targetName])
                    ,left_index = True
                    ,right_index = True)
        g = sns.FacetGrid(df
                         ,catGrid
                         ,aspect = aspect
                         ,height = height
                         )
        g.map(sns.pointplot
             ,catPoint
             ,targetName
             ,catLine
             ,order = df[catPoint].sort_values().drop_duplicates().values.tolist()
             ,hue_order = df[catLine].sort_values().drop_duplicates().values.tolist()
             ,palette = style.styleHexMid
             ,alpha = .75
             )
        
        for ax in g.axes.flat:
            _ = ax.set_ylabel(ax.get_ylabel(), rotation = 90, fontsize = 0.95 * self.chartProp, color = style.styleGrey)
            _ = ax.set_xlabel(ax.get_xlabel(), rotation = 0, fontsize = 0.95 * self.chartProp, color = style.styleGrey)
            # _ = ax.set_yticklabels(ax.get_yticklabels(), rotation = 0, fontsize = 0.85 * self.chartProp, color = style.styleGrey)
            # _ = ax.set_xticklabels(ax.get_xticklabels(), rotation = 0, fontsize = 0.85 * self.chartProp, color = style.styleGrey)
            _ = ax.set_title(ax.get_title(), rotation = 0, fontsize = 1.05 * self.chartProp, color = style.styleGrey)
        
        ## create custom legend
        # create labels
        if legendLabels is None:
            legendLabels = np.unique(df[df[catLine].notnull()][catLine])
        else:
            legendLabels = np.array(legendLabels)

        labelColor = {}
        for ix, i in enumerate(legendLabels):
            labelColor[i] = style.styleHexMid[ix]

        # create patches
        patches = [matplotlib.patches.Patch(color = v, label = k) for k, v in labelColor.items()]
        
        # draw legend
        leg = plt.legend(handles = patches
                    ,fontsize = 1.0 * self.chartProp
                    ,loc = 'upper right'
                    ,markerscale = 0.5 * self.chartProp
                    ,ncol = 1
                    ,bbox_to_anchor = bbox_to_anchor
        )

        # label font color
        for text in leg.get_texts():
            plt.setp(text, color = 'Grey')