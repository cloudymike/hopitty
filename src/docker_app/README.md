# Zappa tutorial

This is the current github repo and README for zappa with most of the details
required to understand zappa: https://github.com/zappa/Zappa

## Basic deploy
### Local testing
runlocal.sh will run the app locally. It will still talk to
AWS mqtt server and dynamodb, so it is not fully local.

### Update zappa
Run script update.sh if you have a working app at AWS. This will not
mess with the current setup, just update code. Make sure that you have
verified that you have good code by running locally first.

Currently all is run in dev.

### New deploy of zappa
Avoid undeploying and deploying as this will remove the environment and
requires extra rebuild.

For the initial deploy the script new_zappa.sh tries to cover all steps
reqired.

### Destroy zappa
The destroy_zappa.sh script will undeploy zappa and (sometime in the future)
remove all artifacts created

##TODO

###Hardcoded variables
* Regions for dynamo
* Random key is not random for googleauth
* Scan code for other variables and use environment variables for secrets and
configuration file for anything else

###AWS setup
Need to create a build script for AWS to setup all of the environment
from scratch
* IOT mqtt
* DynamoDB
* ACM certificates
* Google Auth
* Lambda / Zappa

#### Additional preparation required
Even before starting to run the deploy some setup needs to be done. See this
list as future work for improved automation.
* aws cli installed (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* AWS account with proper credentials setup.
  * To check, try run "aws lambda list-functions"
* Certificate created and arn available. (https://github.com/zappa/Zappa#deploying-to-a-domain-with-aws-certificate-manager)
* Dynamodb setup and connection info (as region) provided
  * See  directory "../dynamo" for setup
  * This directory also included a local version of dynamo for testing.
* mqtt setup and key/cert provided
  * See directory ../communicate for setup

## Learnings

### dynamodb

Make sure the database is in the right region

### flask
jsonify in flask can not handle decimal numbers. Go figure.
TypeError: Decimal('0') is not JSON serializable


### zappa
You need to install packages in environment and run pip freeze anytime you add an import.

For deploy fails check the logs on aws lambda
Example of a full path for an error:
  CloudWatch
  CloudWatch Logs
  Log groups
  /aws/lambda/zappa-app-dev
  2020/08/09/[$LATEST]233ecc2e55c64e0899e13d53548f9608

Do not mix deployer users. One may not be able to update the others info

### Lambda environment variables
The script lambdaenvironment sets up the environment variables required for lambda.
If you undeploy zappa you need to repopulate these after zappa has been deployed
The variables needs to be properly populated with secrets in this script, thus check
if the script is currently reading valid secrets.

The following environment variables needs to be set on Lambda for you project

FN_AUTH_REDIRECT_URI	https://subdomain.yourdomain.com/google/auth
FN_BASE_URI	https://subdomain.yourdomain.com
FN_CLIENT_ID	xxxsomeidzzz.apps.googleusercontent.com
FN_CLIENT_SECRET	yyyasecretttt
IOT_CERT=cut-and-paste-certlines
IOT_PRIVATE=cut-and-paste-keylines
