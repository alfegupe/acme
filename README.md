# Acme

This is a small application to test the Flask and MongoDB integration.
There is a little form where you can upload a json file, after you submit the form, the file will be processed.
This application is built in Python3.9.

To run this app you need to install MongoDB:
https://docs.mongodb.com/manual/administration/install-community/

You also need to install Python 3.9 and the libraries in `requirements.txt` file:
> pip3 install -Ur requirements.txt

Or use your custom method, the libraries are:
>Flask==1.1.2  
>Flask-PyMongo==2.3.0

Finally to run the app you can use the command:
>python3 app.py

This is an example of the information you will see in you browser:
```
Json data was loaded successfully.

* Processing step: ID: start, Action: --.
(1) Transitions.
- Transition #1:
No conditions.
Target: validate_account
End process step start.

* Processing step: ID: validate_account, Action: validate_account.
- Doing action: validate_account
(1) Transitions.
- Transition #1:
Conditions: [{'from_id': 'validate_account', 'field_id': 'is_valid', 'operator': 'eq', 'value': True}]
Target: account_balance
End process step validate_account.

* Processing step: ID: account_balance, Action: get_account_balance.
- Doing action: get_account_balance
(2) Transitions.
- Transition #1:
Conditions: [{'from_id': 'account_balance', 'field_id': 'balance', 'operator': 'gt', 'value': 100000}]
Target: withdraw_30
- Transition #2:
Conditions: [{'from_id': 'account_balance', 'field_id': 'balance', 'operator': 'lt', 'value': 100000}]
Target: deposit_200
End process step account_balance.
```
You can find more information about Flask in https://flask.palletsprojects.com/en/1.1.x/