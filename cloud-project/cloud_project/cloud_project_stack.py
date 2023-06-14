from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2
from constructs import Construct

class CloudProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Check if S3 bucket exists
        existing_bucket = s3.Bucket.from_bucket_name(
            self,
            "ExistingBucket",
            bucket_name="cloud10-project-bucket"
        )

        # Create S3 bucket if it doesn't exist
        if existing_bucket is None:
            # Create S3 bucket
            bucket = s3.Bucket(
                self,
                "CloudProjectBucket",
                bucket_name="cloud10-project-bucket"
            )

            # Set bucket region
            bucket.bucket_region = "eu-central-1"

        else:
            print("S3 bucket already exists. Skipping bucket creation.")

        vpc = ec2.Vpc(self, "Cloud10VPC",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", cidr_mask=24, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
            ],
            nat_gateways=1,
        )