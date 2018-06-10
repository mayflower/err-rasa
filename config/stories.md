## Story greet 
* greet
   - utter_greet

## Story for goodby
* goodby
    - utter_goodby

## Story pedant
* pedant
   - action_pedant

## Story order_pizza
* order_pizza
   - utter_get_pizza_size
* order_pizza
   - utter_get_pizza_toppings
* order_pizza
   - action_order_pizza

## Story Report Illness From To
* report_illness_from_to{"confirmed": "None"}
    - action_pre_report_illness_from_to
    - utter_get_report_illness_confirmed
    - action_pre_report_illness_from_to
* report_illness_from_to{"confirmed": "True"}
    - action_pre_report_illness_from_to

## Story Report Illness duration
* report_illness_duration
    - utter_get_report_illness_duration_duration
* report_illness_duration
    - action_report_illness_duration