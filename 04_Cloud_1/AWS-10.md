# Virtual Private Cloud (VPC)
AWS VPC (Virtual Private Cloud) is a virtual network that you can create in the AWS (Amazon Web Services) cloud. It allows you to launch resources like Amazon EC2 instances, databases, and load balancers in a logically isolated and secure environment that you control. Think of it like your own private network in the cloud. With VPC, you can define your own IP address range, subnets, and routing tables, and you can even connect your VPC to your on-premises network using a VPN (Virtual Private Network) connection.

## Key-terms
**IGW**

An Internet Gateway (IGW) is a component that allows resources within your AWS VPC to communicate with the internet. It acts as a doorway between your VPC and the public internet, allowing traffic to flow in and out. Think of it like a toll booth on a highway - the IGW determines whether traffic is allowed to enter or exit your VPC. Without an IGW, your VPC would be completely isolated from the internet, and resources within it would only be able to communicate with each other.

**NAT Gateway**

A NAT (Network Address Translation) Gateway is a component that allows resources within your AWS VPC to access the internet while keeping their IP addresses private. It translates the private IP addresses of your resources into a public IP address that can be recognized by the internet, and vice versa. Think of it like a translator - the NAT gateway helps your VPC resources speak the same language as the internet. Without a NAT gateway, resources within your VPC would not be able to communicate with the internet using their private IP addresses.

**VPN Connection**

A VPN (Virtual Private Network) connection is a secure way to connect your AWS VPC to your on-premises network or another VPC over the internet. It creates an encrypted tunnel between the two networks, allowing data to be transmitted securely. Think of it like a secret tunnel between two houses - nobody outside can see what's being passed back and forth. With a VPN connection, you can extend your on-premises network to the cloud, or connect multiple VPCs together, allowing resources in each network to communicate with each other securely.

**RDS**

RDS (Relational Database Service) is a managed database service provided by AWS (Amazon Web Services) that allows you to easily create, operate, and scale relational databases in the cloud. It takes care of the underlying infrastructure, such as server maintenance, backups, and software patching, allowing you to focus on your applications and data. Think of it like a hotel - you don't need to worry about the maintenance and cleaning of the room, you just need to focus on enjoying your stay.

**ECS**

ECS (Elastic Container Service) is a managed service provided by AWS (Amazon Web Services) that allows you to run and manage containers on a cluster of virtual machines in the cloud. It makes it easy to deploy, scale, and manage Docker containers without needing to manage the underlying infrastructure. Think of it like a shipping container yard - ECS provides a place to store and manage containers, just like a shipping yard provides a place to store and manage shipping containers.

**CIDR Block**

A CIDR (Classless Inter-Domain Routing) block is a way of representing a range of IP addresses in a compact format. It is used in networking to define the range of IP addresses that can be assigned to devices on a network. Think of it like a street address - just as a street address tells you where a building is located, a CIDR block tells you which IP addresses are available for use.

**EIPs**

An EIP (Elastic IP address) is a static, public IP address that can be assigned to an AWS resource, such as an EC2 instance or a NAT gateway. It allows the resource to have a fixed, public IP address that can be used to communicate with the internet or other resources. Think of it like a phone number that never changes - just as your phone number is a fixed identifier that people can use to reach you, an EIP is a fixed identifier that resources can use to communicate with the outside world. With an EIP, you can avoid the need to update DNS records or reconfigure firewalls every time the IP address of a resource changes.

## Opdracht
**Exercise 1**

- Allocate an Elastic IP address to your account.
- Create a new VPC with the following requirements:
1. Region: Frankfurt (eu-central-1)
2. VPC with a public and a private subnet
3. Name: Lab VPC
4. CIDR: 10.0.0.0/16
- Requirements for the public subnet:
1. Name: Public subnet 1
2. CIDR: 10.0.0.0/24
3. AZ: eu-central-1a
- Requirements for the private subnet:
1. Name: Private subnet 1
2. CIDR: 10.0.1.0/24
3. AZ: eu-central-1a

**Exercise 2**
- Create an additional public subnet with the following requirements:
1. VPC: Lab VPC
2. Name: Public Subnet 2
3. AZ: eu-central-1b
4. CIDR: 10.0.2.0/24
- Create an additional private subnet with the following requirements:
1. VPC: Lab VPC
2. Name: Private Subnet 2
3. AZ: eu-central-1b
4. CIDR: 10.0.3.0/24
- View the main route table for Lab VPC. It should have an entry for the NAT gateway. Rename this route table to Private Route Table.
- Explicitly associate the private route table with your two private subnets.
- View the other route table for Lab VPC. It should have an entry for the internet gateway. Rename this route table to Public Route Table.
- Explicitly associate the public route table to your two public subnets.

**Exercise 3**
- Create a Security Group with the following requirements:
1. Name: Web SG
2. Description: Enable HTTP Access
3. VPC: Lab VPC
4. Inbound rule: allow HTTP access from anywhere
5. Outbound rule: Allow all traffic

**Exercise 4**

- Launch an EC2 instance with the following requirements:
1. AMI: Amazon Linux 2
2. Type: t3.micro
3. Subnet: Public subnet 2
4. Auto-assign Public IP: Enable
5. User data:
![Alt text](../00_includes/Week-4-AWS/AWS-10-UserData.PNG)

6. Tag:
7. Key: Name
8. Value: Web server
9. Security Group: Web SG
10. Key pair: no key pair
- Connect to your server using the public IPv4 DNS name.



### Gebruikte bronnen
ChatGPT

Udemy Course

https://www.youtube.com/watch?v=Iqzgu5UEDKo

### Ervaren problemen
I had some issues understanding some questions, but that is because I looked too deep into them instead of keeping it simpler.

I could not connect the first day. I went through all the settings to make sure everything was set in order, I even used the Reachability Analyzer to check if my connection / setup is good. 

It came out successful but still would not show the web-page.

I also could not see the IPv4 Public DNS on the aws site, But I was able to find it using a command in the terminal

The next day I start my instance and tried again by pasting the ip-address in my browser and it ends up working.

### Resultaat
**Exercise 1**

I allocated an Elastic IP address to my account.
![Alt text](../00_includes/Week-4-AWS/AWS-10-Allocate-ElasticIP.PNG)

I created the VPC with the specified requirements.
![Alt text](../00_includes/Week-4-AWS/AWS-10-VPC1-Created.PNG)

I created the public and private subnets with the specified requirments.
![Alt text](../00_includes/Week-4-AWS/AWS-10-PublicSubnet1.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-PrivateSubnet1.PNG)

**Exercise 2**

I created the additional public and private subnets, with the specified requirments.
![Alt text](../00_includes/Week-4-AWS/AWS-10-PublicSubnet2.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-PrivateSubnet2.PNG)

I renamed the main route table to "Private Route Table"
![Alt text](../00_includes/Week-4-AWS/AWS-10-MainRouteTable-Renamed.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-MainRouteTable-Renamed2.PNG)

I proceeded to explicitly associate the private route table to the private subnets.
![Alt text](../00_includes/Week-4-AWS/AWS-10-ExcplicitlyPrivateSubnet.PNG)

I then proceeded to make a new route table and named it "Public Subnets Table", and explicitly associated the public subnets with it.
![Alt text](../00_includes/Week-4-AWS/AWS-10-ExcplicitlyPublicSubnet.PNG)

I then proceeded to make an Internet Gateway.
![Alt text](../00_includes/Week-4-AWS/AWS-10-InternetGateway-Made.PNG)

I then attached the Internet Gateway to my VPC.
![Alt text](../00_includes/Week-4-AWS/AWS-10-InternetGateway-AttachVPC.PNG)

And proceeded to edit the target and link it to my public route table.
![Alt text](../00_includes/Week-4-AWS/AWS-10-InternetGateway-AddedRoutes.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-LinkedPublicSubnetsToInternetGateway.PNG)

I made a NAT-Gateway and made sure I linked it to the Public Subnet 1.
![Alt text](../00_includes/Week-4-AWS/AWS-10-NAT-Gateway-Made.PNG)

I then proceeded to edit the target and link it to my private route table.
![Alt text](../00_includes/Week-4-AWS/AWS-10-NAT-Gateway-Targeted.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-LinkedPrivateSubnetsToNatGateway.PNG)

So now I had successfully split the private and public route tables, associated the subnets to each accordingly, linked the Internet Gateway to the Public Route Table and the NAT Gateway to the private route table. All of them are also linked the the Lab VPC.
![Alt text](../00_includes/Week-4-AWS/AWS-10-PublicAndPrivateRouteTable-Made.PNG)

**Exercise 3**

I created the security group with the specified requirments.
![Alt text](../00_includes/Week-4-AWS/AWS-10-SecurityGroupSettings.PNG)

**Exercise 4**

I then created an EC2 Instance with the specified requirments and launched it.
![Alt text](../00_includes/Week-4-AWS/AWS-10-InstanceSettings1.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-InstanceSettings2.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-InstanceSettings3.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-InstanceSettings4.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-InstanceSettings5.PNG)

![Alt text](../00_includes/Week-4-AWS/AWS-10-Instance-Launch.PNG)

In order to connect to my server using the public IPv4 DNS name, I tried putting the following command in my terminal. **nslookup (the public ip of my instance) because I did not see the public IPv4 DNS name in the details section of AWS.

![Alt text](../00_includes/Week-4-AWS/AWS-10-Found-DNS-Name.PNG)


After going over all the settings again and rebooting my instance to be sure. I was able to paste public IPv4 DNS name in my web-browser and it worked

![Alt text](../00_includes/Week-4-AWS/AWS-10-WebserverConnect1.PNG)













