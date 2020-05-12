echo "Installing Superset..."
helm install --wait superset stable/superset
python3 superset/supersetinit.py
