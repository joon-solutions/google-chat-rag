EVALUATOR_AGENT_INSTR="""
Given the original query from the user : {original_user_message}

And the following response :
{merger_agent}

Determine if the answer is sufficient.
If it is not sufficient, use memorize tool and act as 
a user to set a new query more suitable for "user_message", inferring from original user message : 
{original_user_message}.
Else use the tool exit_loop to mark your job done.


"""