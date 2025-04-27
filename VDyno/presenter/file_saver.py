"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code contains the FileSaver class, which is used to save data from each of the motors and the torque transducer (file type: dict) into a .csv file.
Results are stored in data_output/results, with the filename being the date and time of creation.

written by:
    - Daniel Muir
"""

import csv
from datetime import datetime
import os
from time import sleep

class FileSaver:
    def __init__(self, parent):
        self.parent = parent
        self.MUT_data = parent.MUT.status
        self.load_data = parent.load_motor.status
        self.TT_data = parent.torque_transducer.status

    def open(self):
        """
        Create a .csv file with the current date and time as the name and prepare it for recording.
        """
        # Ensure the folder exists
        folder_path = "experimental_results"
        os.makedirs(folder_path, exist_ok=True)

        # Create the file in the specified folder
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.csv")
        file_path = os.path.join(folder_path, filename)
        self.file = open(file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        
        # Write the header row (keys from all dictionaries)
        headers = list(self.MUT_data.keys()) + list(self.load_data.keys()) + list(self.TT_data.keys())
        self.writer.writerow(headers)

    def record(self, stop:bool=False):
        """
        Write the current state of the three dictionaries to the file as a new line.
        """
        if stop:
                print("Stopping recording...")
                return  # Exit the method if stop is True
        
        self.MUT_data = self.parent.MUT.status
        self.load_data = self.parent.load_motor.status
        self.TT_data = self.parent.torque_transducer.status
        if not self.writer:
            raise ValueError("File is not open. Call 'open' before recording.")
        
        # Write only the values from the dictionaries
        row = list(self.MUT_data.values()) + list(self.load_data.values()) + list(self.TT_data.values())
        self.writer.writerow(row)
        sleep(1/40)

    def close(self):
        """
        Close the .csv file.
        """
        print("Closing file...")
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None

if __name__ == "__main__":

    class DummyMotor:
        def __init__(self):
            self.status = {
                "Status_RPM": 0,
                "Status_TotalCurrent": 0,
                "Status_DutyCycle": 0,
            }
    class DummyParent:
        def __init__(self):
            self.MUT = DummyMotor()
            self.load_motor = DummyMotor()
            self.torque_transducer = DummyMotor()

    # Create an instance of FileSaver
    example = DummyParent()
    file_saver = FileSaver(example)

    # Open the file (creates a .csv file with headers in the specified folder)
    file_saver.open()

    # Record the current state of the dictionaries (writes values as a row)
    file_saver.record()

    # Modify the dictionaries to simulate new data
    example.MUT.status["Status_RPM"] = 500000

    # Record the updated state of the dictionaries
    file_saver.record()

    # Close the file
    file_saver.close()

