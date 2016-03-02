#!/bin/bash -e
#
# package - Package a lambda function into a zip file
#

# Create ZIP file and upload to S3

    7z a $lambda_zip_file *.py

	#7z a $lambda_zip_file node_modules/async/
    #zip -q -r $lambda_zip_file $lambda_function_file app.js
	
