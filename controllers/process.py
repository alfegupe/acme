
from flask import json

from managers.step import StepManager
from managers.account import AccountBalanceManager


class ProcessController:

    def __init__(self):
        self.data = None
        self.step_manager = StepManager()
        self.account_balance_manager = AccountBalanceManager()
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
        """
        Read the json file from the given url and then start the process.
        :param json_url: str, the url of the json file.
        :return: str, the result log.
        """
        if self._validate_and_load_json_file(json_file_url=json_url):
            self._process()
        return self.log

    def _initialize_account(self, account_params):
        """
        Init the account information for the user.
        :param account_params: dict, the user_id and pin information to create the account.
        :return: bool, the process result.
        """
        try:
            if account_params and 'user_id' in account_params and 'pin' in account_params:
                self.account_balance_manager.create_account(
                    user_id=account_params['user_id'],
                    pin=account_params['pin'],
                )
                self.log += "\n Account has been created for the user with ID: {}".format(
                    account_params['user_id'])
                return True

            self.log += "\n\n Account creation error, missing information."
            return False

        except Exception as e:
            self.log += "\n\nThere was an error during the account creation. Error: {}".format(e)

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
                if self._initialize_account(trigger.get('params')):
                    self._process_step(trigger['id'])

                # Clear collections for testing.
                self.step_manager.clear_collection()
                self.account_balance_manager.clear_collection()

                return self.log

            return "No Steps or trigger configured in json file."

        except Exception as e:
            self.log += "\n\nThere was an error during the process. Error: {}".format(e)

    def _process_step(self, step_id, condition=None):
        """
        Recursive function to manage every step according to the step_id.
        :param step_id: str, the id of the step to process.
        :return: Bool, when the process be finished.
        """
        try:
            current_step = self.step_manager.get_by_id(step_id=step_id)
            self.log += "\n\n  ***  Processing step with ID: {} ***".format(step_id)

            # Perform action
            if current_step.get('action'):
                if condition:
                    self.log += "\n -- Validating condition: {}".format(condition)

                result_step_action = self._manage_action(
                    action=current_step['action'],
                    params=current_step.get('params'),
                    condition=condition
                )
                self.log += "\n - Action result: {}".format(result_step_action)
                if condition:
                    return result_step_action

            transitions = current_step.get('transitions')
            if transitions:
                transitions_counter = 1
                for transition in transitions:
                    self.log += "\n\n - Transition ({}/{}):".format(transitions_counter, len(transitions))
                    transitions_counter += 1
                    valid_conditions = True
                    if transition.get('condition'):
                        self.log += "\n\n Conditions:"
                        for condition in transition['condition']:
                            condition_result = self._process_step(
                                step_id=condition.get('from_id'),
                                condition=condition
                            )
                            self.log += "\n - Condition result: {}".format(condition_result)
                            if condition_result is None:
                                valid_conditions = False
                    else:
                        self.log += "\n  No conditions."

                    if transition.get('target') and valid_conditions:
                        self.log += "\n - Target: {}".format(transition['target'])
                        return self._process_step(step_id=transition['target'])
                    else:
                        self.log += "\n  No target or invalid condition."

            self.log += "\nEnd process step {}.".format(step_id)

            return True

        except Exception as e:
            self.log += "\n\nError while processing step with id: {}. Error: {}".format(step_id, e)
            return None

    def _manage_action(self, action, params, condition):
        """
        Manage the action to perform by step.
        :param action: str, the action name.
        :return: str, the operation result
        """
        try:
            self.log += "\n -  Doing action: {}".format(action)
            function_params, cond = {}, {}

            if condition:
                function_params[condition['field_id']] = {
                    "${}".format(condition['operator']): condition['value']
                }

            if params:
                for param, data in params.items():
                    function_params[param] = self._get_param_value_from_step_id(
                        step_id=data.get('from_id'),
                        param_value=data.get('param_id')
                    ) if data.get('from_id') else data.get('value')

                self.log += "\n - Parameters: {}".format(function_params)

            action_to_perform = getattr(self.account_balance_manager, action)
            action_result = action_to_perform(function_params)
            return action_result

        except Exception as e:
            self.log += "\n\nError while processing action: {}. Error: {}".format(action, e)

    def _get_param_value_from_step_id(self, step_id, param_value):
        """
        Load parameters from given step.
        :param step_id: str, the step id to load.
        :param param_value: str, the param to load.
        :return: param value.
        """
        step = self.step_manager.get_by_id(step_id=step_id)
        if step and 'params' in step and param_value in step['params']:
            return step['params'][param_value]

        return None
