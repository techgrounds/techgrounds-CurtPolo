# Wednesday June 7, 2023

## Daily Report
I reconstructed the AWS infrastructure diagram from a multi region to a single region.
## Obstacles
I am still at loss of the best way to construct it and which is more cost-effective
## Solutions
I suggested that as a team tomorrow we take a time to present our diagrams and fact check them.
## Learnings
I learned that I can replace the VPC peering with Transit Gateway. And that if I make the main communication between my two VPCs happen in the same AZ it won't cost data transfer charges