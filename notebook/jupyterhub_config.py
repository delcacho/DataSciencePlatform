#from nb2kg import managers

c = get_config()
c.InteractiveShellApp.extensions = [
    'rise'
]
#c.InteractiveShellApp.exec_lines = [
#    "from dask.distributed import Client",
#    "client = Client('scheduler:8786')",
#    "import os",
#    "os.environ['MODIN_ENGINE'] = 'dask'",
#    "import modin.pandas as pd"
#]
c.Authenticator.admin_users = {'admin'}
c.LocalAuthenticator.create_system_users = True
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.Spawner.debug = True
c.Spawner.env_keep = ['PATH', 'MLFLOW_TRACKING_URI', 'JAVA_HOME', 'HADOOP_HOME', 'MASTER', 'PYTHONPATH', 'PYSPARK_DRIVER_PYTHON','PYSPARK_DRIVER_PYTHON_OPTS','PYSPARK_PYTHON','SPARKMONITOR_UI_HOST','SPARKMONITOR_UI_PORT','LC_ALL','LANG']
c.PAMAuthenticator.open_sessions = False
c.JupyterHub.ssl_key = 'jhub.key'
c.JupyterHub.ssl_cert = 'jhub.crt'
c.JupyterHub.port = 443
#c.GatewayClient.url = 'http://enterprise-gateway.enterprise-gateway.svc.cluster.local:8888'
#c.JupyterHub.base_url = '/ide'
c.Spawner.default_url = '/lab'
c.Spawner.notebook_dir = '~/notebooks'
