#!/bin/bash -e
#
# deploy - First-time packaging and deployment.
#

	source config.sh

    source package.sh
	
	set -x

	aws lambda create-function \
		--function-name $function \
		--runtime python2.7 \
		--handler hello.handler \
		--description "hello world lambda" \
		--role arn:aws:iam::$my_id:role/$lambda_role \
		--zip-file  fileb://$lambda_zip_file

#remove locally
	rm $lambda_zip_file