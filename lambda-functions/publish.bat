set PATH=%PATH%;C:\Program Files\7-Zip\
set FuncName=%1
set Handler=%2
del index.zip 
cd lambdas 
7z a -r ..\index.zip *
cd .. 
aws lambda update-function-code --function-name %FuncName% --zip-file fileb://index.zip
aws lambda update-function-configuration --function-name %FuncName% --handler %Handler%