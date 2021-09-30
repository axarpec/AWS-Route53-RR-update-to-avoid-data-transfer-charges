# AWS-Route53-RR-update-to-avoid-data-transfer-charges

Topology :
Topology consiste of 3 VPC where 2 VPC are having the same CIDR(all part of same region).
- VPC-ABC - 10.10.0.0/16(default domain)
- VPC-DEF - 10.20.0.0/16(custom domain with domain controllers in vpc-xyz)
- VPC-GHI - 10.30.0.0/16(default domain)
- VPC-XYZ - 10.10.0.0/16(VPC with AWS managed Domain Controller)

We have some serveres in VPC-ABC which needs to be accessed from the VPC-DEF.

VPC-DEF is having having EC2 instances which are acting as client which needs access of servers which are in VPC-ABC in cost effective way.

Additionally, VPC-DEF is having modified DHCP option set where we have custom domain where the domain controllers site in VPC XYZ.

Idea is to launch the Ec2 instances in VPC-ABC and VPC-DEF in same AZ and have communication over private IP to save data transfer cost. We can create VPC peering to achieve the same. But we still have to take care about the DNS part.

Problem : 
- While accessing the ec2 instance EC2 instances in VPC-EFC will have to use hostname to access Ec2 in VPC-ABC.
- DNS request for the ec2 instances in VPC-DEF goes to the Domain controller in VPC-XYZ.
- As VPC-ABC and VPC-XYZ are having same CIDR we cannot create vpc peering, hence the dns request for the ec2 instances in VPC-ABC will resolve to the public IP of ec2 instance. With that when Ec2 instances in VPC-DEF will access the resources of VPC-ABC, traffic will go to pubic IP, which will incure cost.

Solution :
- We will create VPC peering between VPC-GHI and VPC-ABC with DNS resultion enabled.
- Create lambda in VPC-GHI which performs the DNS resolution for the specific URL and keeps on checking the private IP of Ec2 instance.
- Create Private Hosted Zone associated with the VPC-XYZ where we can create a RR for that URL maping to the private IP which is in same az as client.
- In case of change in the IP, lambda will go ahead and make changes in the route53 private hosted zone to update the record.
- With this, domain controllers in VPC-XYZ will be able to resolve hostname of ec2 instance in VPC-ABC to the private IP. Which will eventually help resources in VPC-DEF to resolve the resources of VPC-ABC to resolve to private IP. Which will help us reduce the data transfer cost.

Instructions to lambda :

Triger for Lambda :
- You can have CloudWatch event to run it every 5 min or 1 min.

Here are the Env Variable that you will have to define while deploying this Lambda code :
- hosted_zone_id : Specify hosted zone id of private hosted zone for VPC-XYZ.
- record_name : Specify the record name/FQDN which needs to be monitored.

Here is the IAM policy which is required to run this lambda code :
- Along with default role where CW log access is given, you have to edit the role to have AmazonRoute53FullAccess.


*You can use the code from the file UpdateR53.py

Stay tuned for more developements on this project
