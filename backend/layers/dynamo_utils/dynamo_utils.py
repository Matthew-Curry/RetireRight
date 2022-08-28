"""Utility classes and methods to interact with dynamodb"""

import logging
import boto3
from botocore.config import Config

logger = logging.getLogger()

class UnableToStartSession(BaseException):
    def __init__(self):
        super().__init__("Unable to start the DynamoDB session.")

class DynamoResourceCache:

    def __init__(self):
        logger.info("Initializing Dynamo resources to None")
        self.dynamodb = None
        self.table = None
        # the configuration to use in establishing new sessions
        self.config = Config(
                        connect_timeout = 1,
                        read_timeout =1
                    )

    def get_db_resources(self) -> tuple:
        """Helper method to return DynamoDB service and user table resources. Checks if resources are cached from a 
        warm start, else creates new resources, then returns them.
        raises: 
            UnableToStartSession: if either the service or table resource cannot be instantiated
        returns:
            tuple of the resources in form (service, table) """
      
        if self.dynamodb is None or self.table is None:
            logger.info("Not able to find both Dynamo resources. Creating new ones..")
            try:
                self.dynamodb = boto3.resource('dynamodb', config = self.config)
                self.table = self.dynamodb.Table('users')
            except Exception as e:
                raise UnableToStartSession
            logger.info("Successfully created DynamoDB resources")
        else:
            logger.info("Returning cached DynamoDB resources.")
        
        return self.dynamodb, self.table

# instantiation of cache lambda handlers will import to initialize the resource cache
dynamo_resource_cache = DynamoResourceCache()

def get_dynamo_update_params(fields:dict) -> tuple:
    """helper method to return DynamoDB update expression and expression values for the given fields
    args:
        fields (dict): dictionary mapping fields to update to values
    returns:
        tuple in form (string, dictionary) for the update expression and values in matching order."""
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
