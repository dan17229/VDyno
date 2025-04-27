"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code contains PlotData and PlotWindow classes, which together form a live plot of the data from the dyno object.
To speed up processing, the plotting is done in a separate thread using PyQTGraph's RemoteGraphicsView. The plotting was based on the remotePlot example from PyQTGraph.

written by:
    - Daniel Muir
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QComboBox
from numpy import zeros
from typing import Protocol

class Presenter(Protocol):  # allow for duck-typing of presenter class
    def plot_MUT_changed(self, index: int) -> None: ...
    def plot_load_changed(self, index: int) -> None: ...
    def plot_TT_changed(self, index: int) -> None: ...


def setup_dropdown(options: list) -> object:
    dropdown = QComboBox()
    dropdown.setFixedWidth(200)
    dropdown.addItems(options)
    return dropdown


class Plot_Data:
    """Class handling creation and updating of plot windows"""

    def __init__(self, window_width=200) -> None:
        super().__init__()
        self.Xm = zeros(window_width)  # Array to hold the data for the plot

    def extend(self, value) -> None:
        self.Xm[:-1] = self.Xm[1:]  # Shift data in the temporal mean 1 sample left
        self.Xm[-1] = float(value)  # Add the new value to the end of the array
        return self.Xm  # Return the updated array for plotting


class PlotWindow(pg.LayoutWidget):
    """Class forming the plot window UI"""

    def __init__(self, parent: Presenter) -> None:
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        super().__init__()
        self.parent = parent
        self.setMinimumHeight(400)
        self.MUT_index = 0
        self.Load_index = 0
        self.TT_index = 0
        self.setupInputs()
        self.setupLivePlot()
        self.show()

    def MUT_index_changed(self, index: int) -> None:
        self.MUT_index = index

    def Load_index_changed(self, index: int) -> None:
        self.Load_index = index

    def TT_index_changed(self, index: int) -> None:
        self.TT_index = index

    def setupInputs(self) -> None:
        dropdown1 = setup_dropdown(["MUT RPM", "MUT current (A)", "MUT duty cycle"])
        dropdown2 = setup_dropdown(
            ["Load motor RPM", "Load current (A)", "Load duty cycle"]
        )
        dropdown3 = setup_dropdown(["Torque (Nm)"])

        dropdown1.currentIndexChanged.connect(self.MUT_index_changed)
        dropdown2.currentIndexChanged.connect(self.Load_index_changed)
        dropdown3.currentIndexChanged.connect(self.TT_index_changed)

        # Combine the dropdowns into a single widget
        dropdown_widget = pg.LayoutWidget()
        dropdown_widget.addWidget(dropdown1, row=0, col=0)
        dropdown_widget.addWidget(dropdown2, row=1, col=0)
        dropdown_widget.addWidget(dropdown3, row=2, col=0)

        # Add the combined widget to the window
        self.addWidget(dropdown_widget, row=0, col=0)

    def setupLivePlot(self) -> None:
        view = pg.widgets.RemoteGraphicsView.RemoteGraphicsView()
        view.pg.setConfigOptions(
            antialias=True
        )  # Enable antialiasing for smoother plots
        self.parent.app.aboutToQuit.connect(view.close)

        # Add the view to the layout
        self.addWidget(view, row=0, col=1)

        # # Create a GraphicsLayout in the remote process
        layout = view.pg.GraphicsLayout()
        view.setCentralItem(layout)

        # # Create PlotItems directly in the remote process
        self.MUT_plot = layout.addPlot(row=0, col=0)
        self.Load_plot = layout.addPlot(row=1, col=0)
        self.TT_plot = layout.addPlot(row=2, col=0)

        # Initialize data arrays for each plot
        self.MUT_data_rpm = Plot_Data()
        self.MUT_data_current = Plot_Data()
        self.MUT_data_duty_cycle = Plot_Data()
        self.Load_data_rpm = Plot_Data()
        self.Load_data_current = Plot_Data()
        self.Load_data_duty_cycle = Plot_Data()
        self.TT_torque = Plot_Data()

    def update(self):
        """Update the plots with new data from the dyno object."""
        # Update MUT data
        mut_status = self.parent.dyno.MUT.status
        self.MUT_data_rpm.extend(mut_status["Status_RPM_V1"])
        self.MUT_data_current.extend(mut_status["Status_TotalCurrent_V1"])
        self.MUT_data_duty_cycle.extend(mut_status["Status_DutyCycle_V1"])

        mut_data_map = {
            0: self.MUT_data_rpm,
            1: self.MUT_data_current,
            2: self.MUT_data_duty_cycle,
        }
        if self.MUT_index in mut_data_map:
            self.MUT_plot.plot(
                mut_data_map[self.MUT_index].Xm, clear=True, _callSync="off", pen="k"
            )

        # Update Load motor data
        load_status = self.parent.dyno.load_motor.status
        self.Load_data_rpm.extend(load_status["Status_RPM_V2"])
        self.Load_data_current.extend(load_status["Status_TotalCurrent_V2"])
        self.Load_data_duty_cycle.extend(load_status["Status_DutyCycle_V2"])

        load_data_map = {
            0: self.Load_data_rpm,
            1: self.Load_data_current,
            2: self.Load_data_duty_cycle,
        }
        if self.Load_index in load_data_map:
            self.Load_plot.plot(
                load_data_map[self.Load_index].Xm, clear=True, _callSync="off", pen="k"
            )

        # Update Torque Transducer data
        self.TT_torque.extend(self.parent.dyno.torque_transducer.status["TorqueValue"])
        self.TT_plot.plot(self.TT_torque.Xm, clear=True, _callSync="off", pen="k")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    import os
    from random import randint

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    class DummyMotor:
        def __init__(self) -> None:
            self.status = {
                "Status_RPM_V1": 0,
                "Status_TotalCurrent_V1": 0,
                "Status_DutyCycle_V1": 0,
                "Status_RPM_V2": 0,
                "Status_TotalCurrent_V2": 0,
                "Status_DutyCycle_V2": 0,
            }

    class DummyTorqueTransducer:
        def __init__(self) -> None:
            self.status = {"TorqueValue": 0}

    class DummyPresenter:
        def __init__(self) -> None:
            self.dyno = DummyDyno()
            self.app = QApplication(sys.argv)

        def randomise(self):
            for key in self.dyno.MUT.status:
                self.dyno.MUT.status[key] += randint(-1, 1)
            for key in self.dyno.load_motor.status:
                self.dyno.load_motor.status[key] += randint(-1, 1)
            for key in self.dyno.torque_transducer.status:
                self.dyno.torque_transducer.status[key] += randint(-1, 1)

        def run(self):
            sys.exit(self.app.exec())

    class DummyDyno:
        def __init__(self) -> None:
            self.MUT = DummyMotor()
            self.load_motor = DummyMotor()
            self.torque_transducer = DummyTorqueTransducer()

    example = DummyPresenter()
    live_plot = PlotWindow(example)

    def update():
        live_plot.update()
        example.randomise()

    # Use a QTimer to periodically update the plots
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(10)  # Update every 10 ms

    example.run()
