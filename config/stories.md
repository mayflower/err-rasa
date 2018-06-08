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

## Story Report Illness from-to
* report_illness_from_to
    - action_report_illness_from_to

## Story Report Illness duration
* report_illness_duration{"duration": "None"}
    - utter_get_report_illness_duration_duration
* report_illness_duration
    - action_report_illness_duration