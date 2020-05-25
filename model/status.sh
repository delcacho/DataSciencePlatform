kubectl get sdep --namespace development $1 -o json | jq .status
