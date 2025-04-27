"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code is a test script for plotting CAN data using PyQTGraph. It is not part of the main application.
It proves useful for debugging and testing purposes. The plotting was based on the livePlot example from PyQTGraph.

written by:
    - Daniel Muir
"""

# Import libraries
from numpy import linspace
from pyqtgraph.Qt import QtWidgets
import pyqtgraph as pg

import serial
import can
import cantools
import os
import serial.tools.list_ports

# Search for the CAN transceiver
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ports = list(serial.tools.list_ports.comports())
for port in ports:
    if "USB-SERIAL CH340" in port.description:
        com_port = port.device
        break
else:
    raise Exception("USB-SERIAL CH340 not found")

# Start QT
app = QtWidgets.QApplication([])
app.setStyle("WindowsVista")

# Set the background color to white and the foreground (axes, text) to black
pg.setConfigOption("background", "w")  # White background
pg.setConfigOption("foreground", "k")  # Black axes and text

# Create the main window
win = pg.GraphicsLayoutWidget(show=True, title="Dyno Realtime")

# Input boxes
input_layout = QtWidgets.QVBoxLayout()
input_widget = QtWidgets.QWidget()
input_widget.setLayout(input_layout)

rpm_label = QtWidgets.QLabel("Motor 1 current::")
rpm_input = QtWidgets.QDoubleSpinBox()
rpm_input.setRange(0, 10000)  # Set the range for RPM input
rpm_input.setSingleStep(100)  # Set the step size for duty cycle input
rpm_input.setValue(0)  # Set a default value

brake_current_label = QtWidgets.QLabel("Motor 2 brake current:")
brake_current_input = QtWidgets.QDoubleSpinBox()
brake_current_input.setRange(-5.0, 5.0)
brake_current_input.setSingleStep(0.1)
brake_current_input.setValue(0)

input_layout.addWidget(rpm_label)
input_layout.addWidget(rpm_input)
input_layout.addWidget(brake_current_label)
input_layout.addWidget(brake_current_input)

# Proxy widget to embed the QWidget
proxy = QtWidgets.QGraphicsProxyWidget()
proxy.setWidget(input_widget)
win.addItem(proxy, row=0, col=0)

# First plot
p1 = win.addPlot(title="M.U.T RPM", row=0, col=1)
p1.getAxis("left").setPen(
    pg.mkPen(color="k", width=2)
)  # Black left axis with increased width
p1.getAxis("bottom").setPen(
    pg.mkPen(color="k", width=2)
)  # Black bottom axis with increased width
curve1 = p1.plot(pen=pg.mkPen(color="k", width=2))  # Black line with increased width

# Second plot
p2 = win.addPlot(title="Generator Brake Current", row=1, col=1)
p2.getAxis("left").setPen(pg.mkPen(color="k", width=2))
p2.getAxis("bottom").setPen(pg.mkPen(color="k", width=2))
curve2 = p2.plot(pen=pg.mkPen(color="k", width=2))

# Third plot
p3 = win.addPlot(title="Torque Sensor Reading", row=3, col=1)
p3.getAxis("left").setPen(pg.mkPen(color="k", width=2))
p3.getAxis("bottom").setPen(pg.mkPen(color="k", width=2))
curve3 = p3.plot(pen=pg.mkPen(color="k", width=2))

windowWidth = 500
Xm1 = linspace(0, 0, windowWidth)  # data array for first plot
Xm2 = linspace(0, 0, windowWidth)
Xm3 = linspace(0, 0, windowWidth)
ptr = -windowWidth

can_bus = can.interface.Bus(
    interface="seeedstudio", channel=com_port, baudrate=2000000, bitrate=500000
)

database = cantools.db.load_file("VESC.dbc")
tester = cantools.tester.Tester("VESC1", database, can_bus)
tester.start()

pole_pairs = 7


# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global ptr, Xm1, Xm2, Xm3, brake_current
    try:
        rpm_value = rpm_input.value()  # Use value() instead of text()
    except ValueError:
        rpm_value = 0  # default value if input is invalid
    try:
        brake_current = brake_current_input.value()
    except ValueError:
        brake_current = 0  # default value if input is invalid

    if rpm_value > 0:
        rpm_value = rpm_value * pole_pairs
        tester.send("VESC_Command_RPM_V1", {"Command_RPM_V1": rpm_value})
    tester.send(
        "VESC_Command_AbsBrakeCurrent_V2", {"Command_BrakeCurrent_V2": brake_current}
    )
    tester.flush_input()
    status1 = tester.expect(
        "VESC_Status1_V1", None, timeout=0.01, discard_other_messages=True
    )
    status2 = tester.expect(
        "VESC_Status1_V2", None, timeout=0.01, discard_other_messages=True
    )
    status3 = tester.expect(
        "TEENSY_Status", None, timeout=0.01, discard_other_messages=True
    )
    if status1 is not None:
        plotGraph(curve1, Xm1, status1, "Status_RPM_V1", (1 / pole_pairs))
    if status2 is not None:
        plotGraph(curve2, Xm2, status2, "Status_TotalCurrent_V2")
    if status3 is not None:
        plotGraph(curve3, Xm3, status3, "TorqueValue")
    QtWidgets.QApplication.processEvents()  # you MUST process the plot now


def plotGraph(curve, Xm, status, key, scaling=1):
    global ptr
    Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
    value = status[key]  # read line (single value) from the serial port
    value = value * scaling
    Xm[-1] = float(value)  # vector containing the instantaneous values
    ptr += 1  # update x position for displaying the curve
    curve.setData(Xm)  # set the curve with this data
    curve.setPos(ptr, 0)  # set x position in the graph to 0


## MAIN PROGRAM ##

while True:
    update()

pg.QtWidgets.QApplication.exec()
