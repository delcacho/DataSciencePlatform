export NAME=k8s.dev.bayescluster.com
export KOPS_STATE_STORE=s3://delcachokops
dscacheutil -flushcache
kops validate cluster --name $NAME --wait 1800s
