# Use the following kfctl configuration file for existing cluster
export CONFIG_URI="https://raw.githubusercontent.com/kubeflow/manifests/v1.0-branch/kfdef/kfctl_k8s_istio.v1.0.2.yaml"

# Set an environment variable for your cluster name
export KF_NAME=k8s.dev.bayescluster.com

# Set the path to the base directory where you want to store one or more
# Kubeflow deployments. For example, /opt/.
# Then set the Kubeflow application directory for this deployment.
export BASE_DIR=.
export KF_DIR=${BASE_DIR}/${KF_NAME}


mkdir -p ${KF_DIR}
cd ${KF_DIR}
kfctl apply -V -f ${CONFIG_URI}
