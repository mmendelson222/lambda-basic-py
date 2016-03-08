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

### Deployment scripts: 

These scripts are not to be used OOTB.  Please review each one before using.  
1. config.sh - Settings used by multiple scripts. 
1. package.sh - Creates a zip file containing the python module and its dependencies. 
1. deploy.sh - First-time packaging and deployment.
1. update.sh - Lambda function code update only.