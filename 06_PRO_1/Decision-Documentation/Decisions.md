# Week 1 - Diagram Stage 1
I made the decision to do the following:
- removed the multiple region aspect of the first design, because not only was it unessassary costs, but also the main target group and employees are all located in Netherlands.

- I decided to use a transit gateway instead of VPC peering connection based on the following findings:
1. Scalability: AWS Transit Gateway is highly scalable and can handle a large number of VPC connections. If you anticipate the need to connect multiple VPCs in the future or have plans for further expansion, Transit Gateway provides a centralized and scalable solution.

2. Simplified Management: Transit Gateway allows you to manage the network connections between your VPCs centrally. You can control routing, security, and monitoring from a single location, making it easier to maintain and troubleshoot your network infrastructure.

3. Cost-Effectiveness: AWS Transit Gateway can be a cost-effective solution compared to setting up and managing individual VPC peering connections. With Transit Gateway, you pay for the data processed through the gateway, whereas with VPC peering, you incur costs for each peering connection. If you have multiple VPCs to connect or anticipate frequent changes in your network architecture, the cost savings of Transit Gateway can be significant.

4. Additional Features: AWS Transit Gateway offers additional features such as integration with AWS Direct Connect, support for VPN connections, and the ability to connect to on-premises networks. These features provide flexibility and expandability options for your network architecture.
