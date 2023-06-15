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