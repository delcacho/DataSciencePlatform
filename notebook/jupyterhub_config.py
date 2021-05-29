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
#c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
#c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
from oauthenticator.github import GitHubOAuthenticator
c.JupyterHub.authenticator_class = GitHubOAuthenticator
c.Spawner.debug = True
c.Spawner.env_keep = ['PATH', 'MLFLOW_TRACKING_URI', 'JAVA_HOME', 'HADOOP_HOME', 'MASTER', 'PYTHONPATH', 'PYSPARK_DRIVER_PYTHON','PYSPARK_DRIVER_PYTHON_OPTS','PYSPARK_PYTHON','SPARKMONITOR_UI_HOST','SPARKMONITOR_UI_PORT','LC_ALL','LANG','DOCKER_HOST','DASK_SCHEDULER_ADDRESS','KUBERNETES_SERVICE_HOST','KUBERNETES_SERVICE_PORT', 'MLFLOW_PYTHON_BIN', 'MLFLOW_BIN']
#c.PAMAuthenticator.open_sessions = False
c.JupyterHub.ssl_key = 'jhub.key'
c.JupyterHub.ssl_cert = 'jhub.crt'
c.JupyterHub.port = 443
#c.JupyterHub.base_url = '/ide'
c.Spawner.default_url = '/lab'
c.Spawner.notebook_dir = '~/notebooks'

def pre_spawn_hook(spawner):
    spawner.log.info("Hello from the spawn hook")
    username = spawner.user.name
    spawner.log.info("Prespawn {}".format(username))
    try:
        import pwd
        pwd.getpwnam(username)
    except KeyError:
        import subprocess
        import os
        import grp
        import getpass
        spawner.log.info("Key error! {}".format(username))
        subprocess.check_call(['useradd', '-ms', '/bin/bash', username])
        uid = pwd.getpwnam(username).pw_uid
        gid = grp.getgrnam(username).gr_gid
        os.mkdir("/home/"+username+"/notebooks")
        os.chown("/home/"+username+"/notebooks",uid,gid)
        os.system("sudo -u "+username+" -E /usr/local/hadoop/bin/hdfs dfs -mkdir /user/"+username) 

c.Spawner.pre_spawn_hook = pre_spawn_hook
