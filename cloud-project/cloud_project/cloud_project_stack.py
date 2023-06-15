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

        # Create the web server VPC
        vpc = ec2.Vpc(self, "Cloud10VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.10.10.0/24"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", cidr_mask=26, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="private", cidr_mask=26, subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
            ],
            enable_dns_support=True,
            enable_dns_hostnames=True,
            nat_gateways=1,
            )

        # Create the management server VPC
        vpc_manage = ec2.Vpc(self, "Cloud10VPCManage",
            ip_addresses=ec2.IpAddresses.cidr("10.20.20.0/24"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", cidr_mask=26, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="private", cidr_mask=26, subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
            ],
            enable_dns_support=True,
            enable_dns_hostnames=True,
            nat_gateways=1,
        )
# Create Transit Gateway
        tgw = ec2.CfnTransitGateway(self, "Cloud10TransitGateway",
            amazon_side_asn=65000,  # Using your provided ASN
            auto_accept_shared_attachments="enable",
            default_route_table_association="enable",
            default_route_table_propagation="enable",
            description="Cloud10 Transit Gateway",
            dns_support="enable",
            vpn_ecmp_support="enable",
        )

        # Attach both VPCs to Transit Gateway
        tgw_attachment1 = ec2.CfnTransitGatewayAttachment(self, "Cloud10VPCAttachment",
            subnet_ids=[vpc.public_subnets[0].subnet_id],
            transit_gateway_id=tgw.ref,
            vpc_id=vpc.vpc_id
        )

        tgw_attachment2 = ec2.CfnTransitGatewayAttachment(self, "Cloud10VPCManageAttachment",
            subnet_ids=[vpc_manage.public_subnets[0].subnet_id],
            transit_gateway_id=tgw.ref,
            vpc_id=vpc_manage.vpc_id
        )

        # Create route tables and associate them with VPCs
        tgw_route_table = ec2.CfnTransitGatewayRouteTable(self, "Cloud10TransitGatewayRouteTable",
            transit_gateway_id=tgw.ref
        )

        for i, attachment in enumerate([tgw_attachment1, tgw_attachment2]):
            ec2.CfnTransitGatewayRouteTableAssociation(self, f"Cloud10VPCAssociation{i}",
                transit_gateway_attachment_id=attachment.ref,
                transit_gateway_route_table_id=tgw_route_table.ref
            )

            ec2.CfnTransitGatewayRouteTablePropagation(self, f"Cloud10VPCPropagation{i}",
                transit_gateway_attachment_id=attachment.ref,
                transit_gateway_route_table_id=tgw_route_table.ref
            )