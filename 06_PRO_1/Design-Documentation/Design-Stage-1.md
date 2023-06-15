# Stage 1
I decided to go with this base design and add services that I could possibly use on the side at this point.

- I've added an application load balancer between the internet and my Web-Server VPC.
- Both VPCs will be in multiple AZs
- The two VPC will be connected to each other using a transit gateway.

(Please read the week 1 decision documentation for explanation on the changes)

![Alt text](../../00_includes/Project-Images/AWS-Project-Diagram-1.drawio.png)

# Stage 2
I made some key changes to my design by moving the database to the web server VPC and placing it in the private subnet.

(Please read the week 2 decision documentation for explanation on the changes)

![Alt text](../../00_includes/Project-Images/AWS-Project-Diagram-2.drawio.png)