# Simple Storage Service (S3)
AWS S3 (Simple Storage Service) is a cloud-based storage service provided by Amazon Web Services (AWS) that allows you to store and retrieve data and files on the internet. It provides highly scalable, durable, and secure storage that can be accessed from anywhere in the world through a simple web interface or API.

## Key-terms
S3 Standard
S3 Standard-IA
S3 One-zone IA
S3 Glacier
S3 Glacier Instant Retrieval
S3 Glacier Flexible Retrieval
S3 Glacier Deep Archive
Intelligent Tiering

## Opdracht
**Exercise 1**

- Create new S3 bucket with the following requirements:
Region: Frankfurt (eu-central-1)
- Upload a cat picture to your bucket.
- Share the object URL of your cat picture with a peer. Make sure they are able to see the picture.

**Exercise 2**

- Create new bucket with the following requirements:
Region: Frankfurt (eu-central-1)
- Upload the four files that make up AWS’ demo website.
- Enable static website hosting.
- Share the bucket website endpoint with a peer. Make sure they are able to see the website.


### Gebruikte bronnen
ChatGPT

### Ervaren problemen
Just had to get used to changing permission to Public for the objects and bucket.

### Resultaat
**Exercise 1**

Created S3 Bucket
![Alt text](../00_includes/Week-4-AWS/AWS-05-Bucket1.png)

Upload cat image
![Alt text](../00_includes/Week-4-AWS/AWS-05-Upload.png)

In order to share the cat image I had to take the following steps:

1. I had to click on my bucket name, select the permissions option and edit the "Block public access" settings.
![Alt text](../00_includes/Week-4-AWS/AWS-05-UnblockPA1.png)

2. In the "Block public access" settings I unchecked "Block all public access".
![Alt text](../00_includes/Week-4-AWS/AWS-05-UnblockPA2.png)

3. Then I had to go to the object in this case the cat picture and click on it's name. I then had to select permissions and click on "becket owner enforced".
![Alt text](../00_includes/Week-4-AWS/AWS-05-UnblockPA3.png)

4. I then have to enable ACLs.
![Alt text](../00_includes/Week-4-AWS/AWS-05-UnblockPA4.png)

5. After enabling ACL, I can click the checkbox infront of the object I want to make public, click the "Actions" drop down menu and select "Make public using ACL"
![Alt text](../00_includes/Week-4-AWS/AWS-05-UnblockPA5.png)

I then successfully shared my cat picture by clicking in the checkbox infront of it and then clicking "Copy URL".

![Alt text](../00_includes/Week-4-AWS/AWS-05-Cat.png)

**Exercise 2**

Create new bucket
![Alt text](../00_includes/Week-4-AWS/AWS-05-Bucket2.png)

Upload Demo Website Files
![Alt text](../00_includes/Week-4-AWS/AWS-05-Upload2.png)

To enable static website hosting I had to take the following steps:

1. After taking the steps to make everything **public**, I click on the bucket name and then "Properties". I scroll all the way to the bottom to find "Static website hosting" and choose "Edit"
![Alt text](../00_includes/Week-4-AWS/AWS-05-StaticWebHost.png)

2. I then enable "static website hosting", select "host a static website" and then add the index.html and error.html
![Alt text](../00_includes/Week-4-AWS/AWS-05-StaticWebHostSettings.png)

3. Now if I go to bucket name, properties and scroll down to "Static website hosting", I will see the option to copy the "Bucket website endpoint" URL.
![Alt text](../00_includes/Week-4-AWS/AWS-05-EndPoint.png)

I then posted the URL to my peers and it worked.
![Alt text](../00_includes/Week-4-AWS/AWS-05-Website.png)


