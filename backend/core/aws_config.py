import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, Dict, Any
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSConfig:
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.sagemaker_client = None
        self.s3_client = None
        self.dynamodb_client = None
        self.lambda_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AWS clients with proper error handling"""
        try:
            # Initialize SageMaker client
            self.sagemaker_client = boto3.client(
                'sagemaker',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            # Initialize S3 client
            self.s3_client = boto3.client(
                's3',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            # Initialize DynamoDB client
            self.dynamodb_client = boto3.client(
                'dynamodb',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            # Initialize Lambda client
            self.lambda_client = boto3.client(
                'lambda',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            logger.info("AWS clients initialized successfully")
            
        except NoCredentialsError:
            logger.error("AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """Test AWS connection by making a simple API call"""
        try:
            # Test S3 connection
            self.s3_client.list_buckets()
            logger.info("AWS connection test successful")
            return True
        except Exception as e:
            logger.error(f"AWS connection test failed: {str(e)}")
            return False
    
    def get_sagemaker_endpoints(self) -> list:
        """Get list of available SageMaker endpoints"""
        try:
            response = self.sagemaker_client.list_endpoints()
            return response.get('Endpoints', [])
        except ClientError as e:
            logger.error(f"Failed to get SageMaker endpoints: {str(e)}")
            return []
    
    def invoke_sagemaker_endpoint(self, endpoint_name: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Invoke a SageMaker endpoint"""
        try:
            runtime_client = boto3.client(
                'sagemaker-runtime',
                region_name=self.region,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            response = runtime_client.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            return json.loads(response['Body'].read().decode())
        except ClientError as e:
            logger.error(f"Failed to invoke SageMaker endpoint {endpoint_name}: {str(e)}")
            return None
    
    def upload_to_s3(self, bucket_name: str, key: str, data: str) -> bool:
        """Upload data to S3 bucket"""
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=data.encode('utf-8'),
                ContentType='application/json'
            )
            logger.info(f"Successfully uploaded {key} to S3 bucket {bucket_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {str(e)}")
            return False
    
    def get_from_s3(self, bucket_name: str, key: str) -> Optional[str]:
        """Get data from S3 bucket"""
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            logger.error(f"Failed to get from S3: {str(e)}")
            return None
    
    def store_in_dynamodb(self, table_name: str, item: Dict[str, Any]) -> bool:
        """Store item in DynamoDB table"""
        try:
            self.dynamodb_client.put_item(
                TableName=table_name,
                Item=item
            )
            logger.info(f"Successfully stored item in DynamoDB table {table_name}")
            return True
        except ClientError as e:
            logger.error(f"Failed to store in DynamoDB: {str(e)}")
            return False
    
    def get_from_dynamodb(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get item from DynamoDB table"""
        try:
            response = self.dynamodb_client.get_item(
                TableName=table_name,
                Key=key
            )
            return response.get('Item')
        except ClientError as e:
            logger.error(f"Failed to get from DynamoDB: {str(e)}")
            return None
    
    def invoke_lambda_function(self, function_name: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Invoke AWS Lambda function"""
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            return json.loads(response['Payload'].read().decode())
        except ClientError as e:
            logger.error(f"Failed to invoke Lambda function {function_name}: {str(e)}")
            return None

# Global AWS configuration instance
aws_config = AWSConfig() 