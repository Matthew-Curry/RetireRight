"""Utility methods to interact with dynamodb"""

def get_dynamo_update_params(fields:dict) ->tuple:
    """helper method to return DynamoDB update expression and expression values for the given fields
    args:
        fields (dict): dictionary mapping fields to update to values
    returns:
        tuple in form string, dictionary for the update expression and values in matching order."""
    update_exp = 'SET '
    expression_vals = {}
    for i, k in enumerate(fields.keys()):
        # append to the update expression
        if i == len(fields.keys()) -1:
            update_exp = update_exp + f'{k}=:val{i + 1}'
        else:
            update_exp = update_exp + f'{k}=:val{i + 1} ,'
        
        # append to the values
        expression_vals[f':val{i + 1}'] = fields[k]
    
    return update_exp, expression_vals
