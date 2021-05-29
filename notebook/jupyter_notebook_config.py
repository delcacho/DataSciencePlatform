import os
  
c = get_config()
c.InteractiveShellApp.exec_lines = [
    "from dask.distributed import Client",
    "client = Client('scheduler:8786')",
    "import os",
    "os.environ['MODIN_ENGINE'] = 'dask'",
    "import modin.pandas as pd",
]
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.LatexConfig.latex_command = 'pdflatex'
c.NotebookApp.contents_manager_class = 'jupytext.TextFileContentsManager'
c.NotebookApp.ResourceUseDisplay.track_cpu_percent = True
c.MappingKernelManager.cull_idle_timeout = 600
