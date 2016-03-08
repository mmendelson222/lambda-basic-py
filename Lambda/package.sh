#!/bin/bash -e
#
# package - Create a zip file containing the python module and its dependencies. 
#

    7z a $lambda_zip_file *.py

	#7z a $lambda_zip_file node_modules/async/
    #zip -q -r $lambda_zip_file $lambda_function_file app.js