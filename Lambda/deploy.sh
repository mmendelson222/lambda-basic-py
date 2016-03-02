#!/bin/bash -e
#
# package-s3 - Package a lambda function and upload it to S3
#              Also upload the clouldformation template.
#

	source config.sh

    source package.sh
	
	set -x

	aws lambda create-function \
		--function-name  $function \
		--runtime python2.7 \
		--handler hello.handler \
		--description "hello world lambda" \
		--role arn:aws:iam::$my_id:role/lambda-role \
		--zip-file  fileb://$lambda_zip_file

#remove locally
	rm $lambda_zip_file

