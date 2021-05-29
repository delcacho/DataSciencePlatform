echo "Installing Jenkins..."
kubectl apply -f ./jenkins/jenkins-secrets.yaml
kubectl apply -f ./jenkins/jenkins-credentials.yaml
helm repo add jenkinsci https://charts.jenkins.io
helm repo update
helm install --wait jenkins -f ./jenkins/jenkins-values.yaml jenkinsci/jenkins
