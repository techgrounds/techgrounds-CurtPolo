# Subnetting
Subnetting is the process of dividing a large network into smaller sub-networks, called subnets. The primary purpose of subnetting is to improve network performance and security by reducing network traffic and isolating groups of devices.
## Key-terms
**LAN**

A LAN, or Local Area Network, is a computer network that covers a small geographic area, typically within a single building or campus. A LAN is used to connect computers, servers, printers, and other network devices together so that they can communicate with each other and share resources.

**Subnet Mask**

A subnet mask is a 32-bit number that is used to divide an IP address into two parts: the network part and the host part. 

**Prefix**

A network prefix, or simply prefix, is a notation used in IP networking to indicate the size of the network part of an IP address. The prefix is represented as a number that indicates the number of bits in the network part of the address. For example, a prefix of /24 indicates that the first 24 bits of the IP address represent the network part.

**CIDR notation**

CIDR notation, or Classless Inter-Domain Routing notation, is a compact way of representing IP addresses and their associated network prefixes. It is used to specify the network portion and host portion of an IP address, as well as the subnet mask, in a concise and standardized format.

For example IP address: 192.168.10.18 Submask: 255.255.255.0, can also be written as 192.168.10.18/24

IP address: 192.168.1.1 Submask: 255.255.0.0, can also be written as 192.168.1.1/16.

## Opdracht
Create a network architecture that meets the following requirements:

- 1 private subnet that can only be reached from within the LAN. This subnet must be able to accommodate a minimum of 15 hosts.

- 1 private subnet that has internet access through a NAT gateway. This subnet must be able to place at least 30 hosts (the 30 hosts does not include the NAT gateway).

- 1 public subnet with an internet gateway. This subnet must be able to place at least 5 hosts (the 5 hosts does not include the internet gateway).

Plaats de architectuur die je hebt gemaakt inclusief een korte uitleg in de Github repository die je met de learning coach hebt gedeeld.
### Gebruikte bronnen
ChatGPT

https://www.udemy.com/course/complete-networking-fundamentals-course-ccna-start/

### Ervaren problemen
[Geef een korte beschrijving van de problemen waar je tegenaan bent gelopen met je gevonden oplossing.]

### Resultaat
[Omschrijf hoe je weet dat je opdracht gelukt is (gebruik screenshots waar nodig).]



