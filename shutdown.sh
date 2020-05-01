export AWS_ACCESS_KEY_ID="AKIAUMRLZOPXDQIC543W"
export AWS_SECRET_ACCESS_KEY="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"
export KOPS_STATE_STORE=s3://delcachokops
export NAME=k8s.dev.bayescluster.com

aws iam detach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam detach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam detach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::301813298158:policy/SagemakerExecutionPolicy
aws iam detach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::301813298158:policy/AccessToECR
aws iam detach-role-policy --role-name nodes.k8s.dev.bayescluster.com --policy-arn arn:aws:iam::aws:policy/IAMReadOnlyAccess
kops delete cluster $NAME --yes
