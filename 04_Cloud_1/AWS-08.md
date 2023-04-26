# Security Groups
In AWS, a security group is a virtual firewall that controls inbound and outbound traffic for an EC2 instance or a group of instances. Security Groups are stateful virtual firewalls that can be assigned to instances. They do not run in the OS, but rather in the VPC.


## Key-terms
**VPC**

In AWS, a VPC (Virtual Private Cloud) is a virtual network that allows you to launch and configure resources such as EC2 instances, databases, and load balancers in a logically isolated section of the AWS cloud.

Think of it as your own private data center within the AWS cloud, where you can create subnets, define routing tables, and configure security groups to control traffic flow.

**NACL**

In AWS, a NACL (Network Access Control List) is a security layer that acts as a firewall for your VPC.

It controls traffic in and out of subnets by allowing or denying traffic based on IP addresses, protocols, and port numbers.

Think of it as a traffic cop for your VPC, checking every packet of data to make sure it meets the rules you've set.

Unlike security groups, which are instance-level firewalls, NACLs are subnet-level firewalls that apply to all instances in the subnet.



## Opdracht
- Study Security Groups in AWS
- Study Network Access Control Lists in AWS

### Gebruikte bronnen
ChatGPT

### Ervaren problemen
none
### Resultaat
N/A
