import warnings
warnings.filterwarnings("ignore")
from seldon_core.seldon_client import SeldonClient
import pandas as pd

data = pd.read_csv("wine-quality.csv")
data.head()

x_0 = data.drop(["quality"], axis=1).values[:1]
batch = x_0

sc = SeldonClient( \
   deployment_name="mlflow",namespace="staging", \
   gateway_endpoint="api.bayescluster.com",
   debug = True \
)

for i in range(0,1000):
   r = sc.predict(gateway="ambassador",transport="rest",data=batch, names=data.columns.tolist(),\
                  payload_type = "ndarray", gateway_endpoint="api.bayescluster.com")
   print(r)
assert(r.success==True)
