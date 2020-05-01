kubectl delete all --all --all-namespaces
helm ls | awk '/DEPLOYED/ { print $1 }' | xargs -tn1 helm delete --purge 
