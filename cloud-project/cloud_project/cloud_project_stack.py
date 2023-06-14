from aws_cdk import Stack, aws_s3 as s3
from constructs import Construct

class CloudProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(
            self,
            "CloudProjectBucket",
            bucket_name="cloud10-project-bucket"
        )

        # Set bucket region
        bucket.bucket_region = "eu-central-1"
