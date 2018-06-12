## Story greet 
* greet
   - utter_greet

## Story for goodby
* goodby
    - utter_goodby

## Story pedant
* pedant
   - action_pedant

## Story Report Illness  with from to values
* report_illness_from_to
    - action_pre_report_illness
    - utter_get_report_illness_confirmation
* report_illness_from_to{"confirmation": "confirmation_accepted"}
    - action_report_illness
* report_illness_from_to{"confirmation": "confirmation_declined"}
    - utter_goodby
* report_illness_from_to{"auth_required": "True"}
    - utter_get_report_illness_auth_confirmation
* report_illness_from_to{"auth_confirmed": "auth_accepted"}
    - action_report_illness
* report_illness_from_to{"auth_confirmed": "auth_declined"}
    - utter_goodby

## Story Report Illness duration
* report_illness_duration
    - action_pre_report_illness
    - utter_get_report_illness_confirmation
* report_illness_duration{"confirmation": "confirmation_accepted"}
    - action_report_illness
* report_illness_duration{"confirmation": "confirmation_declined"}
    - utter_goodby
* report_illness_duration{"auth_required": "True"}
    - utter_get_report_illness_auth_confirmation
* report_illness_duration{"auth_confirmation": "auth_confirmed"}
    - action_report_illness
* report_illness_duration{"auth_confirmation": "auth_declined"}
    - utter_goodby