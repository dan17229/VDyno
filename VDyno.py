"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code is the entry point, initialising the model, view, and presenter components- the architecture is based on the Model-View-Presenter (MVP) pattern.

===========================================================
If testing without CAN tranceiver, switch can_handler.py to dummy_can_handler.py in VDyno/model/dyno.py.
If you are using different hardware, you will need to modify the model/value_calibration.csv file to suit your needs. Values go factor, offset.
If using Apple or Linux device, 
============================================================

written by:
    - Daniel Muir
"""

from VDyno.view.main_window import create_UI
from VDyno.presenter.data_handler import Presenter
from VDyno.model.dyno import Dyno


def main() -> None:
    view, app = create_UI()
    model = Dyno()
    presenter = Presenter(model, view, app)
    presenter.run()

if __name__ == "__main__":
    main()
