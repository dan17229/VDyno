"""
VDyno - A PyQT based GUI for the V-Dyno project.

style_sheet.py is used to set the style of the GUI.

written by:
    - Daniel Muir

"""

StyleSheet = """
    QWidget{
        background-color: #FFFFFF; /* background for main window */
        color: #000000; /* text color */
    }

    QMainWindow {
        background-color: #FFFFFF; /* background for main window */
    }

    QMenuBar {
        background-color: #FFFFFF; /* background for menu bar */
        color: #000000; /* text color */
    }

    QMenuBar::item {
        background-color: #FFFFFF; /* background for menu bar items */
        color: #000000; /* text color */
    }

    QMenuBar::item:selected {
        background-color: #E1E1E1; /* background for selected menu bar items */
    }

    QToolBox:tab { /* Style for tabs in QToolBox */
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border-radius: 5px;
        color: #777C80;
    }

    QToolBox:tab:selected { /* Style for tabs when selected */
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0 #58BEA8 stop: 1.0 #323587);
        color: #FFFFFF;
    }

    QTabWidget:pane{ /* The tab widget frame */
        border-top: 0px; /* width of 0 pixels */
    }

    QTabBar:tab{ /* Style the tab using tab sub-control and QTabBar */
        /* Add gradient look to the colors of each tab */
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                        stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
        border: 2px solid #C4C4C3;
        border-bottom-color: #C2C7CB;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 8ex;
        padding: 2px;
        color: #000000; /* text color */
    }

    QTabBar:tab:selected, QTabBar:tab:hover { 
        /* Use same color scheme for selected tab, and other tabs when the user 
        hovers over them */
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #FAFAFA, stop: 0.4 #F4F4F4,
                        stop: 0.5 #E7E7E7, stop: 1.0 #FAFAFA);
        color: #000000; /* text color */
    }

    QTabBar:tab:selected {
        border-color: #9B9B9B;
        border-bottom-color: #C2C7CB; /* Same as pane color */
    }

    QTabBar:tab:!selected {
        margin-top: 2px; /* Make non-selected tabs look smaller when not selected */
    }

    QToolBar {
        background: #D3D3D3; /* Grey background for tool bar */
        border: none;
    }

    QToolButton {
        border: 1px solid #000000; /* Black border for tool buttons */
        border-radius: 4px;
    }

    QWidget#CustomSpacer {
        background-color: #D3D3D3;
        border: none;
    }

    QWidget#ShortBreak{ /* Short break tab container widget */
        background-color: #398AB5;
        border: 1px solid #398AB5;
        border-radius: 4px;
        color: #000000; /* text color */
    }

    QWidget#LongBreak{ /* Long break tab container widget */
        background-color: #55A992;
        border: 1px solid #55A992;
        border-radius: 4px;
        color: #000000; /* text color */
    }

    QPushButton{ /* General look of QPushButtons */
        background-color: #E1E1E1;
        border: 2px solid #C4C4C3;
        border-radius: 4px;
        color: #000000; /* text color */
    }

    QPushButton:hover{
        background-color: #F8F4F4;
    }

    QPushButton:pressed{
        background-color: #E9E9E9;
        border: 2px solid #C4C4C3;
        border-radius: 4px;
    }

    QPushButton:disabled{
        background-color: #D8D3D3;
        border: 2px solid #C4C4C3;
        border-radius: 4px;
    }

    QGroupBox{ /* Style for Pomodoro task bar */
        background-color: #EF635C;
        border: 2px solid #EF635C;
        border-radius: 4px;
        margin-top: 3ex;
        color: #000000; /* text color */
    }

    QGroupBox:title{
        subcontrol-origin: margin;
        padding: 2px;
        color: #000000; /* text color */
    }

    QLineEdit{
        background-color: #FFFFFF;
        color: #000000; /* text color */
    }

    QLabel{
        background-color: #FFFFFF;
        color: #000000; /* text color */
    }

    /* Style for GraphicsLayoutWidget and PlotItem */
    QGraphicsView {
        background-color: #FFFFFF; /* background for plots */
    }

    .pg-PlotItem {
        background-color: #FFFFFF; /* background for plot items */
    }
"""
