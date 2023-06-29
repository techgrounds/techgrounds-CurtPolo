from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2, aws_rds as rds, aws_secretsmanager as sm, aws_backup as backup, aws_iam as iam, aws_elasticloadbalancingv2 as elbv2, aws_autoscaling as autoscaling
import aws_cdk
from aws_cdk.aws_ec2 import AmazonLinuxImage, AmazonLinuxGeneration, InstanceClass, InstanceSize, InstanceType, UserData
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

        # Create the web server VPC
        vpc_web = ec2.Vpc(self, "Cloud10VPC",
            cidr="10.10.10.0/24",
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
            cidr="10.20.20.0/24",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public", cidr_mask=26, subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="private", cidr_mask=26, subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
            ],
            enable_dns_support=True,
            enable_dns_hostnames=True,
            nat_gateways=1,
        )

        # Create a secret in AWS Secrets Manager
        secret = sm.Secret(self, "Cloud10WSDatabaseSecret",
            description="Password for Cloud10WSDatabase",
            generate_secret_string=sm.SecretStringGenerator(
                secret_string_template=json.dumps({"username": "admin"}),
                generate_string_key='password',
                password_length=16,
                exclude_characters='/@"'
            ),
        )

        # Read the user data script file
        with open('user-data.sh', 'r') as file:
            user_data_script = file.read()

        # Create custom UserData from the script
        my_user_data = ec2.UserData.custom(user_data_script)

        # Create web server security group
        web_server_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc_web,
            allow_all_outbound=False,
            security_group_name="WebServerSG"
        )

        # Allow inbound HTTP traffic
        web_server_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow inbound HTTP traffic"
        )

        # Allow inbound HTTPS traffic
        web_server_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow inbound HTTPS traffic"
        )

        # Allow inbound SSH traffic from management server
        web_server_sg.add_ingress_rule(
            ec2.Peer.ipv4(vpc_manage.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow inbound SSH traffic from management server"
        )

        # Allow outbound HTTP traffic
        web_server_sg.add_egress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow outbound HTTP traffic"
        )

        # Allow outbound HTTPS traffic
        web_server_sg.add_egress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow outbound HTTPS traffic"
        )

        # Allow outbound SSH traffic to management server
        web_server_sg.add_egress_rule(
            ec2.Peer.ipv4(vpc_manage.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow outbound SSH traffic to management server"
        )

        # Create management server security group
        management_server_sg = ec2.SecurityGroup(
            self, "ManagementServerSG",
            vpc=vpc_manage,
            allow_all_outbound=True,
            security_group_name="ManagementServerSG"
        )

        # Allow inbound SSH traffic from web server via transit gateway
        management_server_sg.add_ingress_rule(
            ec2.Peer.ipv4(vpc_web.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow inbound SSH traffic from web server via transit gateway"
        )

        # Create the EC2 web server instance
        ec2_instance = ec2.Instance(self, "Cloud10Webserver",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc_web,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            user_data=my_user_data,
            security_group=web_server_sg
        )

        # Create the management server EC2 instance
        management_ec2_instance = ec2.Instance(self, "Cloud10ManagementServer",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc_manage,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            user_data=my_user_data,
            security_group=management_server_sg
        )

        # Create the RDS instance
        # rds_instance = rds.DatabaseInstance(self, "Cloud10WSDatabase",
        #     engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        #     vpc=vpc,
        #     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
        #     publicly_accessible=False,
        #     multi_az=True,
        #     allocated_storage=20,
        #     storage_type=rds.StorageType.GP2,
        #     cloudwatch_logs_exports=["audit", "error", "general"],
        #     deletion_protection=False,
        #     database_name='Cloud10WSDatabase',
        #     credentials=rds.Credentials.from_secret(secret),
        #     storage_encrypted=True
        # )

        # Create an Auto Scaling group
        asg = autoscaling.AutoScalingGroup(
            self,
            "Cloud10WebserverASG",
            vpc=vpc_web,
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=my_user_data,
            security_group=web_server_sg,
            desired_capacity=1,
            min_capacity=1,
            max_capacity=5,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                autoscaling.BlockDevice(
                    device_name="/dev/xvda",
                    volume=autoscaling.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
        )

        # Create a load balancer
        lb = elbv2.ApplicationLoadBalancer(
            self,
            "MyLoadBalancer",
            vpc=vpc_web,
            internet_facing=True
        )

        # Create a target group
        target_group = elbv2.ApplicationTargetGroup(
            self,
            "MyTargetGroup",
            vpc=vpc_web,
            port=80,
            targets=[asg]
        )

        # Add the target group to the load balancer
        listener = lb.add_listener(
            "MyListener",
            port=80,
            default_action=elbv2.ListenerAction.forward([target_group])
        )

        # Output the load balancer DNS name
        aws_cdk.CfnOutput(
            self,
            "LoadBalancerDNS",
            value=lb.load_balancer_dns_name
        )

        # Create a NACL for the web server VPC
        nacl_web = ec2.CfnNetworkAcl(
            self,
            "WebServerNacl",
            vpc_id=vpc_web.vpc_id
        )

        # Inbound rule in vpc_web for HTTP
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundHTTP",
            network_acl_id=nacl_web.ref,
            rule_number=100,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=80,
                to=80
            ),
            cidr_block="0.0.0.0/0",
        )

        # Inbound rule in vpc_web for HTTPS
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundHTTPS",
            network_acl_id=nacl_web.ref,
            rule_number=101,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=443,
                to=443
            ),
            cidr_block="0.0.0.0/0",
        )

        # Inbound rule in vpc_web for SSH from management server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundSSH",
            network_acl_id=nacl_web.ref,
            rule_number=102,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block="10.20.20.0/24",  # Modified
        )

        # Outbound rule in vpc_web for HTTP
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclOutboundHTTP",
            network_acl_id=nacl_web.ref,
            rule_number=100,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=80,
                to=80
            ),
            cidr_block="0.0.0.0/0",
        )

        # Outbound rule in vpc_web for HTTPS
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclOutboundHTTPS",
            network_acl_id=nacl_web.ref,
            rule_number=101,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=443,
                to=443
            ),
            cidr_block="0.0.0.0/0",
        )

        # Outbound rule in vpc_web for SSH to management server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclOutboundSSH",
            network_acl_id=nacl_web.ref,
            rule_number=102,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block="10.20.20.0/24",  # Modified
        )

        # Create a NACL for the management server VPC
        nacl_manage = ec2.CfnNetworkAcl(
            self,
            "ManagementServerNacl",
            vpc_id=vpc_manage.vpc_id
        )

        # Inbound rule in vpc_manage for SSH from web server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclInboundSSH",
            network_acl_id=nacl_manage.ref,
            rule_number=100,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block="10.10.10.0/24",  # Modified
        )

        # Outbound rule in vpc_manage for SSH to web server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclOutboundSSH",
            network_acl_id=nacl_manage.ref,
            rule_number=100,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block="10.10.10.0/24",  # Modified
        )

        # Associate NACL to all the subnets of the WebServer
        for i, subnet in enumerate(vpc_web.public_subnets + vpc_web.private_subnets, 1):
            ec2.CfnSubnetNetworkAclAssociation(
                self,
                f"WebServerSubnet{i}NaclAssociation",
                subnet_id=subnet.subnet_id,
                network_acl_id=nacl_web.ref,
            )

        # Associate NACL to all the subnets of the ManagementServer
        for i, subnet in enumerate(vpc_manage.public_subnets + vpc_manage.private_subnets, 1):
            ec2.CfnSubnetNetworkAclAssociation(
                self,
                f"ManagementServerSubnet{i}NaclAssociation",
                subnet_id=subnet.subnet_id,
                network_acl_id=nacl_manage.ref,
            )

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
            subnet_ids=[subnet.subnet_id for subnet in vpc_web.public_subnets]
        )
        tgw_attachment_vpc.add_depends_on(tgw)  # Add this

        tgw_attachment_vpc_manage = ec2.CfnTransitGatewayAttachment(self, "TgwAttachmentManageVPC",
            transit_gateway_id=tgw.ref,
            vpc_id=vpc_manage.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc_manage.public_subnets]
        )
        tgw_attachment_vpc_manage.add_depends_on(tgw)  # Add this

        # Create Transit Gateway route tables for the VPCs
        tgw_route_table_web = ec2.CfnTransitGatewayRouteTable(self, "TgwRouteTableWeb",
            transit_gateway_id=tgw.ref
        )

        tgw_route_table_manage = ec2.CfnTransitGatewayRouteTable(self, "TgwRouteTableManage",
            transit_gateway_id=tgw.ref
        )

        # Associate the VPCs with the Transit Gateway route tables
        ec2.CfnTransitGatewayRouteTableAssociation(self, "TgwRouteTableAssociationWeb",
            transit_gateway_attachment_id=tgw_attachment_vpc.ref,
            transit_gateway_route_table_id=tgw_route_table_web.ref
        )

        ec2.CfnTransitGatewayRouteTableAssociation(self, "TgwRouteTableAssociationManage",
            transit_gateway_attachment_id=tgw_attachment_vpc_manage.ref,
            transit_gateway_route_table_id=tgw_route_table_manage.ref
        )

        # Create routes in the Transit Gateway route tables
        ec2.CfnTransitGatewayRoute(self, "TgwRouteToManageVPC",
            destination_cidr_block="10.20.20.0/24",
            transit_gateway_route_table_id=tgw_route_table_web.ref,
            transit_gateway_attachment_id=tgw_attachment_vpc_manage.ref
        )

        ec2.CfnTransitGatewayRoute(self, "TgwRouteToWebVPC",
            destination_cidr_block="10.10.10.0/24",
            transit_gateway_route_table_id=tgw_route_table_manage.ref,
            transit_gateway_attachment_id=tgw_attachment_vpc.ref
        )
