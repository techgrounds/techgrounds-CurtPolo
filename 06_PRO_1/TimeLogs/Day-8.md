# Wednesday June 14, 2023

## Daily Report
Today I finally was able to successfully deploy an S3 bucket, VPC, public and private subnets and a NAT Gateway.
## Obstacles
I encountered several issues with the codes not working and having several errors.

I also found it hard to find good resources to explain this new version 2 way of doing things.
## Solutions
I managed to find the right code after breaking it down a bit more and using ChatGPT.

I also communicated with an Azure buddy for advice.
## Learnings
After receiving plenty of errors using the following.

" ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE) "

I managed to get the code to work by using

" ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_ISOLATED) "

which was later changed to

" ec2.SubnetConfiguration(name="private", cidr_mask=24, subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT) "

Thanks to my Azure colleague I was able to take her tip and break things down into much smaller tasks and reconstructing the whole code bit by bit.