kubectl create secret generic seldon-init-container-secret \
    --from-literal=AWS_ACCESS_KEY_ID='AKIAUMRLZOPXLZIB7DXK' \
    --from-literal=AWS_SECRET_ACCESS_KEY='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' \
    --from-literal=AWS_ENDPOINT_URL='https://s3.us-east-1.amazonaws.com/' \
    --from-literal=USE_SSL=true --namespace development

kubectl create secret generic seldon-init-container-secret \
    --from-literal=AWS_ACCESS_KEY_ID='AKIAUMRLZOPXLZIB7DXK' \
    --from-literal=AWS_SECRET_ACCESS_KEY='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' \
    --from-literal=AWS_ENDPOINT_URL='https://s3.us-east-1.amazonaws.com/' \
    --from-literal=USE_SSL=true --namespace staging

kubectl create secret generic seldon-init-container-secret \
    --from-literal=AWS_ACCESS_KEY_ID='AKIAUMRLZOPXLZIB7DXK' \
    --from-literal=AWS_SECRET_ACCESS_KEY='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' \
    --from-literal=AWS_ENDPOINT_URL='https://s3.us-east-1.amazonaws.com/' \
    --from-literal=USE_SSL=true --namespace production
