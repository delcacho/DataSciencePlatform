echo "Installing Jenkins..."
kubectl apply -f ./jenkins/jenkins-secrets.yaml
kubectl apply -f ./jenkins/jenkins-credentials.yaml
helm install --wait jenkins stable/jenkins -f ./jenkins/jenkins-values.yaml
python3 ./jenkins/jenkinsinit.py
