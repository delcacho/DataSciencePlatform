import warnings
warnings.filterwarnings("ignore")
from seldon_core.seldon_client import SeldonClient
import pandas as pd

data = pd.read_csv("wine-quality.csv")
data.head()

x_0 = data.drop(["quality"], axis=1).values[:1]
batch = x_0

sc = SeldonClient( \
   deployment_name="vino-malo",
   namespace="development", \
   gateway_endpoint="api.bayescluster.com",
   transport="rest",
   debug = True \
)

colnames = data.columns.tolist()
colnames.remove("quality")

for i in range(1,2000):
  r = sc.predict(data=batch, names=colnames, payload_type = "ndarray")
  print(r)

assert(r.success==True)


#r = sc.explain(data=batch, predictor="quality")
#print(r)
