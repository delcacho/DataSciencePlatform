kubectl get sdep --namespace $2 $1 -o json | jq .status
