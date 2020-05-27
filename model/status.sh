kubectl get sdep --namespace staging $1 -o json | jq .status
