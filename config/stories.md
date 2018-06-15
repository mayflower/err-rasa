## Story greet 
* greet
   - utter_greet
> say_hello

## Story for goodby
* goodby
    - utter_goodby
> say_goodby

## Story User asks for something
* who_knows_topic
    - action_who_knows_topic

## Story User claims to know something in a specific category
* claim_to_know_topic_in_category
    - action_claim_to_know_topic

## Story user claims to know a topic
* claim_to_know_topic
    - action_claim_to_know_topic

## Story user asks for topics in category
* topics_in_category
    - action_topics_in_category

## Story user forgot skills
* forgott_topic
    - action_forgotten

## Story Report Illness  with from to values
* report_illness_from_to
    - action_pre_report_illness
* report_illness_from_to{"confirmation_required": "True"}dddddddddddddddddd
    - action_confirmation
> check_confirmation_for_issue_creation_from_to

## Story accept issue creation for from-to situation
> check_confirmation_for_issue_creation_from_to
* report_illness_from_to{"confirmation": "confirmation_accepted"}
    - action_report_illness
> check_auth_confirmation_for_issue_creation_from_to

## Story decline issue creation for from-to situation
> check_confirmation_for_issue_creation_from_to
* report_illness_from_to{"confirmation": "confirmation_declined"}
    - utter_goodby

## Story accecepted auth request
> check_auth_confirmation_for_issue_creation_from_to
* report_illness_from_to{"auth_confirmation": "auth_confirmed"}
    - action_report_illness
* report_illness_from_to{"auth_required": "True"}
    - action_confirmation

## Story declined auth request
> check_auth_confirmation_for_issue_creation_from_to
* report_illness_from_to{"auth_confirmation": "auth_declined"}
    - utter_goodby


## Story Report Illness duration
* report_illness_duration
    - action_pre_report_illness
* report_illness_duration{"confirmation_required": "True"}
    - action_confirmation
    - action_listen
> check_confirmation_for_issue_creation_duration

## Story accept issue creation for duration
> check_confirmation_for_issue_creation_duration
* report_illness_duration{"confirmation": "confirmation_accepted"}
    - action_report_illness
* report_illness_duration{"auth_required": "True"}
    - action_confirmation
    - action_listen
> check_auth_confirmation_for_issue_creation_duration

## Story decline issue creation for duration
> check_confirmation_for_issue_creation_duration
* report_illness_duration{"confirmation": "confirmation_declined"}
    - utter_goodby

## Story accecepted auth request
> check_auth_confirmation_for_issue_creation_duration
* report_illness_duration{"auth_confirmation": "auth_confirmed"}
    - action_report_illness

## Story declined auth request
> check_auth_confirmation_for_issue_creation_duration
* report_illness_duration{"auth_confirmation": "auth_declined"}
    - utter_goodby
