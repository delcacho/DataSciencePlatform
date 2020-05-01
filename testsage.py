import boto3
import json
import pandas as pd
from sklearn import datasets

wine_path = "https://raw.githubusercontent.com/databricks/mlflow-example-sklearn-elasticnet-wine/master/wine-quality.csv"
data = pd.read_csv(wine_path)

endpoint_name = "wine-deployment-goyeah"
print(endpoint_name)
runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='eu-east-1')

input_json = data.iloc[0,:].to_json()
print (input_json)

response = runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/json', Body=input_json)
print(response['Body'].read())
