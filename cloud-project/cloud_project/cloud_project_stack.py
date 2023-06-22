from aws_cdk import Stack, aws_s3 as s3, aws_ec2 as ec2, aws_rds as rds, aws_secretsmanager as sm, aws_backup as backup, aws_iam as iam
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
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="WebServerSG"
        )

        # Allow inbound HTTP traffic
        web_server_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow inbound HTTP traffic"
        )

        # Create the EC2 web server instance
        ec2_instance = ec2.Instance(self, "Cloud10Webserver",
            instance_type=InstanceType.of(InstanceClass.BURSTABLE3, InstanceSize.MICRO),
            machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
            vpc=vpc,
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

        # Create AWS Backup Vault for the web server
        backup_vault = backup.CfnBackupVault(
            self, "WebServerBackupVault",
            backup_vault_name="WebServerBackupVault"
        )

        # Backup plan rules
        backup_plan_rules = [{
            "ruleName": "DailyBackup",
            "targetBackupVault": backup_vault.backup_vault_name,
            "scheduleExpression": "cron(0 0 * * ? *)",
            "startWindowMinutes": 60,
            "completionWindowMinutes": 180,
            "lifecycle": {
                "deleteAfterDays": 7
            }
        }]

        # Create Backup plan
        backup_plan = backup.CfnBackupPlan(
            self, "WebServerBackupPlan",
            backup_plan=backup.CfnBackupPlan.BackupPlanResourceTypeProperty(
                backup_plan_name="WebServerBackupPlan",
                backup_plan_rule=backup_plan_rules
            )
        )

        # Assign backup plan to resource
        backup_selection = backup.CfnBackupSelection(
            self, "WebServerBackupSelection",
            backup_plan_id=backup_plan.ref,
            backup_selection=backup.CfnBackupSelection.BackupSelectionResourceTypeProperty(
                iam_role_arn="arn:aws:iam::017967599866:role/aws-service-role/backup.amazonaws.com/AWSServiceRoleForBackup",  # replace "account-id" with your actual AWS account ID
                selection_name="WebServerSelection",
                resources_to_backup=[ec2_instance.instance_arn]
            )
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
            user_data=my_user_data
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

        # Create route tables for each VPC and associate them with Transit Gateway
        vpc_route_table1 = ec2.CfnTransitGatewayRouteTable(self, "Cloud10VPCRouteTable",
            transit_gateway_id=tgw.ref
        )
        
        vpc_route_table_association1 = ec2.CfnTransitGatewayRouteTableAssociation(self, "Cloud10VPCRouteTableAssociation",
            transit_gateway_attachment_id=tgw_attachment1.ref,
            transit_gateway_route_table_id=vpc_route_table1.ref
        )
        
        vpc_route_table_propagation1 = ec2.CfnTransitGatewayRouteTablePropagation(self, "Cloud10VPCRouteTablePropagation",
            transit_gateway_attachment_id=tgw_attachment1.ref,
            transit_gateway_route_table_id=vpc_route_table1.ref
        )

        vpc_route_table2 = ec2.CfnTransitGatewayRouteTable(self, "Cloud10VPCManageRouteTable",
            transit_gateway_id=tgw.ref
        )
        
        vpc_route_table_association2 = ec2.CfnTransitGatewayRouteTableAssociation(self, "Cloud10VPCManageRouteTableAssociation",
            transit_gateway_attachment_id=tgw_attachment2.ref,
            transit_gateway_route_table_id=vpc_route_table2.ref
        )
        
        vpc_route_table_propagation2 = ec2.CfnTransitGatewayRouteTablePropagation(self, "Cloud10VPCManageRouteTablePropagation",
            transit_gateway_attachment_id=tgw_attachment2.ref,
            transit_gateway_route_table_id=vpc_route_table2.ref
        )
