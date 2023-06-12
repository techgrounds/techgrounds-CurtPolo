from aws_cdk import (
    aws_ec2 as ec2,
    core,
)

class FinalProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_vpc = ec2.Vpc(
            self,
            "WebVPC",
            cidr="10.10.10.0/24",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnetAZ-A",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                    reserved=False,
                    availability_zone="eu-central-1a"
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnetAZ-B",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                    reserved=False,
                    availability_zone="eu-central-1b"
                ),
            ]
        )

        management_vpc = ec2.Vpc(
            self,
            "ManagementVPC",
            cidr="10.20.20.0/24",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnetAZ-A",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                    reserved=False,
                    availability_zone="eu-central-1a"
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnetAZ-A",
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24,
                    reserved=False,
                    availability_zone="eu-central-1a"
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnetAZ-B",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                    reserved=False,
                    availability_zone="eu-central-1b"
                ),
            ]
        )

        transit_gateway = ec2.CfnTransitGateway(
            self,
            "TransitGateway",
            description="CDK Example Transit Gateway"
        )

        for vpc in [web_vpc, management_vpc]:
            ec2.CfnTransitGatewayAttachment(
                self,
                f"{vpc.node.id}Attachment",
                transit_gateway_id=transit_gateway.ref,
                vpc_id=vpc.vpc_id,
                subnet_ids=vpc.select_subnets().subnet_ids,
            )

app = core.App()
FinalProjectStack(app, "FinalProjectStack")
app.synth()
