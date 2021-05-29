echo "Installing Superset..."
helm repo add superset https://apache.github.io/superset
helm repo update
helm install --wait superset superset/superset
python3 superset/supersetinit.py
