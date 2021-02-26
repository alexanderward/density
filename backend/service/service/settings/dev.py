from service.settings.base import *

DYNAMODB_NAME = {
    'sensor': os.environ['dynamoSensorsTable'],
    "heartbeat":  os.environ['dynamoHeartbeatsTable'],
}
AWS_REGION_NAME = "us-east-1"
