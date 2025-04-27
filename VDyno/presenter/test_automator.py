"""
VDyno - A PyQT based GUI for the V-Dyno project.

This code contains the TestAutomator class, which reads a JSON file containing the experiment steps and executes them using the ExperimentWorker class.
The idea is to allow for easy definition of experiment steps without code changes. Ideally JSON files could one day be made via GUI. JSON files are stored in VDyno/experiments.
JSON was chosen because I like it, can easily be replaced if required.

written by:
    - Daniel Muir
"""

import json
from time import sleep
from typing import Protocol

if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class MainWindow(Protocol): ...


class ExperimentWorker:
    def __init__(self, parent: MainWindow, steps: list) -> None:
        super().__init__()
        self.parent = parent
        self.steps = steps
        self.running = True

    def execute_step(self, step: dict) -> None:
        """Execute a single step for both motors."""
        self.mut_property = step["MUT"]["property"]
        self.load_property = step["load_motor"]["property"]
        self.duration = step["duration"]

        if step["action"] == "ramp":
            self.mut_start = step["MUT"]["start"]
            self.mut_end = step["MUT"]["end"]
            self.load_start = step["load_motor"]["start"]
            self.load_end = step["load_motor"]["end"]
            self.ramp()
        elif step["action"] == "hold":
            self.mut_start = step["MUT"]["value"]
            self.load_start = step["load_motor"]["value"]
            self.hold()

    def ramp(self) -> None:
        """Ramp both motors' properties simultaneously."""
        steps = 100
        step_duration = self.duration / steps
        mut_step_size = (self.mut_end - self.mut_start) / steps
        load_step_size = (self.load_end - self.load_start) / steps

        mut_current_value = self.mut_start
        load_current_value = self.load_start
        for _ in range(steps):
            if not self.running:
                return
            if self.mut_property == "current":
                self.parent.change_MUT_current(float(mut_current_value))
            if self.load_property == "rpm":
                self.parent.change_load_rpm(int(load_current_value))
            mut_current_value += mut_step_size
            load_current_value += load_step_size
            sleep(step_duration)

    def hold(self) -> None:
        """Hold both motors' properties at specific values."""
        if not self.running:
            return
        if self.mut_property == "current":
            self.parent.change_MUT_current(self.mut_start)
        if self.load_property == "rpm":
            self.parent.change_load_rpm(self.load_start)
        sleep(self.duration)

    def run(self) -> None:
        """Run the experiment steps."""
        print("Experiment started")
        for step in self.steps:
            print(f"Executing step: {step}")
            if not self.running:
                break
            self.execute_step(step)
        self.parent.change_MUT_current(0)
        self.parent.change_load_rpm(0)
        print("Experiment stopped or completed.")


class TestAutomator:
    def __init__(self, parent: MainWindow, stop=False) -> None:
        self.parent = parent

    def start_experiment(self, experiment_file: str) -> None:
        """Execute an experiment defined in a JSON file."""
        with open(experiment_file, "r") as file:
            experiment = json.load(file)

        steps = experiment["steps"]
        self.worker = ExperimentWorker(self.parent, steps)
        self.worker.run()
        return

    def _on_experiment_finished(self):
        """Handle experiment completion."""
        print("Experiment finished successfully.")

    def _on_experiment_error(self, error_message: str):
        """Handle experiment errors."""
        print(f"Experiment failed with error: {error_message}")

    def stop_experiment(self) -> None:
        """Stop the experiment."""
        print("Stopping experiment...")
        self.worker.running = False


if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

    class DummyDyno:
        def change_MUT_current(self, value: float) -> None:
            ...
            # print(f"Setting MUT current to {value}")

        def change_load_rpm(self, value: int) -> None:
            ...
            # print(f"Setting load motor RPM to {value}")

    dyno = DummyDyno()
    automator = TestAutomator(dyno)

    # Example: Execute an experiment from a JSON file
    automator.start_experiment("VDyno/experiments/ramp.json")
