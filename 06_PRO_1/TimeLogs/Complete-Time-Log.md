# Monday June 5, 2023

## Daily Report
Focused on understanding the project tasks and preparing the tools to be used.

## Obstacles
- There was a lot of flow of information that needs to be structured. (Gave a overwhelming feeling)
- Had some difficulties preparing VS Code for the project. (installing the needed extentions and adding my credentials)
- Understanding exactly how to properly conduct the tasks.

## Solutions
- Get more information from the product owner tomorrow morning and break tasks up into sub-tasks.
- Found the correct youtube video which guided me through the process
- This will also be asked tomorrow during the meeting with the product owner

## Learnings
- I have learned at least how to use my credentials to login via VS Code.
- Found out that if the budget is passed it will be on my own account.
- Deadline must be made / planned for the end of the V1.0 not the end of the whole project.

# Tuesday June 6, 2023

## Daily Report
I focused on really starting with the two first user stories and preparing my working environment using CDK on VS Code.

## Obstacles
- I had issues knowing where to begin.
- I had issues with creating the project environment. I did not understand the concept of all the information I had to fill in.
## Solutions
- decided to use ChatGPT to help guide me through the best possible start points and help me structure things much better.
- I encountered a guide video which helped me create a sample application template. This way I can just delete what is build on the template but keep the structure of it so I can build my own application.

## Learnings
- I found out that I can just make a new directory using the terminal on VS Code
- I found the following useful commands: 
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

 # Wednesday June 7, 2023

## Daily Report
I reconstructed the AWS infrastructure diagram from a multi region to a single region.
## Obstacles
I am still at loss of the best way to construct it and which is more cost-effective
## Solutions
I suggested that as a team tomorrow we take a time to present our diagrams and fact check them.
## Learnings
I learned that I can replace the VPC peering with Transit Gateway. And that if I make the main communication between my two VPCs happen in the same AZ it won't cost data transfer charges

# Thursday June 8, 2023

## Daily Report
I continued with the construction of my infrastructure diagram and started to look for services that would fit my infrastructure.
## Obstacles
Difficulty picking the correct architecture 
## Solutions
I did not find a clear solution yet for it.
## Learnings
I do not feel like I learned much

# Friday June 9, 2023

## Daily Report 
I continued with the construction of my infrastructure diagram and made a decision to run with what I have and change things if needed.
## Obstacles
The obstacles I encountered was with setting up my CDK enviorement.
## Solutions
At the end of the day I reached out to Casper to assist with trouble shooting these issues on Monday
## Learnings
Not much to add when it came to learnings.

# Monday June 12, 2023

## Daily Report 
Today I tried to finally get the CDK envioronment to work properly.
## Obstacles
Was having various import errors. every solution on chatgpt gave more errors. Seems like it has conflifcts between V1 and V2
## Solutions
I deleted everything and recreated everything step by step. 
## Learnings
Not much to add when it came to learnings.

# Tuesday June 13, 2023

## Daily Report
I am pushing to have one errorless working code for today and figure out the best way to test it.
## Obstacles
Figuring out what is the best way to test my application without costs.
## Solutions
I found out I needed to install pytest in my test folder and create a 'pytest.ini' file in my root directory and configure it to be able to instructs pytest to look for test files that start with "test_" and have the ".py" extension.
## Learnings
I learned how to create the pytest.ini file, how to configure it for this specific use and the best practice of using the test folder to test changes in my code before adapting it to my main code.

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

# Thursday June 15, 2023

## Daily Report
I was able to successfully deploy my infrastructure with the correct CIDR and managed to attach my VPCs to a transit gateway.

I also made some changes to my infrastructure diagram.
## Obstacles
It had trouble finding the correct way to attach my VPCs to the transit gateway.
## Solutions
I received some documents from one of my colleagues which allowed me to combine the information in that document with chatGPT for a good working code.
## Learnings
I have not done so yet but I will have chatGPT break down the current code I have into smaller pieces and explain how the code works in each section.

# Monday June 19, 2023

## Daily Report
I attempted to figure out a way to structure my route tables better, by spending most of the days following a tutorial, but seeing it made me feel like I would have to change my entire structure I decided to discontinue with it.
## Obstacles
It was hard to truly figure out and follow the tutorial because I felt that some sections were skipped and some information were not explained clear enough.
## Solutions
I decided to skip this and focus on getting back to working for that MVP instead of making things tidy for now.
## Learnings
I would say I learned that I should prioritize better.

# Tuesday June 20, 2023

## Daily Report
I successfully managed to deploy my infrastructure, which currently consists of two VPCs, two AZs, four subnets, a ec2 linux web server, a MySQL RDS database, a transit gateway, two NAT gateways, a S3 bucket and a secret in the secrets manager.
## Obstacles
I received several errors in regards to both the way i coded my web-server and my database.

most of them had to do with how I pull the credentials out of secrets mananger and following the password guidelines.
## Solutions
I used chatGPT to troubleshoot each individual error code until I found the codes that were able to snyth and deploy without error.
## Learnings
I did learn that I can use a code to randomly generate a strong password and add the requirments the password needs to adhere by

# Wednesday June 21, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Thursday June 22, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Friday June 23, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Monday June 26, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Tuesday June 27, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Wednesday June 28, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Thursday June 29, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Friday June 30, 2023

## Daily Report

## Obstacles

## Solutions

## Learnings

# Monday July 3, 2023

## Daily Report
I was finally able to fix my issue with not being able to create a new route in a route table.

I now need to finish up some essential V1.0 stuff so I can start with V1.1
## Obstacles
- create a route in my route table to my transit gateway.
## Solutions
- I found the correct code to do so, modified it and also added a dependency to run that code only after my transit gateway is created.
## Learnings

# Tuesday July 4, 2023

## Daily Report
I created a load balancer security group and started the process of making my load balancer a proxy for my web server.

I also started to look into KMS
## Obstacles
I was having some issues with the process of doing an SSH to my load balancer and having it re-direct it to my web server
## Solutions
I was informed that I could attempt to use the transit gateway to allow my management server to SSH to my web server directly.
## Learnings
That it is possible to reach the private subnet of another VPC via the transit gateway. But also that SSH could be redirected via the load balancer if done properly

# Wednesday July 5, 2023

## Daily Report
I shifted my focus towards the load balancer and auto scaling.
## Obstacles
I encountered a lot of Attribute errors and Type Erros
## Solutions
I was not able to find a solution at the time
## Learnings
N/A

# Thursday July 6, 2023

## Daily Report
I was able to seemingly fix the auto-scaling and addapt the load balancer and also removed the previous 
web-server ec2 instance that I made, because it was no longer needed and was replaced by the load balancer.
## Obstacles
I encountered a lot of Attribute errors and Type Erros
## Solutions
Thanks to a classmate I was able to troubleshoot and find out that I was missing the autoscaling group name in one line of code.
## Learnings
To try solutions that are not indicated as directly as I would like

# Thursday July 7, 2023

## Daily Report
Today I attempted to make a SSL certificate and make a redirection from HTTP to my HTTPS.
## Obstacles
- All of a sudden my boto3 module no longer works.
- I am having issues with my certificate because it is asking for a domain name. So now my stack can't successfully deploy.
## Solutions
No solutions found as of yet
## Learnings
N/A

# Friday July 8, 2023

## Daily Report
Again I attempted to make a SSL certificate and make a redirection from HTTP to my HTTPS.
## Obstacles
Continued with these issues as well
- All of a sudden my boto3 module no longer works.
- I am having issues with my certificate because it is asking for a domain name. So now my stack can't successfully deploy.
## Solutions
No solutions found as of yet
## Learnings
N/A

# Monday July 10, 2023

## Daily Report
Again I attempted to make a SSL certificate and make a redirection from HTTP to my HTTPS.

I also worked on changing my management server from Linux to Windows and also establishing RDP connection.
## Obstacles
Continued with these issues as well
- All of a sudden my boto3 module no longer works.
- I am having issues with my certificate because it is asking for a domain name. So now my stack can't successfully deploy.
## Solutions
- Uninstalled boto3 and reinstalled it.
- I used a dummy/place holder domain name in a new certificate.
## Learnings
- I can use a place holder domain name for testing enviorment but it's not recommended for production.

# Tuesday July 11, 2023

## Daily Report
- I successfully tested my RDP connection between my PC and the management server.
- I am attempting to now SSH via my management server to my web server.
- I am testing my autoscaling group
## Obstacles
- my SSH to the web server via my management server times out.
## Solutions
- have not found a soultion for it yet
## Learnings
- I did learn I can use a Session Manager to achieve the same connection results without using SSH.
- I learned about the possiblity of using Instance Connect Endpoints.

# Wednesday July 12, 2023

## Daily Report
I continued with trying to resolve the issue with being able to SSH into the web server
## Obstacles
- my SSH to the web server via my management server times out.
## Solutions
- I made a new key pair seeing that for some reason the other was currupt.
## Learnings
- Learned from a colleague about a way I can have the key.pem file on my pc without having to copy it to the management server.

# Thursday July 13, 2023

## Daily Report
- Added the user date for the management server
- Made a security group for the RDS database
- came to the decision to use lambda to deploy the post deployment script
## Obstacles
- when attempting to deploy my stack with the database, my transit gateway route table was made before my transit gateway and everything failed.
## Solutions
- I moved the part of the code that creates the transit gateway further up in the stack.
## Learnings
- found out I can use lambda for the post deployment script instead of the s3 bucket.

# Friday July 14, 2023

## Daily Report
- Succesfully tested the connection to the database via my management server
- Looked into the lambda for the post deployment script
- attempted to find a way to create an interactive input for the admin IP
## Obstacles
- running into several errors everytime I attempt to make an input function.
## Solutions
- I have found no suitable solution for the input yet
## Learnings
N/A