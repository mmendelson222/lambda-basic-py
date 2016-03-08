#!/bin/bash -e
#
# update - Update the lambda function 
#

	source config.sh

    source package.sh

	aws lambda update-function-code \
		--function-name  $function \
		--zip-file  fileb://$lambda_zip_file

#remove locally
	rm $lambda_zip_file