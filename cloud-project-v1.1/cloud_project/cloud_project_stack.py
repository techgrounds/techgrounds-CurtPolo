from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2, aws_rds as rds, aws_secretsmanager as sm, aws_backup as backup, aws_iam as iam, aws_elasticloadbalancingv2 as elbv2, aws_autoscaling as autoscaling, aws_cloudwatch as cloudwatch, aws_certificatemanager as acm
import aws_cdk as cdk
import aws_cdk.aws_kms as kms
from aws_cdk.aws_ec2 import AmazonLinuxImage, AmazonLinuxGeneration, InstanceClass, InstanceSize, InstanceType, WindowsImage, WindowsVersion, UserData
from constructs import Construct
import json
import boto3

class CloudProjectStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Check if S3 bucket exists
        s3_client = boto3.client('s3')
        bucket_name = 'cloud10-project-bucket'
        bucket_exists = True

        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except:
            bucket_exists = False

        # Create S3 bucket if it doesn't exist
        if not bucket_exists:
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
                ec2.SubnetConfiguration(name="private", cidr_mask=26, subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
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

        # Create load balancer security group
        load_balancer_sg = ec2.SecurityGroup(
            self, "LoadBalancerSG",
            vpc=vpc_web,
            allow_all_outbound=True,
            security_group_name="LoadBalancerSG"
        )

        # Allow inbound HTTP traffic
        load_balancer_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow inbound HTTP traffic"
        )

        # Allow inbound HTTPS traffic
        load_balancer_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow inbound HTTPS traffic"
        )

        # Allow outbound HTTP traffic
        load_balancer_sg.add_egress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow outbound HTTP traffic"
        )

        # Allow outbound HTTPS traffic
        load_balancer_sg.add_egress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow outbound HTTPS traffic"
        )

        # Create web server security group
        web_server_sg = ec2.SecurityGroup(
            self, "WebServerSG",
            vpc=vpc_web,
            allow_all_outbound=True,
            security_group_name="WebServerSG"
        )

        # Allow inbound HTTP traffic from load balancer security group
        web_server_sg.add_ingress_rule(
            ec2.SecurityGroup.from_security_group_id(
                self, "LoadBalancerSGRefHTTP", load_balancer_sg.security_group_id),
            ec2.Port.tcp(80),
            "Allow inbound HTTP traffic from load balancer security group"
        )

        # Allow inbound HTTPS traffic from load balancer security group
        web_server_sg.add_ingress_rule(
            ec2.SecurityGroup.from_security_group_id(
                self, "LoadBalancerSGRefHTTPS", load_balancer_sg.security_group_id),
            ec2.Port.tcp(443),
            "Allow inbound HTTPS traffic from load balancer security group"
        )

        
        # Allow inbound SSH traffic from management server via transit gateway
        web_server_sg.add_ingress_rule(
            ec2.Peer.ipv4(vpc_manage.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow inbound SSH traffic from management server via transit gateway"
        )


        # Create management server security group
        management_server_sg = ec2.SecurityGroup(
            self, "ManagementServerSG",
            vpc=vpc_manage,
            allow_all_outbound=True,
            security_group_name="ManagementServerSG"
        )

        admin_ip = "213.73.212.167/32" #replace this with your admin's public ip

        # Allow inbound SSH traffic from web server via transit gateway
        management_server_sg.add_ingress_rule(
            ec2.Peer.ipv4(vpc_web.vpc_cidr_block),
            ec2.Port.tcp(22),
            "Allow inbound SSH traffic from web server via transit gateway"
        )

        # Allow RDP traffic between admin pc and management server
        management_server_sg.add_ingress_rule(
            ec2.Peer.ipv4(admin_ip),
            ec2.Port.tcp(3389),
            "Allow RDP access from admin IP"
        )

        # Create the management server EC2 instance
        management_ec2_instance = ec2.Instance(self, "Cloud10ManagementServer",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=WindowsImage(WindowsVersion.WINDOWS_SERVER_2022_ENGLISH_FULL_BASE),
            vpc=vpc_manage,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_name="ManageKeyPair", # Name of the key pair used for the SSH / RDP connection
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(30, encrypted=True)
                )
            ],
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


        # Define the IAM Role with SSM policy
        ssm_role = iam.Role(
            self, 
            "SSMRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")]
)

        # Create an Auto Scaling group
        asg = autoscaling.AutoScalingGroup(
            self,
            "Cloud10WebServerASG",
            auto_scaling_group_name="Cloud10WebServerASG",
            vpc=vpc_web,
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            user_data=my_user_data,
            security_group=web_server_sg,
            desired_capacity=1,
            min_capacity=1,
            max_capacity=3,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            # key_name="WebKeyPair", #If I want to use Key Pairs to SSH
            block_devices=[
                autoscaling.BlockDevice(
                    device_name="/dev/xvda",
                    volume=autoscaling.BlockDeviceVolume.ebs(20, encrypted=True)
                )
            ],
            # Add the role to your Auto Scaling Group
            role=ssm_role
        )

        # Get the underlying CfnAutoScalingGroup object (to eliminate the type error in the dependency)
        cfn_asg = asg.node.default_child

        # Scale up based on CPU utilization
        cpu_scale_up_policy = autoscaling.CfnScalingPolicy(
            self,
            "CpuScaleUpPolicy",
            policy_type="TargetTrackingScaling",
            auto_scaling_group_name=asg.auto_scaling_group_name,
            target_tracking_configuration=autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty(
                target_value=70,
                predefined_metric_specification=autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="ASGAverageCPUUtilization"
                )
            )
        )
        cpu_scale_up_policy.add_dependency(cfn_asg)

        # Scale down based on CPU utilization
        cpu_scale_down_policy = autoscaling.CfnScalingPolicy(
            self,
            "CpuScaleDownPolicy",
            policy_type="TargetTrackingScaling",
            auto_scaling_group_name=asg.auto_scaling_group_name,
            target_tracking_configuration=autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty(
                target_value=50,
                predefined_metric_specification=autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty(
                    predefined_metric_type="ASGAverageCPUUtilization"
                )
            )
        )
        cpu_scale_down_policy.add_dependency(cfn_asg)

        # Create a CloudWatch alarm for scaling up
        cpu_utilization_high_alarm = cloudwatch.CfnAlarm(
            self,
            "CpuUtilizationHighAlarm",
            alarm_description="Scale up if CPU utilization is greater than 70 percent for 1 minute",
            comparison_operator="GreaterThanThreshold",
            evaluation_periods=1,
            metric_name="CPUUtilization",
            namespace="AWS/EC2",
            period=60, # 1 minute in seconds
            statistic="Average",
            threshold=70,
            alarm_actions=[cpu_scale_up_policy.ref],
            dimensions=[cloudwatch.CfnAlarm.DimensionProperty(name="AutoScalingGroupName", value=asg.auto_scaling_group_name)]
        )

        # Create a CloudWatch alarm for scaling down
        cpu_utilization_low_alarm = cloudwatch.CfnAlarm(
            self,
            "CpuUtilizationLowAlarm",
            alarm_description="Scale down if CPU utilization is low",
            comparison_operator="LessThanThreshold",
            evaluation_periods=1,
            metric_name="CPUUtilization",
            namespace="AWS/EC2",
            period=60, # 1 minute in seconds
            statistic="Average",
            threshold=50,
            alarm_actions=[cpu_scale_down_policy.ref],
            dimensions=[cloudwatch.CfnAlarm.DimensionProperty(name="AutoScalingGroupName", value=asg.auto_scaling_group_name)]
        )

        # Attach the CloudWatch alarms to the Auto Scaling group
        cpu_utilization_high_alarm.add_dependency(cfn_asg)
        cpu_utilization_low_alarm.add_dependency(cfn_asg)


        # Create a load balancer
        lb = elbv2.ApplicationLoadBalancer(
            self,
            "WebLoadBalancer",
            vpc=vpc_web,
            internet_facing=True, # This makes the load balancer publically accessable
            load_balancer_name="WebLoadBalancer",
            security_group=load_balancer_sg,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
            )
        
        # Add the target group to the load balancer
        listener = lb.add_listener(
            "MyListener",
            port=80,
            open=True,
        )

        # Configure the HTTP Listener to redirect requests to HTTPS
        listener.add_action(
            "HTTPSRedirect",
            action=elbv2.ListenerAction.redirect(
                protocol="HTTPS",
                port="443",
                host="#{host}",
                path="/#{path}",
                query="#{query}",
            ),
        )

        # Import an existing SSL certificate
        certificate = acm.Certificate.from_certificate_arn(
            self,
            "Certificate",
            certificate_arn="arn:aws:acm:eu-central-1:017967599866:certificate/233edc35-55d3-4854-9047-f50a374a84df",
        )

        # Add an HTTPS listener
        https_listener = lb.add_listener(
            "HTTPSListener",
            port=443,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            certificates=[certificate],
            ssl_policy=elbv2.SslPolicy.RECOMMENDED 
        )
        
        # Create a target group for the web servers
        target_group = elbv2.ApplicationTargetGroup(
             self,
            "WebServerTargetGroup",
            vpc=vpc_web,
            port=80,
            protocol=elbv2.ApplicationProtocol.HTTP,
            targets=[asg],
            health_check=elbv2.HealthCheck(
                port="80",
                protocol=elbv2.Protocol.HTTP,
                path="/",
                timeout=cdk.Duration.seconds(5),
                healthy_threshold_count=2,
                unhealthy_threshold_count=6,
                interval=cdk.Duration.seconds(10)
            ))
        
        # Add a default action to the HTTPS listener
        https_listener.add_action(
            "DefaultAction",
            action=elbv2.ListenerAction.forward(target_groups=[target_group]),
        )

        # Output the load balancer DNS name
        cdk.CfnOutput(
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

        # Inbound rule in vpc_web for HTTP traffic from load balancer security group
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
            cidr_block=vpc_web.public_subnets[0].ipv4_cidr_block
        )

        # Inbound rule in vpc_web for HTTPS traffic from load balancer security group
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundHTTPS",
            network_acl_id=nacl_web.ref,
            rule_number=200,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=443,
                to=443
            ),
            cidr_block=vpc_web.public_subnets[0].ipv4_cidr_block
        )

        # Inbound rule in vpc_web for SSH from management server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "WebServerNaclInboundSSH",
            network_acl_id=nacl_web.ref,
            rule_number=300,
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=22,
                to=22
            ),
            cidr_block=vpc_manage.public_subnets[0].ipv4_cidr_block
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
            rule_number=200,
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
            rule_number=300,
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
            rule_number=400,
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
            rule_number=200,
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

        # Add a new inbound rule in vpc_manage for RDP from the admin IP
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclInboundRDPFromAdmin",
            network_acl_id=nacl_manage.ref,
            rule_number=300,  # A unique rule number
            protocol=6,  # TCP
            rule_action="allow",
            egress=False,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=3389,
                to=3389
            ),
            cidr_block=admin_ip,  # Your admin IP
        )

        # Outbound rule in vpc_manage for RDP to management server via transit gateway
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclOutboundRDP",
            network_acl_id=nacl_manage.ref,
            rule_number=300,  # A unique rule number
            protocol=6,  # TCP
            rule_action="allow",
            egress=True,
            port_range=ec2.CfnNetworkAclEntry.PortRangeProperty(
                from_=3389,
                to=3389
            ),
            cidr_block=vpc_manage.vpc_cidr_block,  # Modified to your VPC's CIDR block
        )


        # Add a new outbound rule in vpc_manage for SSH traffic to the entire vpc_web CIDR block
        ec2.CfnNetworkAclEntry(
            self,
            "ManagementServerNaclOutboundSSHToWeb",
            network_acl_id=nacl_manage.ref,
            rule_number=200,
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
            subnet_ids=[subnet.subnet_id for subnet in vpc_web.private_subnets]
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
        cdk.CfnOutput(
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

