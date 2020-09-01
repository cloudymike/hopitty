# Zappa tutorial

## Learnings

### dynamodb

Make sure the database is in the right region

### flask
jsonify in flask can not handle decimal numbers. Go figure.
TypeError: Decimal('0') is not JSON serializable


## zappa
You need to install packages in environment and run pip freeze anytime you add an import.

For deploy fails check the logs on aws lambda
Example of a full path for an error:
  CloudWatch
  CloudWatch Logs
  Log groups
  /aws/lambda/zappa-app-dev
  2020/08/09/[$LATEST]233ecc2e55c64e0899e13d53548f9608

Do not mix deployer users. One may not be able to update the others info
