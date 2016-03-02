#!/bin/bash -e
#
# config - settings for this lambda project. 
#

# Settings

    function=lambdabasic
    s3_bucket=mm-test-xfer
	s3_key=lambda/$function.zip
    s3_zip_file=s3://$s3_bucket/$s3_key
    s3_template_file=s3://$s3_bucket/cloudformation/$function.template
    lambda_zip_file=$function.zip
	my_id=847453500548

