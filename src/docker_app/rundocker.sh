#! /bin/bash
# For now, serious hacks to talk to AWS. We can remove this when all is dockerized

docker build . -t brew

IOT_CERT=$(cat $HOME/secrets/certs/e27d28a42b-certificate.pem.crt)
IOT_PRIVATE=$(cat $HOME/secrets/keys/e27d28a42b-private.pem.key)

AWS_ACCESS_KEY_ID=$(grep aws_access_key_id ~/.aws/credentials | cut -f 3 -d ' ')
AWS_SECRET_ACCESS_KEY=$(grep aws_secret_access_key ~/.aws/credentials | cut -f 3 -d ' ')


docker run -p 8080:8080 \
	-e FLASK_DEBUG=1 \
	-e FN_FLASK_SECRET_KEY=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1) \
	-e FN_AUTH_REDIRECT_URI=http://localhost:8080/google/auth \
	-e FN_BASE_URI=http://localhost:8080 \
	-e IOT_CERT="$IOT_CERT"  \
	-e IOT_PRIVATE="$IOT_PRIVATE" \
	-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
	brew
