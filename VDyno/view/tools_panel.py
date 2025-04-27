"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code contains ToolsPanel class, which sends various signals to the presenter class when the user changes the values in the GUI.

written by:
    - Daniel Muir

"""


from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QToolBox,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QMainWindow,
)


class ToolsPanel(QVBoxLayout):
    """A class to set up a permanent tools panel with a QToolBox for motor control, graph settings, and data filters."""

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent
        self.setupToolsPanel()

    def setupToolsPanel(self):
        """Set up a permanent tools panel with a QToolBox for motor control, graph settings, and data filters."""
        settings_toolbox = QToolBox()
        settings_toolbox.setFixedWidth(300)
        settings_toolbox.setCurrentIndex(0)  # Show the first tab by default

        # Tab 1: Motor Control
        motor_control_tab = QWidget()
        motor_control_layout = QVBoxLayout()
        motor_control_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Manual Control Checkbox
        manual_control_cb = QCheckBox("Manual Control")
        manual_control_cb.setChecked(False)  # Default to unchecked

        # MUT Current Spin Box
        MUT_current_label = QLabel("Relative Motor 1 current (A):")
        MUT_current_box = QDoubleSpinBox()
        MUT_current_box.setRange(-5.0, 5.0)  # Set the range for RPM input
        MUT_current_box.setSingleStep(0.1)  # Set the step size for duty cycle input
        MUT_current_box.setValue(0)  # Set a default value
        MUT_current_box.setEnabled(False)  # Initially disabled

        MUT_current_box.valueChanged.connect(self.parent.change_MUT_current)

        # Load RPM Spin Box
        load_rpm_label = QLabel("Motor 2 rpm:")
        load_rpm_input = QSpinBox()
        load_rpm_input.setRange(0, 10000)  # Set the range for duty cycle input
        load_rpm_input.setSingleStep(100)  # Set the step size for duty cycle input
        load_rpm_input.setValue(0)  # Set a default value
        load_rpm_input.setEnabled(False)  # Initially disabled

        load_rpm_input.valueChanged.connect(self.parent.change_load_rpm)

        # Define a method to enable/disable spin boxes
        def toggle_manual_control(state):
            print(f"Manual Control state changed to: {state}")
            is_checked = state
            print(f"Is checked: {is_checked}")
            MUT_current_box.setEnabled(is_checked)
            load_rpm_input.setEnabled(is_checked)

        # Connect Manual Control Checkbox to the toggle method
        manual_control_cb.stateChanged.connect(toggle_manual_control)

        # Add widgets to the layout
        motor_control_layout.addWidget(manual_control_cb)
        motor_control_layout.addWidget(MUT_current_label)
        motor_control_layout.addWidget(MUT_current_box)
        motor_control_layout.addWidget(load_rpm_label)
        motor_control_layout.addWidget(load_rpm_input)

        motor_control_tab.setLayout(motor_control_layout)
        settings_toolbox.addItem(motor_control_tab, "Motor Control")

        # Tab 2: Graph Settings
        graph_settings_tab = QWidget()
        graph_settings_layout = QVBoxLayout()
        graph_settings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        show_grid_cb = QCheckBox("Show Grid")
        show_grid_cb.setChecked(True)

        show_legend_cb = QCheckBox("Show Legend")
        show_legend_cb.setChecked(True)

        graph_settings_layout.addWidget(show_grid_cb)
        graph_settings_layout.addWidget(show_legend_cb)
        graph_settings_tab.setLayout(graph_settings_layout)

        settings_toolbox.addItem(graph_settings_tab, "Results Window")

        # Emit signal when the tab changes
        settings_toolbox.currentChanged.connect(self.parent.tab_changed)

        # Set up the layout for the settings toolbox
        self.addWidget(settings_toolbox, 0, Qt.AlignmentFlag.AlignTop)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    from style_sheet import StyleSheet

    class window(QMainWindow):
        tab_changed = pyqtSignal(int)  # Signal for tab changes

        def __init__(self):
            super().__init__()
        
        def change_MUT_current(self, value):
            print(f"MUT current changed to: {value}")

        def change_load_rpm(self, value):   
            print(f"Load RPM changed to: {value}")


    app = QApplication(sys.argv)
    app.setStyle("WindowsVista")
    app.setStyleSheet(StyleSheet)

    trial = window()

    tools_panel = ToolsPanel(trial)

    # Create a central widget and set the layout
    central_widget = QWidget()
    main_layout = QVBoxLayout()
    main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    main_layout.addLayout(tools_panel)
    central_widget.setLayout(main_layout)

    trial.setCentralWidget(central_widget)
    trial.setWindowTitle("Tools Panel")
    trial.show()

    sys.exit(app.exec())
