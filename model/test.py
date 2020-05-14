import warnings
warnings.filterwarnings("ignore")
from seldon_core.seldon_client import SeldonClient
import pandas as pd

data = pd.read_csv("wine-quality.csv")
data.head()

x_0 = data.drop(["quality"], axis=1).values[:1]
batch = x_0

sc = SeldonClient( \
   deployment_name="vino-del-gueno",
   namespace="none", \
   gateway_endpoint="api.bayescluster.com",
   gateway="ambassador",
   transport="rest",
   debug = True \
)

r = sc.predict(data=batch, names=data.columns.tolist(), payload_type = "ndarray", namespace="none")
print(r)

assert(r.success==True)
