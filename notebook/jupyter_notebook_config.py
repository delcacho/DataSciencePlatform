import os

c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from dask.distributed import Client",
    "client = Client('scheduler:8786')",
    "import os",
    "os.environ['MODIN_ENGINE'] = 'dask'",
    "import modin.pandas as pd",
]
#c.GatewayClient.url = 'http://enterprise-gateway.enterprise-gateway.svc.cluster.local:8888'
#c.NotebookApp.contents_manager_class = "jupytext.TextFileContentsManager"
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
