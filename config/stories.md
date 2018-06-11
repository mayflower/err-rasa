## Story greet 
* greet
   - utter_greet

## Story for goodby
* goodby
    - utter_goodby

## Story pedant
* pedant
   - action_pedant

## Story Report Illness with unknown last value
* report_illness_from_to{"last": "None"}
    - utter_get_report_illness_last
* report_illness_from_to
    - action_pre_report_illness
* report_illness_from_to{"confirmed": "False"}
   - utter_get_report_illness_confirmed
* report_illness_from_to
    - action_report_illness

## Story Report Illness  with from to values
* report_illness_from_to{"last": "True"}
    - action_pre_report_illness
* report_illness_from_to{"confirmed": "False"}
   - utter_get_report_illness_confirmed
* report_illness_from_to
    - action_report_illness

## Story Report Illness with unknown duration
* report_illness_duration{"duration": "None"}
    - utter_get_report_illness_duration
* report_illness_duration
    - action_pre_report_illness
* report_illness_duration{"confirmed": "False"}
   - utter_get_report_illness_confirmed
* report_illness_duration
    - action_report_illness

## Story Report Illness duration
* report_illness_duration{"duration": "True"}
    - action_pre_report_illness
* report_illness_duration{"confirmed": "False"}
   - utter_get_report_illness_confirmed
* report_illness_duration
    - action_report_illness
