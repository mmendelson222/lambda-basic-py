#!/bin/bash -e
#
# update - Update a lambda function 
#

	source config.sh

    source package.sh

	aws lambda update-function-code \
		--function-name  $function \
		--zip-file  fileb://$lambda_zip_file

#remove locally
	rm $lambda_zip_file




