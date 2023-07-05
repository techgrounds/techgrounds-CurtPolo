# Week 1 - Diagram Stage 1
I made the decision to do the following:
- removed the multiple region aspect of the first design, because not only was it unessassary costs, but also the main target group and employees are all located in Netherlands.

- I decided to use a transit gateway instead of VPC peering connection based on the following findings:
1. Scalability: AWS Transit Gateway is highly scalable and can handle a large number of VPC connections. If you anticipate the need to connect multiple VPCs in the future or have plans for further expansion, Transit Gateway provides a centralized and scalable solution.

2. Simplified Management: Transit Gateway allows you to manage the network connections between your VPCs centrally. You can control routing, security, and monitoring from a single location, making it easier to maintain and troubleshoot your network infrastructure.

3. Cost-Effectiveness: AWS Transit Gateway can be a cost-effective solution compared to setting up and managing individual VPC peering connections. With Transit Gateway, you pay for the data processed through the gateway, whereas with VPC peering, you incur costs for each peering connection. If you have multiple VPCs to connect or anticipate frequent changes in your network architecture, the cost savings of Transit Gateway can be significant.

4. Additional Features: AWS Transit Gateway offers additional features such as integration with AWS Direct Connect, support for VPN connections, and the ability to connect to on-premises networks. These features provide flexibility and expandability options for your network architecture.

# Week 2 - Diagram Stage 2
I made the decision to make some changes to my infrastructure diagram.

- I decided to place my database in the private subnet of my web-server VPC. The reason is as followed:
    1. Reduced network latency: Placing your database in the same VPC as your web server reduces network latency. The communication between your web server and the database will be faster because they are located in the same network environment.

    2. Simplified security configuration: By placing the database in the same VPC as your web server, you can simplify your security configuration. You can set up security groups or network ACLs (Access Control Lists) within the same VPC to control access between the web server and the database. It reduces the complexity of managing security rules across multiple VPCs.

    3. Private subnet advantages: Placing the database in a private subnet within the same VPC provides an additional layer of security. The private subnet is not directly accessible from the internet, reducing the attack surface and protecting your database from unauthorized access.

    4. Efficient data transfer: If your web server and database are in the same VPC, data transfer between them doesn't incur data transfer costs. AWS typically charges for data transfer between different VPCs or over the internet, so keeping them in the same VPC can save costs, especially if you have significant data transfer between the web server and the database.

# Week 3 - Workflow
I was thinking about adding a stack for each service being created and then making a class for them now. But I decided that it should be considered a way to make my code more tidy. So I rather have a fully working code first then if I have time, split everything up to make it more organized

# Week 4 - Workflow
Due to the fact that I have been absolutely stuck with deployment errors related to my structure, NACL and Security Group. I decided to take the approach of a colleagues husband which is more expierienced in IT and restructred my code to avoid dependency issues and also I made everything into a comment and uncomment and deployed everything one by one step by step to find out exactly where my problems are.

I managed to do this successfully at the start of the week. So now I have no previous deployment errors.

My main error I was receiving was that my two security groups can't reference each other because they are in two different VPCs. (Casper did indicate that it could be a dependency issue)

I found a way around it by adding the cidr of the subnet my management server is on instead of the security group, as seen below.

## Allow SSH from management server to web server
        web_server_sg.add_ingress_rule(
            ec2.Peer.ipv4("10.20.20.64/26"),  # Replace this with the CIDR block of the management server's subnet
            ec2.Port.tcp(22),
            "Allow SSH from management server"
        )


# Week 5 - Diagram Stage 3
Due to version 1.1 there will be some changes to the diagram.

- My web server will be moved to a private subnet with egress
- A load balancer will be placed in the public subnet of my web vpc and act as proxy to my web server
- My management server will be on a public subnet and be able to SSH to my web server via the transit gateway.

# Week 6