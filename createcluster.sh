export AWS_ACCESS_KEY_ID="AKIAUMRLZOPXDQIC543W"
export AWS_SECRET_ACCESS_KEY="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"
export KOPS_STATE_STORE=s3://delcachokops
export NAME=k8s.dev.bayescluster.com 

export NUM_WORKERS=5

aws s3api create-bucket \
    --bucket delcachokops \
    --region us-east-1

echo "Going to create cluster"
kops create cluster \
--name $NAME \
--api-loadbalancer-type public \
--zones us-east-1a \
--master-size t2.large \
--master-count 1 \
--node-size t2.large \
--node-count $NUM_WORKERS \
--dns-zone=dev.bayescluster.com \
--yes 

echo "Attaching policy rules"
aws iam attach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam attach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/IAMReadOnlyAccess
aws iam attach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::301813298158:policy/SagemakerExecutionPolicy
aws iam attach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::301813298158:policy/AccessToECR
aws iam update-assume-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-document  file://trust-policy.txt
