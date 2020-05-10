c = get_config()
c.InteractiveShellApp.extensions.append('sparkmonitor.kernelextension')
c.InteractiveShellApp.exec_lines = [
    "from dask.distributed import Client",
    "client = Client('scheduler:8786')",
    "import os",
    "os.environ['MODIN_ENGINE'] = 'dask'",
    "import modin.pandas as pd",
]
