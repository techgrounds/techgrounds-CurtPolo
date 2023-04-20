# Detection, Response and Analysis
**Detection** refers to the process of identifying or discovering a problem or issue. In the context of cybersecurity, detection involves identifying potential security breaches or attacks on computer systems and networks.

**Response** refers to the actions taken in response to a detected problem or issue. In the context of cybersecurity, response involves taking immediate steps to mitigate the effects of a security breach or attack and prevent further damage or compromise.

**Analysis** refers to the process of examining and evaluating information in order to gain a better understanding of it. In the context of cybersecurity, analysis involves studying the details of security breaches or attacks in order to identify the root cause, the scope of the problem, and potential solutions for preventing similar incidents in the future.

## Key-terms
**Malware**

Malware is a type of software that is designed to cause harm to a computer system, network, or device. It can be used to steal sensitive information, disrupt normal operations, or gain unauthorized access to a system. Malware can come in many forms, including viruses, worms, Trojan horses, and ransomware, and is often spread through email attachments, malicious websites, or infected software downloads.

**IDS**

Intrusion Detection Systems (IDS) are computer security systems that monitor networks or computer systems for signs of unauthorized access or malicious activity. They analyze network traffic or system logs to identify patterns or anomalies that could indicate a security breach or attack. IDS can be either network-based or host-based, with network-based IDS monitoring network traffic and host-based IDS monitoring system logs and events on individual computers. When an intrusion is detected, IDS can alert system administrators or take automated actions to prevent further damage or compromise.

**IPS**

Intrusion Prevention Systems (IPS) are computer security systems that monitor networks or computer systems for signs of unauthorized access or malicious activity and take automated actions to prevent the intrusion. IPS work similarly to Intrusion Detection Systems (IDS) but they are proactive in nature and have the capability to prevent an attack in real-time, rather than just detecting it. IPS can be either network-based or host-based, and can block suspicious traffic or take other actions such as quarantining a compromised system. IPS are often used in conjunction with firewalls and antivirus software to provide comprehensive network security.

**Disaster Recovery Plan**

A disaster recovery plan is a documented process for restoring important business functions after a natural or man-made disaster such as a flood, fire, or cyber attack. The plan outlines steps to be taken to minimize damage, assess the situation, and restore normal operations as quickly as possible. It includes measures such as data backups, alternative communication systems, and emergency procedures. A disaster recovery plan helps organizations prepare for unexpected events and ensures that they are able to recover from disasters and resume normal operations with minimal disruption.

**Cold Backup**

Cold backup is a type of data backup process where a backup copy of important data is created and stored offline in a separate location, such as an external hard drive or tape backup. This backup is not connected to the system or network and is not updated regularly, so it can become outdated if it is not periodically refreshed. In the event of a disaster or data loss, the cold backup can be used to restore the data and resume normal operations. Cold backups are considered a less efficient backup method than hot backups, which are updated in real-time and stored on active systems, but they provide a higher level of security against malware or cyber attacks that could corrupt active data.

**Redundant Site**

A redundant site is a backup location or facility that is available in case the primary location or facility becomes unavailable. It is often used to ensure continuity of business operations in the event of a natural disaster, power outage, or other emergency situation. The redundant site typically has the same equipment, resources, and data as the primary location, and can take over operations seamlessly with minimal downtime. Redundant sites can be physical locations such as a secondary data center or virtual sites that are hosted in the cloud. The use of a redundant site is a key part of disaster recovery planning and helps to ensure that critical business operations can continue even in the face of unexpected events.

**RPO**

Recovery Point Objective (RPO) is a measure of how much data loss is acceptable in the event of a disaster or system failure. It represents the maximum amount of time between data backups or snapshots, and determines the point in time to which data must be restored to ensure that the organization can resume normal operations. For example, if an organization has an RPO of 1 hour and a data backup is taken every hour, then in the event of a disaster, data can be restored to no more than 1 hour before the failure occurred. The RPO is an important part of disaster recovery planning and helps organizations to determine how frequently data backups should be taken in order to meet their recovery goals.

**RTO**

Recovery Time Objective (RTO) is a measure of how long it takes to restore critical business operations after a disaster or system failure. It represents the maximum allowable downtime for the organization, and determines the time frame within which systems and data must be restored to ensure that the organization can resume normal operations. For example, if an organization has an RTO of 4 hours, then all critical systems and data must be restored within 4 hours of a disaster or failure in order to minimize the impact on the business. The RTO is an important part of disaster recovery planning and helps organizations to prioritize recovery efforts and allocate resources in order to meet their recovery goals.


**Hack Response Strategies**

- Hack response strategies are the set of procedures and plans that organizations follow to identify and respond to cybersecurity incidents, including hacks and other types of cyber attacks.
- Effective hack response strategies can minimize the damage caused by an attack, prevent further breaches, and help organizations return to normal operations as quickly as possible.
- Hack response strategies typically include incident detection, containment, investigation, and recovery.
- Incident detection involves monitoring systems and network traffic for signs of suspicious activity, such as unexpected logins or network traffic patterns.
- Containment involves isolating affected systems or networks to prevent the spread of the attack and minimize the damage caused.
- Investigation involves determining the nature and scope of the attack, including identifying the attacker and the methods used.
- Recovery involves restoring affected systems and data to their normal state and verifying that the system is secure and free of vulnerabilities.

**Hack Response Strategies Examples**

- Incident response plans: These are formalized plans that outline the steps that organizations should take in the event of a cybersecurity incident.
- Forensic analysis: This involves collecting and analyzing digital evidence to identify the attacker and the methods used.
- Backup and recovery plans: These plans ensure that critical data and systems can be restored quickly and efficiently after an attack.
- Penetration testing: This involves simulating a hack or cyber attack to identify vulnerabilities and weaknesses in an organization's systems and networks.
- Security training and awareness programs: These programs educate employees and other stakeholders on how to recognize and prevent cybersecurity incidents, as well as how to respond effectively in the event of an attack.

**System Hardening**

Systems hardening is the process of securing computer systems by minimizing potential vulnerabilities and reducing the attack surface available to potential attackers. It involves taking steps to ensure that only necessary services and applications are running on a system, removing unnecessary software and services, and applying security updates and patches to operating systems and applications.

The goal of systems hardening is to make it more difficult for attackers to gain unauthorized access to a system, steal data, or cause damage. By reducing the attack surface and ensuring that systems are properly configured and secured, organizations can improve their overall security posture and better protect against cyber attacks.

**System Hardening Examples**

- Configuring firewalls to restrict network traffic to only necessary ports and protocols
- Disabling unnecessary services and applications
- Enabling security features such as encryption and access controls
- Implementing strong authentication and password policies
- Applying security patches and updates to operating systems and applications
- Regularly monitoring and reviewing system logs for signs of suspicious activity

**Disaster Recovery Options**

1. Cold backup: This involves creating a backup of data and system configurations, but keeping it offline and disconnected from the network. In the event of a disaster, the organization would need to physically transfer the backup to the affected system and restore it. This can take a significant amount of time, but it is a cost-effective option for organizations with limited resources.

2. Warm backup: This involves creating a backup of data and system configurations, but keeping it at a remote location that is connected to the network. In the event of a disaster, the organization can quickly switch to the backup system and restore the data. This is a faster option than cold backup, but it still requires some downtime and data loss may occur.

3. Hot backup: This involves creating a real-time backup of data and system configurations to a remote location that is continuously synchronized with the primary system. In the event of a disaster, the backup system can immediately take over and there is minimal downtime and data loss. However, this is the most expensive option as it requires significant investment in hardware and software.

4. Cloud disaster recovery: This involves using cloud-based services to back up data and applications, which can be quickly restored in the event of a disaster. This is a flexible and scalable option, but it may be more expensive than other options depending on the amount of data being stored and the frequency of backups.

5. Hybrid disaster recovery: This involves using a combination of the above options to create a disaster recovery plan that best suits the organization's needs and resources. For example, an organization might use a hot backup system for critical applications and a cloud-based backup for less critical data.

Overall, the choice of disaster recovery option will depend on the organization's budget, resources, and tolerance for downtime and data loss. It's important to regularly review and test the disaster recovery plan to ensure that it remains effective and up-to-date.


## Opdracht
- A Company makes daily backups of their database. The database is automatically recovered when a failure happens using the most recent available backup. The recovery happens on a different physical machine than the original database, and the entire process takes about 15 minutes. What is the RPO of the database?

- An automatic failover to a backup web server has been configured for a website. Because the backup has to be powered on first and has to pull the newest version of the website from GitHub, the process takes about 8 minutes. What is the RTO of the website?

### Gebruikte bronnen
ChatGPT

### Ervaren problemen
None

### Resultaat
**Task 1**

Seeing that in the first task we are speaking of RPO. I believe that I should look at the fact that the organization updates **DAILY**.

This leads me to believe that it is updated every 24 hours. So 24 hours / 1 day's worth of data loss is maximum amount that this organization is willing to accept.

So the RPO is 1 Day.

**Task 2**

Looking at the fact we are speaking of RTO and the whole process of powering on the backup site and it pulling the updates of GitHub takes 8 minutes. I would say the RTO is 8 minutes.



