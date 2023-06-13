from aws_cdk import (
    Stack,
    aws_ec2 as ec2
)
from constructs import Construct

class CloudProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC for Web Server
        web_server_vpc = ec2.Vpc(
            self, 
            "WebServerVPC",
            cidr="10.10.10.0/24",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet1", 
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=25
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnet2", 
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=25
                )
            ],
            availability_zones=['eu-central-1a', 'eu-central-1b']
        )

        # VPC for Management Server
        management_server_vpc = ec2.Vpc(
            self, 
            "ManagementServerVPC",
            cidr="10.20.20.0/24",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet1", 
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=25
                ),
                ec2.SubnetConfiguration(
                    name="PublicSubnet2", 
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=25
                )
            ],
            availability_zones=['eu-central-1a', 'eu-central-1b']
        )

        # Transit Gateway
        transit_gateway = ec2.CfnTransitGateway(
            self,
            "TransitGateway",
            default_route_table_association="true",
            default_route_table_propagation="true",
            description="My Transit Gateway"
        )

        # Attach VPCs to Transit Gateway
        web_server_attachment = ec2.CfnTransitGatewayAttachment(
            self,
            "WebServerVPCAttachment",
            transit_gateway_id=transit_gateway.ref,
            vpc_id=web_server_vpc.vpc_id,
            subnet_ids=[web_server_vpc.select_subnets(subnet_name="PublicSubnet1", one_per_az=True).subnet_ids[0],
                        web_server_vpc.select_subnets(subnet_name="PublicSubnet2", one_per_az=True).subnet_ids[0]]
        )

        management_server_attachment = ec2.CfnTransitGatewayAttachment(
            self,
            "ManagementServerVPCAttachment",
            transit_gateway_id=transit_gateway.ref,
            vpc_id=management_server_vpc.vpc_id,
            subnet_ids=[management_server_vpc.select_subnets(subnet_name="PublicSubnet1", one_per_az=True).subnet_ids[0],
                        management_server_vpc.select_subnets(subnet_name="PublicSubnet2", one_per_az=True).subnet_ids[0]]
        )

        # Associate each attachment with the Transit Gateway's default route table
        ec2.CfnTransitGatewayRouteTablePropagation(
            self,
            "WebServerVPCTGAttachmentPropagation",
            transit_gateway_route_table_id=transit_gateway.attr_default_route_table_id,
            transit_gateway_attachment_id=web_server_attachment.ref
        )

        ec2.CfnTransitGatewayRouteTableAssociation(
            self,
            "WebServerVPCTGAttachmentAssociation",
            transit_gateway_route_table_id=transit_gateway.attr_default_route_table_id,
            transit_gateway_attachment_id=web_server_attachment.ref
        )

        ec2.CfnTransitGatewayRouteTablePropagation(
            self,
            "ManagementServerVPCTGAttachmentPropagation",
            transit_gateway_route_table_id=transit_gateway.attr_default_route_table_id,
            transit_gateway_attachment_id=management_server_attachment.ref
        )

        ec2.CfnTransitGatewayRouteTableAssociation(
            self,
            "ManagementServerVPCTGAttachmentAssociation",
            transit_gateway_route_table_id=transit_gateway.attr_default_route_table_id,
            transit_gateway_attachment_id=management_server_attachment.ref
        )
