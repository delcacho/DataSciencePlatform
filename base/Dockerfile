FROM continuumio/miniconda3:4.7.12

RUN pip install \
    modin

RUN conda install --yes \
    -c conda-forge \
    python-blosc \
    cytoolz \
    dask==2.11.0 \
    scikit-learn==0.22.1 \
    TPOT==0.11.1 \
    dask-ml==1.2.0 \
    lz4 \
    nomkl \
    numpy==1.18.1 \
    pandas==0.25.3 \
    s3fs==0.4.0 \
    gcsfs==0.6.0 \
    joblib==0.14.1 \
    stopit==1.1.2 \
    nose==1.3.7 \
    deap==1.3.1 \
    tqdm==4.43.0 \
    tini==0.18.0 \
    jupyter-server-proxy==1.2.0 \ 
    && conda clean -tipsy \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs

COPY prepare.sh /usr/bin/prepare.sh

RUN mkdir /opt/app

ENTRYPOINT ["tini", "-g", "--", "/usr/bin/prepare.sh"]
