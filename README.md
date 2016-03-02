# LambdaBasic
Basic template for an AWS Lambda program

Make sure youare running AT LEAST visual studio 2013, and have the following installed. 
* pip
* AWS CLI (command line)
* Python Tools for Visual Studio
* AWSToolkit VS Extension (optional but helpful)

Download the solution and open it in VS.  

Information on creating a lambda/python deployment package: 
http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

Look here for more details: https://blogs.aws.amazon.com/net/post/Tx381XNNQALP8BA/AWS-Lambda-Support-in-Visual-Studio

### Deployment using S3 and CloudFormation
1. Invoke package-s3 whcih packages the code into a zip file, then uploads the zip plus a CloudFormation template s3.  
1. From the AWS console, invoke the cloudformation template to create the Lambda (could be scripted). 
1. after that use update-from-s3.sh to invoke.

