export AWS_ACCESS_KEY_ID="AKIAUMRLZOPXDQIC543W"
export AWS_SECRET_ACCESS_KEY="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"
export KOPS_STATE_STORE=s3://delcachokops
export NAME=k8s.dev.bayescluster.com

export NUM_WORKERS=5

kops create secret --name k8s.dev.bayescluster.com sshpublickey admin -i ~/.ssh/id_rsa.pub

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
--dns-zone=dev.bayescluster.com
