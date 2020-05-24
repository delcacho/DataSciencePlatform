FROM jupyter/base-notebook:lab-2.0.1

USER root
RUN apt-get update \
  && apt-get install -yq --no-install-recommends graphviz git build-essential \
     build-essential texlive-latex-base texlive-fonts-recommended texlive-xetex \
     texlive-fonts-extra texlive-latex-extra libgsl-dev libatlas-base-dev gfortran
RUN sudo apt-get purge openjdk* \
  && apt-get install -yq openjdk-8-jdk-headless ca-certificates-java \
  && apt-get -yqq install docker.io maven curl libcurl4-openssl-dev software-properties-common \
     libxml2-dev libssl-dev vim iputils-ping libopenblas-dev \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 51716619E084DAB9
RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran40/'
RUN apt update && apt install -yq r-base r-base-core r-recommended r-base-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Spark dependencies
ENV APACHE_SPARK_VERSION=2.4.5 \
    HADOOP_VERSION=2.7

# Using the preferred mirror to download the file
RUN cd /tmp && \
    wget -q $(wget -qO- https://www.apache.org/dyn/closer.lua/spark/spark-${APACHE_SPARK_VERSION}/spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz\?as_json | \
    python -c "import sys, json; content=json.load(sys.stdin); print(content['preferred']+content['path_info'])") && \
    echo "2426a20c548bdfc07df288cd1d18d1da6b3189d0b78dee76fa034c52a4e02895f0ad460720c526f163ba63a17efae4764c46a1cd8f9b04c60f9937a554db85d2 *spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" | sha512sum -c - && \
    tar xzf spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -C /usr/local --owner root --group root --no-same-owner && \
    rm spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz
RUN cd /usr/local && ln -s spark-${APACHE_SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark

ENV SPARK_HOME=/usr/local/spark
ENV MASTER=spark://spark-master-svc:7077
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip
ENV SPARK_OPTS="--driver-java-options=-Xms1024M --driver-java-options=-Xmx4096M --driver-java-options=-Dlog4j.logLevel=info"

#USER $NB_USER
RUN conda install python=3.6.9
RUN pip install h2o_pysparkling_2.4  colorama ipykernel portalocker \
    causal_impact modin ipyparallel hyperopt psycopg2-binary \
    nbconvert mlflow  ipywidgets jupyterlab_latex 
RUN pip install jupyter_helpers dvc seaborn spacy sqlalchemy flask
RUN pip install tensorflow-cpu tensorflow-gpu
RUN pip install --pre jupyter-lsp
RUN pip install jupytext --upgrade
RUN pip install jupyterlab==2.1.1
RUN pip install --pre jupyterlab-git==0.20.0rc0
RUN pip install python-language-server[all]
RUN pip install matplotlib xgboost lightgbm keras psutil seldon-core alibi
RUN pip install ml-versioning-tools dask-kubernetes sqlalchemy-redshift PyHive PyAthena pydruid impyla pinotdb sqlalchemy-clickhouse gsheetsdb gsheets \
 pybigquery pymssql snowflake-sqlalchemy kylinpy \
    sqlalchemy-pytds snowflake-sqlalchemy jupyter_contrib_nbextensions
RUN pip install pyspark kubernetes jupyter-archive 
RUN pip install jupyter-offlinenotebook nbresuse[resources] sdnotify
#RUN pip install jupyterlab-sparkmonitor
COPY jupyterlab-sparkmonitor/ /usr/local/jupyterlab-sparkmonitor/
RUN chmod -R 777 /usr/local/jupyterlab-sparkmonitor/
WORKDIR /usr/local/jupyterlab-sparkmonitor
RUN pip install -e .

RUN conda install --yes \
    -c conda-forge \
    -c damianavila82 \
    jupyterhub \
    ipympl \
    python-blosc \
    cytoolz \
    dask==2.11.0 \
    lz4 \
    nomkl \
    numpy \
    pandas \
    s3fs==0.4.0 \
    gcsfs==0.6.0 \
    pivottablejs \
    scikit-learn==0.22.1 \
    dask-ml \
    TPOT==0.11.1 \
    joblib==0.14.1 \
    stopit==1.1.2 \
    nose==1.3.7 \
    deap==1.3.1 \
    tqdm \
    jupyter-server-proxy==1.2.0 \ 
    dask-labextension \
    python-graphviz \
    && conda clean -tipsy \
    && jupyter lab clean \
    && jlpm cache clean \
    && npm cache clean --force \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs
#RUN conda install -n python_env ipykernel
#RUN conda install -n r_env r-irkernel

#RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager dask-labextension@1.0.1 @jupyterlab/hub-extension jupyterlab-drawio @jupyterlab/latex
#RUN jupyter serverextension enable jupyterlab_sql --py --sys-prefix
# @jupyterlab/dataregistry-extension

RUN mkdir -p /home/jovyan/.local/share/jupyter/kernels
RUN chown jovyan:users -R /home/jovyan/.local
USER jovyan 

RUN npm install -g ijavascript
RUN ijsinstall
USER root

# Create the /opt/app directory, and assert that Jupyter's NB_UID/NB_GID values
# haven't changed.
RUN mkdir /opt/app \
    && if [ "$NB_UID" != "1000" ] || [ "$NB_GID" != "100" ]; then \
        echo "Jupyter's NB_UID/NB_GID changed, need to update the Dockerfile"; \
        exit 1; \
    fi


# Copy over the example as NB_USER. Unfortuantely we can't use $NB_UID/$NB_GID
# in the `--chown` statement, so we need to hardcode these values.
RUN mkdir -p /home/$NB_USER/.local/share/jupyter
RUN chmod 777 /home/$NB_USER/.local/share/jupyter
RUN chmod 777 /usr/local/lib/R/site-library
COPY --chown=1000:100 examples/ /home/$NB_USER/examples
COPY prepare.sh /usr/bin/prepare.sh
#COPY nbgrader_config.py /etc/jupyter/nbgrader_config.py
WORKDIR /opt/conda/lib/python3.7/site-packages
RUN jupyter labextension install jupyterlab-topbar-extension
#RUN ipcluster nbextension enable
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter labextension install jupyter-matplotlib
RUN jupyter labextension install jupyterlab-system-monitor
#RUN jupyter labextension install jupyterlab-topbar-text
RUN jupyter labextension install jupyterlab-logout
RUN jupyter labextension install jupyterlab-theme-toggle
RUN jupyter labextension install @lckr/jupyterlab_variableinspector
#RUN jupyter labextension install @mflevine/jupyterlab_html
#RUN jupyter labextension install jupyterlab_rise
#RUN jupyter nbextension install --sys-prefix --py nbgrader --overwrite
#RUN jupyter nbextension enable --sys-prefix --py nbgrader
#RUN jupyter serverextension enable --sys-prefix --py nbgrader
RUN jupyter serverextension enable --py jupyterlab_git
RUN jupyter nbextension enable --py jupytext
RUN jupyter nbextension enable codefolding/main
RUN jupyter labextension install jupyterlab_filetree
RUN jupyter contrib nbextension install --user
#RUN jupyter-nbextension enable hinterland/hinterland --sys-prefix
RUN jupyter-nbextension enable skip-traceback/main --sys-prefix
RUN jupyter-nbextension enable snippets_menu/main --sys-prefix
#RUN jupyter-nbextension enable toc2/main --sys-prefix
RUN jupyter labextension install @jupyterlab/latex 
#RUN jupyter labextension install jupyterlab-plotly
RUN jupyter labextension install @jupyterlab/codemirror
RUN jupyter labextension install @krassowski/jupyterlab-lsp
RUN jupyter labextension install @jupyterlab/toc
RUN jupyter nbextension enable --py jupyter_offlinenotebook --sys-prefix
RUN jupyter serverextension enable --py jupyter_offlinenotebook --sys-prefix
RUN jupyter labextension install /usr/local/jupyterlab-sparkmonitor # install the jupyterlab extension
RUN jupyter serverextension enable --py sparkmonitor
#RUN jupyter labextension install nbgather 
#RUN jupyter labextension install @liorbaber/jupyterlab-spark-ui-tab
#RUN jupyter serverextension install --py spark-ui-tab
#RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
COPY jupyter_notebook_config.py /etc/ipython/ipython_config.py
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py
COPY kernels/ /usr/local/share/jupyter/kernels/
RUN mkdir -p /usr/local/share/jupyter/kernels/
RUN jupyter lab build
RUN jlpm cache clean
RUN npm cache clean --force

RUN useradd -ms /bin/bash admin
RUN useradd -ms /bin/bash hdfs

USER root
RUN R -e 'install.packages("IRkernel")' && R -e 'IRkernel::installspec(user = FALSE, displayname="R 4.0.0")' && R -e 'install.packages("languageserver")' && R -e 'install.packages("caret",dependencies = T)'
RUN R -e 'install.packages("randomForest")' && R -e 'install.packages("e1071")' && R -e 'install.packages("rpart")' && R -e 'install.packages("kernlab")' && R -e 'install.packages("nnet")' && R -e 'install.packages("dplyr")' &&  R -e 'install.packages("ggplot2")' && R -e 'install.packages("tidyr")'
RUN R -e 'install.packages("tm")' && R -e 'install.packages("MICE")' && R -e 'install.packages("igraph")' && R -e 'install.packages("ROCR")' && R -e 'install.packages("DataExplorer")'
RUN R -e 'install.packages("mlr")' && R -e 'install.packages("arules")' && R -e 'install.packages("mboost")' && R -e 'install.packages("party")' && R -e 'install.packages("mlflow")' 
RUN R -e 'install.packages("ranger")' && R -e 'install.packages("SparkR")' && R -e 'install.packages("sparklyr")' && R -e 'install.packages("xgboost")' && R -e 'install.packages("esquisse")' && R -e 'install.packages("RCurl")' && R -e 'install.packages("glmnet")'

ADD /sudoers.txt /etc/sudoers
RUN chmod 440 /etc/sudoers
USER admin
WORKDIR /home/admin
RUN mkdir notebooks
RUN echo 'admin:jupyter' | sudo chpasswd

#RUN sudo mount -o remount,rw /
USER $NB_USER
#USER admin
RUN  mkdir /home/$NB_USER/nbdata
WORKDIR /home/$NB_USER/nbdata
#COPY nbgrader_config.py /home/$NB_USER/nbdata
RUN mkdir /home/$NB_USER/notebooks
USER $NB_USER
COPY jhub.key /home/$NB_USER/jhub.key
COPY jhub.crt /home/$NB_USER/jhub.crt
RUN echo $NB_USER
USER root
RUN chmod 777 /home/$NB_USER/jhub.*
RUN wget https://ftp.cixug.es/apache/hadoop/common/hadoop-2.9.2/hadoop-2.9.2.tar.gz && tar -xzvpf hadoop-2.9.2.tar.gz && \
    mv hadoop-2.9.2 /usr/local/hadoop && rm hadoop-2.9.2.tar.gz
COPY core-site.xml /usr/local/hadoop/etc/hadoop/ 
RUN rm -rf /tmp/exchange
RUN mkdir /tmp/exchange
RUN mkdir -p /srv/nbgrader/exchange
RUN mkdir -p /home/admin/source
RUN mkdir -p /home/admin/.jupyter
COPY jupyter_notebook_config.py /home/admin/.jupyter/jupyter_notebook_config.py
RUN chmod ugo+rw /tmp/exchange
RUN chmod ugo+rw /home/admin/source
RUN chmod ugo+rw /home/admin/.jupyter
RUN chmod ugo+rw /srv/nbgrader/exchange
#USER $NB_USER

USER admin
WORKDIR /home/admin
RUN wget http://h2o-release.s3.amazonaws.com/sparkling-water/spark-2.4/3.30.0.1-1-2.4/sparkling-water-3.30.0.1-1-2.4.zip && unzip sparkling-water-3.30.0.1-1-2.4.zip && rm sparkling-water-3.30.0.1-1-2.4.zip
USER root
#RUN R -e 'remove.packages("h2o")'
RUN R -e 'install.packages("h2o", type = "source", repos = "http://h2o-release.s3.amazonaws.com/h2o/rel-zahradnik/1/R")'
RUN R -e 'install.packages("/home/admin/sparkling-water-3.30.0.1-1-2.4/rsparkling_3.30.0.1-1-2.4.tar.gz", repos=NULL, type="source")'
USER admin
ENV MLFLOW_TRACKING_URI=http://mlflow.bayescluster.com
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$SPARK_HOME/bin:$HADOOP_HOME/bin:$JAVA_HOME/bin:$PATH
#ENV JAVA_HOME=$(/usr/libexec/java_home -v 1.8) 
ADD https://repo1.maven.org/maven2/io/fabric8/kubernetes-client/4.9.1/kubernetes-client-4.9.1.jar $SPARK_HOME/jars
USER root
ENV MLFLOW_TRACKING_URI=http://mlflow.bayescluster.com
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH=$SPARK_HOME/bin:$PATH:$HADOOP_HOME/bin
ENV PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
ENV PYSPARK_DRIVER_PYTHON="jupyter"
ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook"
ENV PYSPARK_PYTHON=python3
ENV PATH=$SPARK_HOME/bin:$PATH:~/.local/bin:$JAVA_HOME/bin:$JAVA_HOME/jre/bin
ENV SPARKMONITOR_UI_HOST=spark-master-svc
ENV SPARKMONITOR_UI_PORT=80

ENTRYPOINT ["tini", "--", "/usr/bin/prepare.sh"]
#CMD ["start.sh", "jupyter", "lab"]
CMD ["jupyterhub", "--debug","--port=8000","-f","/etc/jupyterhub/jupyterhub_config.py", \
     "--ssl-key=/home/jovyan/jhub.key", \
     "--ssl-cert=/home/jovyan/jhub.crt"]
