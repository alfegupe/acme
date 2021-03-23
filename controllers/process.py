import os

from flask import json

from managers.step import StepManager
from managers.balance import BalanceManager


class ProcessController:

    def __init__(self):
        self.data = None
        self.step_manager = StepManager()
        self.balance_manager = BalanceManager()
        self.log = ""

    def _validate_and_load_json_file(self, json_file_url):
        """
        Validate the json file and load its content.
        :param json_file_url: str, the URL where the json file was uploaded.
        :return: Dict with the data loaded or None if the file has errors or is empty.
        """
        try:
            with open(json_file_url) as test_file:
                self.data = json.load(test_file)
                if self.data:
                    self.log += "Json data was loaded successfully."
                    return self.data

                self.log += "Json file is empty."
                return None

        except Exception as e:
            self.log += "\n\nError while processing json file. Error: {}".format(e)
            return None

    def read_file_and_process(self, json_url):
        if self._validate_and_load_json_file(json_file_url=json_url):
            self._process()
        return self.log

    def _process(self):
        """
        Store the steps from json file and call one to one to process it.
        :return: str, the output log.
        """
        try:
            if self.data.get('steps') and self.data.get('trigger'):
                # Save steps
                inserted_steps = self.step_manager.insert_many(self.data['steps'])

                # Get trigger event
                trigger = self.data['trigger']
                self.step_manager.insert_one(trigger)
                process_result = self._process_step(trigger['id'])

                # Clear Step collection for tests proposal.
                self.step_manager.clear_collection()

                return self.log

            return "No Steps or trigger configured in json file."

        except Exception as e:
            self.log += "\n\nThere was an error during the process. Error: {}".format(e)

    def _process_step(self, step_id):
        """
        Recursive function to manage every step according to the step_id.
        :param step_id: str, the id of the step to process.
        :return: Bool, when the process be finished.
        """
        try:
            target = None
            current_step = self.step_manager.get_by_id(step_id=step_id)
            self.log += "\n\n  *  Processing step:  ID: {},  Action: {}.".format(
                step_id, current_step.get('action', "--"))

            # Perform action
            if current_step.get('action'):
                self._manage_action(action=current_step['action'])

            transitions = current_step.get('transitions')
            if transitions:
                self.log += "\n({}) Transitions.".format(len(transitions))
                transitions_counter = 1
                for transition in transitions:
                    self.log += "\n - Transition #{}:".format(transitions_counter)
                    transitions_counter += 1

                    if transition.get('condition'):
                        # Manage condition here.
                        self.log += "\nConditions: {}".format(transition['condition'])
                    else:
                        self.log += "\nNo conditions."

                    if transition.get('target'):
                        self.log += "\nTarget: {}".format(transition['target'])
                        target = transition['target']
                    else:
                        self.log += "\nNo target."

            self.log += "\nEnd process step {}.".format(step_id)

            if target:
                return self._process_step(step_id=target)

            return True

        except Exception as e:
            self.log += "\n\nError while processing step with id: {}. Error: {}".format(step_id, e)
            return None

    def _manage_action(self, action):
        """
        Manage the action to perform by step.
        :param action: str, the action name.
        :return: str, the operation result
        """
        try:
            self.log += "\n -  Doing action: {}".format(action)
            return True

        except Exception as e:
            self.log += "\n\nError while processing action: {}. Error: {}".format(action, e)
