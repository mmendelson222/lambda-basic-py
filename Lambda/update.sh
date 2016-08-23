#!/bin/bash -e
#
# update - Update the lambda function 
#

	source config.sh

    source package.sh

	set -x

	aws lambda update-function-code \
		--function-name  $function \
		--zip-file  fileb://$lambda_zip_file \
		--handler $lambda_handler

#remove locally
	rm $lambda_zip_file