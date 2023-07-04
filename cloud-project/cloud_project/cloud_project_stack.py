from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2, aws_rds as rds, aws_secretsmanager as sm, aws_backup as backup, aws_iam as iam, aws_elasticloadbalancingv2 as elbv2, aws_autoscaling as autoscaling
import aws_cdk
import aws_cdk.aws_kms as kms
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
                ec2.SubnetConfiguration(name="private", cidr_mask=26, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
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
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            user_data=my_user_data,
            security_group=management_server_sg
        )

        # # Create the RDS instance
        # rds_instance = rds.DatabaseInstance(self, "Cloud10WSDatabase",
        #     engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0),
        #     instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        #     vpc=vpc_web,
        #     vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
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
            max_capacity=3,
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

        # Add a new inbound rule in vpc_web for SSH from the entire vpc_manage CIDR block
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundSSHFromManage",
            network_acl_id=nacl_web.ref,
            rule_number=103,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block=vpc_manage.vpc_cidr_block,
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

        # Outbound rule in vpc_web for SSH traffic to management server via transit gateway
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

        # Add a new outbound rule in vpc_web for SSH traffic to the entire vpc_manage CIDR block
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclOutboundSSHToManage",
            network_acl_id=nacl_web.ref,
            rule_number=103,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block=vpc_manage.vpc_cidr_block,
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

        # Add a new inbound rule in vpc_manage for SSH from the entire vpc_web CIDR block
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclInboundSSHFromWeb",
            network_acl_id=nacl_manage.ref,
            rule_number=101,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block=vpc_web.vpc_cidr_block,
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

        # Add a new outbound rule in vpc_manage for SSH traffic to the entire vpc_web CIDR block
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclOutboundSSHToWeb",
            network_acl_id=nacl_manage.ref,
            rule_number=101,
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block=vpc_web.vpc_cidr_block,
        )

        # Create a transit gateway
        transit_gateway = ec2.CfnTransitGateway(
            self,
            "TransitGateway",
            amazon_side_asn=64512
        )

        # TEST Add a dependency between the transit gateway and the route creation loop
        transit_gateway_dependency = ec2.CfnTransitGatewayRouteTable(
            self,
            "TransitGatewayDependency",
            transit_gateway_id=transit_gateway.ref
        )

        # Create a transit gateway route table
        transit_gateway_route_table = ec2.CfnTransitGatewayRouteTable(
            self,
            "TransitGatewayRouteTable",
            transit_gateway_id=transit_gateway.ref
        )

        # Associate the transit gateway route table with the web server VPC
        transit_gateway_vpc_attachment_web = ec2.CfnTransitGatewayAttachment(
            self,
            "TransitGatewayAttachmentWeb",
            transit_gateway_id=transit_gateway.ref,
            vpc_id=vpc_web.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc_web.public_subnets]
        )

        # Associate the transit gateway route table with the management server VPC
        transit_gateway_vpc_attachment_manage = ec2.CfnTransitGatewayAttachment(
            self,
            "TransitGatewayAttachmentManage",
            transit_gateway_id=transit_gateway.ref,
            vpc_id=vpc_manage.vpc_id,
            subnet_ids=[subnet.subnet_id for subnet in vpc_manage.public_subnets]
        )

        # Add a route from the web server VPC to the management server VPC via transit gateway
        ec2.CfnTransitGatewayRoute(
            self,
            "TransitGatewayRouteWebToManage",
            transit_gateway_route_table_id=transit_gateway_route_table.ref,
            destination_cidr_block=vpc_manage.vpc_cidr_block,
            transit_gateway_attachment_id=transit_gateway_vpc_attachment_manage.ref
        )

        # Add a route from the management server VPC to the web server VPC via transit gateway
        ec2.CfnTransitGatewayRoute(
            self,
            "TransitGatewayRouteManageToWeb",
            transit_gateway_route_table_id=transit_gateway_route_table.ref,
            destination_cidr_block=vpc_web.vpc_cidr_block,
            transit_gateway_attachment_id=transit_gateway_vpc_attachment_web.ref
        )

        # Output the transit gateway ID
        aws_cdk.CfnOutput(
            self,
            "TransitGatewayID",
            value=transit_gateway.ref
        )

        # TEST Add transit gateway routes to public subnets of vpc_manage
        for index, subnet in enumerate(vpc_manage.public_subnets):
            route_table_id = subnet.route_table.route_table_id
            route = ec2.CfnRoute(
                self, f'PublicSubnetTransitGatewayRoute{index}',
                destination_cidr_block='10.10.10.0/24',
                route_table_id=route_table_id,
                transit_gateway_id=transit_gateway.ref
            )
            route.add_dependency(transit_gateway_dependency)
