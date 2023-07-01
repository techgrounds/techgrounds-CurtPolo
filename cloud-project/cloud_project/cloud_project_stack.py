from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2, aws_rds as rds, aws_secretsmanager as sm, aws_backup as backup, aws_iam as iam, aws_elasticloadbalancingv2 as elbv2, aws_autoscaling as autoscaling
import aws_cdk
from aws_cdk.aws_ec2 import AmazonLinuxImage, AmazonLinuxGeneration, InstanceClass, InstanceSize, InstanceType, UserData, Peer, Port
from constructs import Construct
import json

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

        
        # Read the user data script file
        with open('user-data.sh', 'r') as file:
            user_data_script = file.read()

        # Create custom UserData from the script
        my_user_data = ec2.UserData.custom(user_data_script)


        # Create the web server VPC
        vpc_web = ec2.Vpc(self, "Cloud10VPC", cidr="10.10.10.0/24",
                        enable_dns_support=True,
                        enable_dns_hostnames=True)

        
        # Create the management server VPC
        vpc_manage = ec2.Vpc(self, "Cloud10VPCManage", cidr="10.20.20.0/24",
                            enable_dns_support=True,
                            enable_dns_hostnames=True)

        
        # Create Transit Gateway
        tgw = ec2.CfnTransitGateway(self, "Cloud10TransitGateway",
            amazon_side_asn=64512,
            auto_accept_shared_attachments="enable",
            default_route_table_association="enable",
            default_route_table_propagation="enable",
            description="Cloud10 Transit Gateway",
            dns_support="enable",
            vpn_ecmp_support="enable",
        )

        # Attach VPCs to the Transit Gateway
        tgw_attachment_vpc = ec2.CfnTransitGatewayAttachment(self, "TgwAttachmentWebVPC",
            transit_gateway_id=tgw.ref,
            vpc_id=vpc_web.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc_web.public_subnets + vpc_web.private_subnets]
        )
        tgw_attachment_vpc.add_depends_on(tgw)  # Add this

        tgw_attachment_vpc_manage = ec2.CfnTransitGatewayAttachment(self, "TgwAttachmentManageVPC",
            transit_gateway_id=tgw.ref,
            vpc_id=vpc_manage.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc_manage.public_subnets + vpc_manage.private_subnets]
        )
        tgw_attachment_vpc_manage.add_depends_on(tgw)  # Add this    


        # Create vpc_web subnets manually
        public_subnet_1 = ec2.CfnSubnet(self, "VPCWebPublicSubnet1",
                                        vpc_id=vpc_web.vpc_id,
                                        cidr_block="10.10.10.0/26",
                                        availability_zone="eu-central-1a"
                                        )

        public_subnet_2 = ec2.CfnSubnet(self, "VPCWebPublicSubnet2",
                                        vpc_id=vpc_web.vpc_id,
                                        cidr_block="10.10.10.64/26",
                                        availability_zone="eu-central-1b"
                                        )
        


        # Create route tables for the vpc web private and public subnets
        route_table_web1 = ec2.CfnRouteTable(self, "VPCWebRouteTable1", vpc_id=vpc_web.vpc_id)
        route_table_web2 = ec2.CfnRouteTable(self, "VPCWebRouteTable2", vpc_id=vpc_web.vpc_id)


        # Associate route table with public subnet 1
        ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation1",
                                            subnet_id=public_subnet_1.ref,
                                            route_table_id=route_table_web1.ref
                                            )

        # Associate route table with public subnet 2
        ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation2",
                                            subnet_id=public_subnet_2.ref,
                                            route_table_id=route_table_web2.ref
                                            )
        
        # Create vpc_web EIP for the NAT gateway
        eip_web = ec2.CfnEIP(self, "WebEIP", domain="vpc")

        # Create NAT Gateway for vpc_web
        nat_gw_web = ec2.CfnNatGateway(self, "NATGatewayWeb",
                                   allocation_id=eip_web.ref,
                                   subnet_id=public_subnet_1.ref
                                   )
        
        # Create vpc_web private subnets manually
        private_subnet_1 = ec2.CfnSubnet(self, "VPCWebPrivateSubnet1",
                                        vpc_id=vpc_web.vpc_id,
                                        cidr_block="10.10.10.128/26",
                                        availability_zone="eu-central-1a"
                                        )

        private_subnet_2 = ec2.CfnSubnet(self, "VPCWebPrivateSubnet2",
                                        vpc_id=vpc_web.vpc_id,
                                        cidr_block="10.10.10.192/26",
                                        availability_zone="eu-central-1b"
                                        )

        # Associate route table with private subnet 1
        ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation3",
                                            subnet_id=private_subnet_1.ref,
                                            route_table_id=route_table_web1.ref
                                            )

        # Associate route table with private subnet 2
        ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation4",
                                            subnet_id=private_subnet_2.ref,
                                            route_table_id=route_table_web1.ref
                                            )
        
        # Create a route to the Transit Gateway in route_table1
        ec2.CfnTransitGatewayRoute(self, "TransitGatewayRouteWeb1",
            transit_gateway_attachment_id=tgw.ref,
            destination_cidr_block="10.20.20.0/24",
            transit_gateway_route_table_id=route_table_web1.ref
        )

        # Create a route to the Transit Gateway in route_table2
        ec2.CfnTransitGatewayRoute(self, "TransitGatewayRouteWeb2",
            transit_gateway_attachment_id=tgw.ref,
            destination_cidr_block="10.20.20.0/24",
            transit_gateway_route_table_id=route_table_web2.ref
        )

        # Create a default vpc web route pointing to the NAT Gateway for non-transit traffic
        ec2.CfnRoute(self, "VPCWebDefaultRoute1", 
                        route_table_id=route_table_web1.ref,
                        destination_cidr_block="0.0.0.0/0", 
                        nat_gateway_id=nat_gw_web.ref
                        )

        ec2.CfnRoute(self, "VPCWebDefaultRoute2", 
                        route_table_id=route_table_web2.ref,
                        destination_cidr_block="0.0.0.0/0", 
                        nat_gateway_id=nat_gw_web.ref
                        )


        
        # Create vpc_manage subnets manually
        public_subnet_1_manage = ec2.CfnSubnet(self, "VPCManagePublicSubnet1",
                                                vpc_id=vpc_manage.vpc_id,
                                                cidr_block="10.20.20.0/26",
                                                availability_zone="eu-central-1a"
                                                )

        public_subnet_2_manage = ec2.CfnSubnet(self, "VPCManagePublicSubnet2",
                                                vpc_id=vpc_manage.vpc_id,
                                                cidr_block="10.20.20.64/26",
                                                availability_zone="eu-central-1b"
                                                )

        # Create route tables for the vpc_manage private and public subnets
        route_table_manage1 = ec2.CfnRouteTable(self, "VPCManageRouteTable1", vpc_id=vpc_manage.vpc_id)
        route_table_manage2 = ec2.CfnRouteTable(self, "VPCManageRouteTable2", vpc_id=vpc_manage.vpc_id)


        # Associate route table with public subnet 1 in vpc_manage
        ec2.CfnSubnetRouteTableAssociation(self, "VPCManageRouteTableAssociation1",
                                            subnet_id=public_subnet_1_manage.ref,
                                            route_table_id=route_table_manage1.ref
                                            )

        # Associate route table with public subnet 2 in management VPC
        ec2.CfnSubnetRouteTableAssociation(self, "SubnetRouteTableAssociation2Manage",
                                            subnet_id=public_subnet_2_manage.ref,
                                            route_table_id=route_table_manage2.ref
                                            )

        
        # Create vpc_manage EIP for the NAT gateway
        eip_manage = ec2.CfnEIP(self, "ManageEIP", domain="vpc")

        # Create NAT Gateway in vpc_manage public subnet 1
        nat_gw_manage = ec2.CfnNatGateway(self, "VPCManageNATGateway",
                                   allocation_id=eip_manage.ref,
                                   subnet_id=public_subnet_1_manage.ref
                                   )
        
        # Create vpc_manage private subnets manually
        private_subnet_1_manage = ec2.CfnSubnet(self, "VPCManagePrivateSubnet1",
                                                vpc_id=vpc_manage.vpc_id,
                                                cidr_block="10.20.20.128/26",
                                                availability_zone="eu-central-1a"
                                                )

        private_subnet_2_manage = ec2.CfnSubnet(self, "VPCManagePrivateSubnet2",
                                                vpc_id=vpc_manage.vpc_id,
                                                cidr_block="10.20.20.192/26",
                                                availability_zone="eu-central-1b"
                                                )

        # Associate route table with private subnet 1 in management VPC
        ec2.CfnSubnetRouteTableAssociation(self, "SubnetRouteTableAssociation1ManagePrivate",
                                            subnet_id=private_subnet_1_manage.ref,
                                            route_table_id=route_table_manage1.ref
                                            )

        # Associate route table with private subnet 2 in management VPC
        ec2.CfnSubnetRouteTableAssociation(self, "SubnetRouteTableAssociation2ManagePrivate",
                                            subnet_id=private_subnet_2_manage.ref,
                                            route_table_id=route_table_manage2.ref
                                            )
        
        # Create a route to the Transit Gateway in route_table_manage1
        ec2.CfnTransitGatewayRoute(self, "TransitGatewayRouteManage1",
            transit_gateway_attachment_id=tgw.ref,
            destination_cidr_block="10.10.10.0/24",
            transit_gateway_route_table_id=route_table_manage1.ref
        )

        # Create a route to the Transit Gateway in route_table_manage2
        ec2.CfnTransitGatewayRoute(self, "TransitGatewayRouteManage2",
            transit_gateway_attachment_id=tgw.ref,
            destination_cidr_block="10.10.10.0/24",
            transit_gateway_route_table_id=route_table_manage2.ref
        )

        # Create a default vpc manage route pointing to the NAT Gateway
        ec2.CfnRoute(self, "VPCManageDefaultRoute1", 
                        route_table_id=route_table_manage1.ref,
                        destination_cidr_block="0.0.0.0/0", 
                        nat_gateway_id=nat_gw_manage.ref
                        )

        ec2.CfnRoute(self, "VPCManageDefaultRoute2", 
                        route_table_id=route_table_manage2.ref,
                        destination_cidr_block="0.0.0.0/0", 
                        nat_gateway_id=nat_gw_manage.ref
                        )


        # Create web server security group
        web_server_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc_web,
            allow_all_outbound=False,
            security_group_name="WebServerSG"
        )

        # Allow inbound HTTP traffic
        web_server_sg.add_ingress_rule(
            Peer.any_ipv4(),
            Port.tcp(80),
            "Allow inbound HTTP traffic"
        )

        # Allow inbound HTTPS traffic
        web_server_sg.add_ingress_rule(
            Peer.any_ipv4(),
            Port.tcp(443),
            "Allow inbound HTTPS traffic"
        )

        # Allow inbound SSH traffic from management server
        web_server_sg.add_ingress_rule(
            Peer.ipv4('10.20.20.0/26'),
            Port.tcp(22),
            "Allow inbound SSH traffic from management server"
        )

        # Allow outbound HTTP traffic
        web_server_sg.add_egress_rule(
            Peer.any_ipv4(),
            Port.tcp(80),
            "Allow outbound HTTP traffic"
        )

        # Allow outbound HTTPS traffic
        web_server_sg.add_egress_rule(
            Peer.any_ipv4(),
            Port.tcp(443),
            "Allow outbound HTTPS traffic"
        )

        # Allow outbound SSH traffic to management server
        web_server_sg.add_egress_rule(
            Peer.ipv4('10.20.20.0/26'),
            Port.tcp(22),
            "Allow outbound SSH traffic to management server"
        )

        # Create management server security group
        management_server_sg = ec2.SecurityGroup(
            self, "ManagementServerSG",
            vpc=vpc_manage,
            allow_all_outbound=False,
            security_group_name="ManagementServerSG"
        )

        # Allow inbound SSH traffic from web server 
        management_server_sg.add_ingress_rule(
            Peer.ipv4('10.10.10.0/26'),
            Port.tcp(22),
            "Allow inbound SSH traffic from web server"
        )

        # Allow Outbound SSH traffic from web server 
        management_server_sg.add_egress_rule(
            Peer.ipv4('10.10.10.0/26'),
            Port.tcp(22),
            "Allow Outbound SSH traffic from web server"
        )



        # Create the EC2 web server instance
        ec2_instance = ec2.Instance(self, "Cloud10Webserver",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc_web,
            vpc_subnets=ec2.SubnetSelection(subnets=[ec2.Subnet.from_subnet_attributes(self, "PublicSubnet1", subnet_id=public_subnet_1.ref, availability_zone="eu-central-1a")]),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            user_data=my_user_data
        )

        # Create the management server EC2 instance
        management_ec2_instance = ec2.Instance(self, "Cloud10ManagementServer",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc_manage,
            vpc_subnets=ec2.SubnetSelection(subnets=[ec2.Subnet.from_subnet_attributes(self, "PublicSubnet1Manage", subnet_id=public_subnet_1_manage.ref, availability_zone="eu-central-1a")]),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            user_data=my_user_data,
            security_group=management_server_sg
        )





#         # Create vpc_manage private subnets manually
#         private_subnet_manage_1 = ec2.CfnSubnet(self, "VPCManagePrivateSubnet1", 
#                                         vpc_id=vpc_manage.vpc_id,
#                                         cidr_block="10.20.20.128/26", 
#                                         availability_zone="eu-central-1a" # replace with your preferred AZ
#                                         )

#         private_subnet_manage_2 = ec2.CfnSubnet(self, "VPCManagePrivateSubnet2", 
#                                         vpc_id=vpc_manage.vpc_id,
#                                         cidr_block="10.20.20.192/26", 
#                                         availability_zone="eu-central-1b" # replace with your preferred AZ
#                                         )
        
        # # Create route tables for the vpc web private and public subnets
        # route_table1 = ec2.CfnRouteTable(self, "VPCWebRouteTable1", vpc_id=vpc_web.vpc_id)
        # route_table2 = ec2.CfnRouteTable(self, "VPCWebRouteTable2", vpc_id=vpc_web.vpc_id)
        # route_table1.add_depends_on(tgw)
        # route_table2.add_depends_on(tgw)

        # # Associate the vpc web route tables with the private and public subnets
        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation1", 
        #                                 subnet_id=private_subnet_1.ref, 
        #                                 route_table_id=route_table1.ref
        #                                 )

        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation2", 
        #                                 subnet_id=private_subnet_2.ref, 
        #                                 route_table_id=route_table2.ref
        #                                 )
        
        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation3", 
        #                                 subnet_id=public_subnet_1.ref, 
        #                                 route_table_id=route_table1.ref
        #                                 )

        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation4", 
        #                                 subnet_id=public_subnet_2.ref, 
        #                                 route_table_id=route_table2.ref
        #                                 )
        
        # # Create a route to the Transit Gateway in route_table1
        # ec2.CfnTransitGatewayRoute(self, "TransitGatewayRoute1",
        #     transit_gateway_attachment_id=tgw.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     route_table_id=route_table1.ref
        # )

        # # Create a route to the Transit Gateway in route_table2
        # ec2.CfnTransitGatewayRoute(self, "TransitGatewayRoute1",
        #     transit_gateway_attachment_id=tgw.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     route_table_id=route_table2.ref
        # )

        # # Create a default vpc web route pointing to the NAT Gateway
        # ec2.CfnRoute(self, "VPCWebDefaultRoute1", 
        #             route_table_id=route_table1.ref,
        #             destination_cidr_block="0.0.0.0/0", 
        #             nat_gateway_id=nat_gw.ref
        #             )

        # ec2.CfnRoute(self, "VPCWebDefaultRoute2", 
        #             route_table_id=route_table2.ref,
        #             destination_cidr_block="0.0.0.0/0", 
        #             nat_gateway_id=nat_gw.ref
        #             )
        
        # # Create route tables for the vpc manage private subnets
        # route_table1_manage = ec2.CfnRouteTable(self, "VPCManageRouteTable1", vpc_id=vpc_manage.vpc_id)
        # route_table2_manage = ec2.CfnRouteTable(self, "VPCManageRouteTable2", vpc_id=vpc_manage.vpc_id)
        # route_table1_manage.add_depends_on(tgw)
        # route_table2_manage.add_depends_on(tgw)

        # # Associate the vpc manage route tables with the private and public subnets
        # ec2.CfnSubnetRouteTableAssociation(self, "VPCManageRouteTableAssociation1", 
        #                                 subnet_id=private_subnet_manage_1.ref, 
        #                                 route_table_id=route_table1_manage.ref
        #                                 )

        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation2", 
        #                                 subnet_id=private_subnet_manage_2.ref, 
        #                                 route_table_id=route_table2_manage.ref
        #                                 )

        # ec2.CfnSubnetRouteTableAssociation(self, "VPCManageRouteTableAssociation3", 
        #                                 subnet_id=public_subnet_1_manage.ref, 
        #                                 route_table_id=route_table1_manage.ref
        #                                 )

        # ec2.CfnSubnetRouteTableAssociation(self, "VPCWebRouteTableAssociation4", 
        #                                 subnet_id=public_subnet_2_manage.ref, 
        #                                 route_table_id=route_table2_manage.ref
        #                                 )
        # # Create a route to the Transit Gateway in route_table1_manage
        # ec2.CfnTransitGatewayRoute(self, "TransitGatewayRoute1",
        #     transit_gateway_attachment_id=tgw.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     route_table_id=route_table1_manage.ref
        # )

        # # Create a route to the Transit Gateway in route_table2_manage
        # ec2.CfnTransitGatewayRoute(self, "TransitGatewayRoute1",
        #     transit_gateway_attachment_id=tgw.ref,
        #     destination_cidr_block="0.0.0.0/0",
        #     route_table_id=route_table2_manage.ref
        # )

        # # Create a default vpc manage route pointing to the NAT Gateway
        # ec2.CfnRoute(self, "VPCWebDefaultRoute1", 
        #             route_table_id=route_table1_manage.ref,
        #             destination_cidr_block="0.0.0.0/0", 
        #             nat_gateway_id=nat_gw.ref
        #             )

        # ec2.CfnRoute(self, "VPCWebDefaultRoute2", 
        #             route_table_id=route_table2_manage.ref,
        #             destination_cidr_block="0.0.0.0/0", 
        #             nat_gateway_id=nat_gw.ref
        #             )
        
#         # # Create a secret in AWS Secrets Manager
#         # secret = sm.Secret(self, "Cloud10WSDatabaseSecret",
#         #     description="Password for Cloud10WSDatabase",
#         #     generate_secret_string=sm.SecretStringGenerator(
#         #         secret_string_template=json.dumps({"username": "admin"}),
#         #         generate_string_key='password',
#         #         password_length=16,
#         #         exclude_characters='/@"'
#         #     ),
#         # )

#         # Read the user data script file
#         with open('user-data.sh', 'r') as file:
#             user_data_script = file.read()

#         # Create custom UserData from the script
#         my_user_data = ec2.UserData.custom(user_data_script)

#         # Create web server security group
#         web_server_sg = ec2.SecurityGroup(
#             self, "WebServerSG",
#             vpc=vpc_web,
#             allow_all_outbound=False,
#             security_group_name="WebServerSG"
#         )

#         # Allow inbound HTTP traffic
#         web_server_sg.add_ingress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(80),
#             "Allow inbound HTTP traffic"
#         )

#         # Allow inbound HTTPS traffic
#         web_server_sg.add_ingress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(443),
#             "Allow inbound HTTPS traffic"
#         )

#         # Allow inbound SSH traffic from management server
#         web_server_sg.add_ingress_rule(
#             ec2.Peer.ipv4(private_subnet_manage_1),
#             ec2.Port.tcp(22),
#             "Allow inbound SSH traffic from management server"
#         )

#         # Allow outbound HTTP traffic
#         web_server_sg.add_egress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(80),
#             "Allow outbound HTTP traffic"
#         )

#         # Allow outbound HTTPS traffic
#         web_server_sg.add_egress_rule(
#             ec2.Peer.any_ipv4(),
#             ec2.Port.tcp(443),
#             "Allow outbound HTTPS traffic"
#         )

#         # Allow outbound SSH traffic to management server
#         web_server_sg.add_egress_rule(
#             ec2.Peer.ipv4(private_subnet_manage_1),
#             ec2.Port.tcp(22),
#             "Allow outbound SSH traffic to management server"
#         )

#         # Create management server security group
#         management_server_sg = ec2.SecurityGroup(
#             self, "ManagementServerSG",
#             vpc=vpc_manage,
#             allow_all_outbound=False,
#             security_group_name="ManagementServerSG"
#         )

#         # Allow inbound SSH traffic from web server 
#         management_server_sg.add_ingress_rule(
#             ec2.Peer.ipv4(public_subnet_1),
#             ec2.Port.tcp(22),
#             "Allow inbound SSH traffic from web server"
#         )

#         # Allow Outbound SSH traffic from web server 
#         management_server_sg.add_egress_rule(
#             ec2.Peer.ipv4(public_subnet_1),
#             ec2.Port.tcp(22),
#             "Allow Outbound SSH traffic from web server"
#         )

#         # Create the EC2 web server instance
#         ec2_instance = ec2.Instance(self, "Cloud10Webserver",
#             instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
#             machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
#             vpc=vpc_web,
#             vpc_subnets=ec2.SubnetSelection(subnets=public_subnet_1),
#             block_devices=[
#                 ec2.BlockDevice(
#                     device_name="/dev/xvda",
#                     volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
#                 )
#             ],
#             user_data=my_user_data,
#             security_group=web_server_sg
#         )

#         # Create the management server EC2 instance
#         management_ec2_instance = ec2.Instance(self, "Cloud10ManagementServer",
#             instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
#             machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
#             vpc=vpc_manage,
#             vpc_subnets=ec2.SubnetSelection(subnets=private_subnet_manage_1),
#             block_devices=[
#                 ec2.BlockDevice(
#                     device_name="/dev/xvda",
#                     volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
#                 )
#             ],
#             user_data=my_user_data,
#             security_group=management_server_sg
#         )

#         # Create the RDS instance
#         # rds_instance = rds.DatabaseInstance(self, "Cloud10WSDatabase",
#         #     engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
#         #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
#         #     vpc=vpc,
#         #     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
#         #     publicly_accessible=False,
#         #     multi_az=True,
#         #     allocated_storage=20,
#         #     storage_type=rds.StorageType.GP2,
#         #     cloudwatch_logs_exports=["audit", "error", "general"],
#         #     deletion_protection=False,
#         #     database_name='Cloud10WSDatabase',
#         #     credentials=rds.Credentials.from_secret(secret),
#         #     storage_encrypted=True
#         # )

#         # Create an Auto Scaling group
#         asg = autoscaling.AutoScalingGroup(
#             self,
#             "Cloud10WebserverASG",
#             vpc=vpc_web,
#             instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
#             machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
#             user_data=my_user_data,
#             security_group=web_server_sg,
#             desired_capacity=1,
#             min_capacity=1,
#             max_capacity=5,
#             vpc_subnets=ec2.SubnetSelection(subnets=public_subnet_1),
#             block_devices=[
#                 autoscaling.BlockDevice(
#                     device_name="/dev/xvda",
#                     volume=autoscaling.BlockDeviceVolume.ebs(20, encrypted=True)
#                 )
#             ],
#         )

#         # Create a load balancer
#         lb = elbv2.ApplicationLoadBalancer(
#             self,
#             "MyLoadBalancer",
#             vpc=vpc_web,
#             internet_facing=True
#         )

#         # Create a target group
#         target_group = elbv2.ApplicationTargetGroup(
#             self,
#             "MyTargetGroup",
#             vpc=vpc_web,
#             port=80,
#             targets=[asg]
#         )

#         # Add the target group to the load balancer
#         listener = lb.add_listener(
#             "MyListener",
#             port=80,
#             default_action=elbv2.ListenerAction.forward([target_group])
#         )

#         # Output the load balancer DNS name
#         aws_cdk.CfnOutput(
#             self,
#             "LoadBalancerDNS",
#             value=lb.load_balancer_dns_name
#         )

#         # Create a NACL for the web server VPC
#         nacl_web = ec2.CfnNetworkAcl(
#             self,
#             "WebServerNacl",
#             vpc_id=vpc_web.vpc_id
#         )

#         # Inbound rule in vpc_web for HTTP
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclInboundHTTP",
#             network_acl_id=nacl_web.ref,
#             rule_number=100,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=False,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=80,
#                 to=80
#             ),
#             cidr_block="0.0.0.0/0",
#         )

#         # Inbound rule in vpc_web for HTTPS
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclInboundHTTPS",
#             network_acl_id=nacl_web.ref,
#             rule_number=101,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=False,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=443,
#                 to=443
#             ),
#             cidr_block="0.0.0.0/0",
#         )

#         # Inbound rule in vpc_web for SSH from management server via transit gateway
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclInboundSSH",
#             network_acl_id=nacl_web.ref,
#             rule_number=102,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=False,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=22,
#                 to=22
#             ),
#             cidr_block="10.20.20.128/26",  # Modified
#         )

#         # Outbound rule in vpc_web for HTTP
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclOutboundHTTP",
#             network_acl_id=nacl_web.ref,
#             rule_number=100,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=True,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=80,
#                 to=80
#             ),
#             cidr_block="0.0.0.0/0",
#         )

#         # Outbound rule in vpc_web for HTTPS
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclOutboundHTTPS",
#             network_acl_id=nacl_web.ref,
#             rule_number=101,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=True,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=443,
#                 to=443
#             ),
#             cidr_block="0.0.0.0/0",
#         )

#         # Outbound rule in vpc_web for SSH traffic to management server via transit gateway
#         ec2.CfnNetworkAclEntry(
#             self,
#             "WebServerNaclOutboundSSH",
#             network_acl_id=nacl_web.ref,
#             rule_number=102,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=True,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=22,
#                 to=22
#             ),
#             cidr_block="10.20.20.128/26",  # Modified
#         )

#         # Create a NACL for the management server VPC
#         nacl_manage = ec2.CfnNetworkAcl(
#             self,
#             "ManagementServerNacl",
#             vpc_id=vpc_manage.vpc_id
#         )

#         # Inbound rule in vpc_manage for SSH from web server via transit gateway
#         ec2.CfnNetworkAclEntry(
#             self,
#             "ManagementServerNaclInboundSSH",
#             network_acl_id=nacl_manage.ref,
#             rule_number=100,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=False,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=22,
#                 to=22
#             ),
#             cidr_block="10.10.10.0/26",  # Modified
#         )

#         # Outbound rule in vpc_manage for SSH to web server via transit gateway
#         ec2.CfnNetworkAclEntry(
#             self,
#             "ManagementServerNaclOutboundSSH",
#             network_acl_id=nacl_manage.ref,
#             rule_number=100,
#             protocol=6,  # TCP
#             rule_action="allow",
#             egress=True,
#             port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
#                 from_=22,
#                 to=22
#             ),
#             cidr_block="10.10.10.0/26",  # Modified
#         )

#         # Associate NACL to all the subnets of the WebServer
#         for i, subnet in enumerate(vpc_web.public_subnets + vpc_web.private_subnets, 1):
#             ec2.CfnSubnetNetworkAclAssociation(
#                 self,
#                 f"WebServerSubnet{i}NaclAssociation",
#                 subnet_id=subnet.subnet_id,
#                 network_acl_id=nacl_web.ref,
#             )

#         # Associate NACL to all the subnets of the ManagementServer
#         for i, subnet in enumerate(vpc_manage.public_subnets + vpc_manage.private_subnets, 1):
#             ec2.CfnSubnetNetworkAclAssociation(
#                 self,
#                 f"ManagementServerSubnet{i}NaclAssociation",
#                 subnet_id=subnet.subnet_id,
#                 network_acl_id=nacl_manage.ref,
#             )


#         # Attach VPCs to the Transit Gateway
#         tgw_attachment_vpc = ec2.CfnTransitGatewayAttachment(self, "TgwAttachmentWebVPC",
#             transit_gateway_id=tgw.ref,
#             vpc_id=vpc_web.vpc_id,
#             subnet_ids=[subnet.subnet_id for subnet in vpc_web.public_subnets]
#         )
#         tgw_attachment_vpc.add_depends_on(tgw)  # Add this

#         tgw_attachment_vpc_manage = ec2.CfnTransitGatewayAttachment(self, "TgwAttachmentManageVPC",
#             transit_gateway_id=tgw.ref,
#             vpc_id=vpc_manage.vpc_id,
#             subnet_ids=[subnet.subnet_id for subnet in vpc_manage.public_subnets]
#         )
#         tgw_attachment_vpc_manage.add_depends_on(tgw)  # Add this

#         # Create Transit Gateway route tables for the VPCs
#         tgw_route_table_web = ec2.CfnTransitGatewayRouteTable(self, "TgwRouteTableWeb",
#             transit_gateway_id=tgw.ref
#         )

#         tgw_route_table_manage = ec2.CfnTransitGatewayRouteTable(self, "TgwRouteTableManage",
#             transit_gateway_id=tgw.ref
#         )

#         # Associate the VPCs with the Transit Gateway route tables
#         ec2.CfnTransitGatewayRouteTableAssociation(self, "TgwRouteTableAssociationWeb",
#             transit_gateway_attachment_id=tgw_attachment_vpc.ref,
#             transit_gateway_route_table_id=tgw_route_table_web.ref
#         )

#         ec2.CfnTransitGatewayRouteTableAssociation(self, "TgwRouteTableAssociationManage",
#             transit_gateway_attachment_id=tgw_attachment_vpc_manage.ref,
#             transit_gateway_route_table_id=tgw_route_table_manage.ref
#         )

#         # Create routes in the Transit Gateway route tables
#         ec2.CfnTransitGatewayRoute(self, "TgwRouteToManageVPC",
#             destination_cidr_block="10.20.20.0/24",
#             transit_gateway_route_table_id=tgw_route_table_web.ref,
#             transit_gateway_attachment_id=tgw_attachment_vpc_manage.ref
#         )

#         ec2.CfnTransitGatewayRoute(self, "TgwRouteToWebVPC",
#             destination_cidr_block="10.10.10.0/24",
#             transit_gateway_route_table_id=tgw_route_table_manage.ref,
#             transit_gateway_attachment_id=tgw_attachment_vpc.ref
#         )

        
# app = aws_cdk.App()
# CloudProjectStack(app, "CloudProjectStack")
# app.synth()

