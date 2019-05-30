set PATH=%PATH%;C:\Program Files\7-Zip\
del index.zip 
cd lambdas 
7z a -r ..\index.zip *
cd .. 

aws lambda update-function-code --function-name classifyimage --zip-file fileb://index.zip
aws lambda update-function-code --function-name pageDataFunction --zip-file fileb://index.zip

aws lambda update-function-configuration --function-name classifyimage --handler api/classify_image.lambda_handler
aws lambda update-function-configuration --function-name pageDataFunction --handler api/get_page_data.lambda_handler