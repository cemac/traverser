# -*- coding: utf-8 -*-
"""
Traverser status area
"""

# Third party imports:
from PyQt5.Qt import QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QScatterSeries
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QLabel
# Package imports:
from traverser.ui_components.ui_component import UIComponent

class StatusArea(UIComponent):
    """
    Status area for traverser UI
    """
    def __init__(self, ui):
        # Run parent init first:
        super().__init__(ui, 3)
        # Store ui:
        self.ui = ui
        # Run component init:
        self.init()

    def chart_status(self, ui):
        """
        Draw chart of traverse status
        """
        # Set x and y bounds 0 -> 1, values will be normalised for plotting:
        min_x = 0
        max_x = 1
        min_y = 0
        max_y = 1
        # If traverse x axis is longer than y axis, rotate the axes:
        if ui.config.values['max_x'] > ui.config.values['max_y']:
             rotate_axes = True
             min_x = 1 - min_x
             max_x = 1 - max_x
        else:
             rotate_axes = False
        # Grid line Increments / positions:
        x_grid_inc = 0.1
        y_grid_inc = 0.1
        # Create Line series to draw area bounds:
        area_bounds = QLineSeries()
        area_bounds.append(min_x, max_y)
        area_bounds.append(max_x, max_y)
        area_bounds.append(max_x, min_y)
        # Set style (dashed line):
        ab_color = area_bounds.color()
        ab_color.setNamedColor('#0066ff')
        ab_pen = area_bounds.pen()
        ab_pen.setColor(ab_color)
        ab_pen.setStyle(2)
        area_bounds.setPen(ab_pen)
        # Line series for x and y axes:
        xy_axes = QLineSeries()
        xy_axes.append(min_x, min_y)
        xy_axes.append(max_x, min_y)
        xy_axes.append(min_x, min_y)
        xy_axes.append(min_x, max_y)
        # Set style (solid line):
        xy_color = xy_axes.color()
        xy_color.setNamedColor('#0066ff')
        xy_pen = xy_axes.pen()
        xy_pen.setColor(xy_color)
        xy_pen.setStyle(1)
        xy_axes.setPen(xy_pen)
        # Scatter serieses for axes labels:
        xl_axes = QScatterSeries()
        xl_axes.setMarkerSize(0)
        xl_axes.setPointLabelsVisible(True)
        if rotate_axes:
            xl_axes.append(0.05, -0.065)
            xl_axes.setPointLabelsFormat('y')
        else:
            xl_axes.append(0.95, -0.065)
            xl_axes.setPointLabelsFormat('x')
        yl_axes = QScatterSeries()
        yl_axes.setMarkerSize(0)
        yl_axes.setPointLabelsVisible(True)
        if rotate_axes:
            yl_axes.append(1.05, 0.925)
            yl_axes.setPointLabelsFormat('x')
        else:
            yl_axes.append(-0.05, 0.925)
            yl_axes.setPointLabelsFormat('y')
        # Create the chart:
        chart_status = QChart()
        # Set margins:
        chart_status.setMargins(QMargins(-20, -10, -8, -25))
        # Remove rounded corners:
        chart_status.setBackgroundRoundness(0)
        # Add serieses to chart:
        chart_status.addSeries(area_bounds)
        chart_status.addSeries(xy_axes)
        chart_status.addSeries(xl_axes)
        chart_status.addSeries(yl_axes)
        # Create axes:
        chart_status.createDefaultAxes()
        chart_axes = chart_status.axes()
        chart_x_axis = chart_axes[0]
        chart_y_axis = chart_axes[1]
        # Set axes min and max values:
        chart_x_axis.setRange(-0.1, 1.1)
        chart_y_axis.setRange(-0.1, 1.1)
        # set tick count / number of grid lines:
        chart_x_axis.setTickCount(13)
        chart_y_axis.setTickCount(13)
        # Remove axes lines:
        chart_x_axis.setLineVisible(False)
        chart_y_axis.setLineVisible(False)
        # Remove axes labels:
        chart_x_axis.setLabelFormat(' ')
        chart_x_axis.setLabelsVisible(False)
        chart_y_axis.setLabelFormat(' ')
        chart_y_axis.setLabelsVisible(False)
        # Remove legend:
        chart_status.legend().setVisible(False)
        # chart view?
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setChart(chart_status)
        # Return the components:
        return area_bounds, chart_status, chart_view

    def status_property(self, ui, label, value):
        """
        Return a status property display object
        """
        # Label for the property:
        text_label = '{0} :'.format(label)
        property_label = QLabel(text_label, self)
        property_label.setTextFormat(Qt.PlainText)
        property_label.setFont(ui.fonts['bold'])
        property_label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        # Value for the property:
        property_value = QLabel(value, self)
        property_value.setTextFormat(Qt.PlainText)
        property_value.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # Return the label and value:
        return property_label, property_value

    def init(self):
        """
        Main component init
        """
        # Get the ui:
        ui = self.ui
        # Get self grid:
        grid = self.properties['grid']
        # Create a label for the area:
        self.properties['label'] = QLabel('Status', self)
        label = self.properties['label']
        label.setTextFormat(Qt.PlainText)
        label.setFont(ui.fonts['bold'])
        grid.addWidget(label, 0, 0, 1, 1)
        # Add traverse status chart:
        (self.properties['area_bounds'], self.properties['chart_status'],
             self.properties['chart_view']) = self.chart_status(ui)
        chart_view = self.properties['chart_view']
        grid.addWidget(chart_view, 1, 0, 1, 3)
        # Add size labels ... X:
        self.properties['x_slabel'], self.properties['x_svalue'] = (
            self.status_property(ui, 'X Size', ' -- ')
        )
        x_slabel = self.properties['x_slabel']
        x_svalue = self.properties['x_svalue']
        grid.addWidget(x_slabel, 2, 0, 1, 1)
        grid.addWidget(x_svalue, 2, 1, 1, 2)

        # Add size labels ... Y:
        self.properties['y_slabel'], self.properties['y_svalue'] = (
            self.status_property(ui, 'Y Size', ' -- ')
        )
        y_slabel = self.properties['y_slabel']
        y_svalue = self.properties['y_svalue']
        grid.addWidget(y_slabel, 3, 0, 1, 1)
        grid.addWidget(y_svalue, 3, 1, 1, 2)
        # Add status labels ... X:
        self.properties['x_plabel'], self.properties['x_pvalue'] = (
            self.status_property(ui, 'X Position', ' -- ')
        )
        x_plabel = self.properties['x_plabel']
        x_pvalue = self.properties['x_pvalue']
        grid.addWidget(x_plabel, 4, 0, 1, 1)
        grid.addWidget(x_pvalue, 4, 1, 1, 2)
        # Y:
        y_units = ui.config.values['y_units']
        self.properties['y_plabel'], self.properties['y_pvalue'] = (
            self.status_property(ui, 'Y Position', ' -- ')
        )
        y_plabel = self.properties['y_plabel']
        y_pvalue = self.properties['y_pvalue']
        grid.addWidget(y_plabel, 5, 0, 1, 1)
        grid.addWidget(y_pvalue, 5, 1, 1, 2)
        # Init current_pos value:
        self.properties['current_pos'] = None
