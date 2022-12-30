# Import Libraries
from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage
from prettytable import PrettyTable

import re
import os
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'univ-pertahanan-poc-59fedef57d83.json'

# Set your Processor ID
processor_id = "ecf99942554dfb65"  # TODO: Replace with a valid Processor ID 

# Set your variables
project_id = "universitas-pertahanan-poc"
project_id = project_id[0]
location = 'us'           # Replace with 'eu' if processor does not use 'us' location
"""
gcs_input_bucket  = project_id+"_doc_ai_async"   # Bucket name only, no gs:// prefix
gcs_input_prefix  = "input/"                     # Input bucket folder e.g. input/
"""
gcs_input_bucket  = 'universitas-pertahanan-poc'   # Bucket name only, no gs:// prefix
gcs_input_prefix  = "rapor-file/"                     # Input bucket folder e.g. input/


gcs_output_bucket = 'universitas-pertahanan-poc'   # Bucket name only, no gs:// prefix
gcs_output_prefix = "output/"                    # Input bucket folder e.g. output/
timeout = 100000

# Define Google Cloud client objects
client_options = {"api_endpoint": "{}-documentai.googleapis.com".format(location)}
client = documentai.DocumentProcessorServiceClient(client_options=client_options)
storage_client = storage.Client()

# Create input configuration
blobs = storage_client.list_blobs(gcs_input_bucket, prefix=gcs_input_prefix)
input_configs = []
print("Input Files:")
for blob in blobs:
    #print(blob.name)
    if re.findall(".pdf", blob.name):
        source = "gs://{bucket}/{name}".format(bucket = gcs_input_bucket, name = blob.name)
        print(source)
        input_config = documentai.types.document_processor_service.BatchProcessRequest.BatchInputConfig(
            gcs_source=source, mime_type="application/pdf"
        )
        input_configs.append(input_config)

# Create output configuration
destination_uri = f"gs://{gcs_output_bucket}/{gcs_output_prefix}"
output_config = documentai.types.document_processor_service.BatchProcessRequest.BatchOutputConfig(
    gcs_destination=destination_uri
)

# Create the Document AI API request
name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
request = documentai.types.document_processor_service.BatchProcessRequest(
    name=name,
    input_configs=input_configs,
    output_config=output_config,
)

# Start the batch (asynchronous) API operation 
operation = client.batch_process_documents(request)
# Wait for the operation to finish
operation.result(timeout = timeout)
print ("Batch process  completed.")

# Fetch list of output files
match = re.match(r"gs://([^/]+)/(.+)", destination_uri)
output_bucket = match.group(1)
prefix = match.group(2)
bucket = storage_client.get_bucket(output_bucket)
blob_list = list(bucket.list_blobs(prefix=prefix))



# Display detected text from asynchronous output JSON files
for i, blob in enumerate(blob_list):
    # If JSON file, download the contents of this blob as a bytes object.
    if ".json" in blob.name:
        blob_as_bytes = blob.download_as_bytes()
        document = documentai.types.Document.from_json(blob_as_bytes)
        print(f"Fetched file {i + 1}:{blob.name}")
        # print the text data output from the processor
        print(f"Text Data:\n {document.text}")
    else:
        print(f"Skipping non-supported file type {blob.name}")

# Display entity data from asynchronous output JSON files
for i, blob in enumerate(blob_list):
    # If JSON file, download the contents of this blob as a bytes object.
    if ".json" in blob.name:
        blob_as_bytes = blob.download_as_bytes()
        document = documentai.types.Document.from_json(blob_as_bytes)
        print(f"Fetched file {i + 1}:{blob.name}")
        # print the entity data output from the processor
        if 'entities' in dir(document):
            entities=document.entities
            table = PrettyTable(['Type', 'Value', 'Confidence'])
            entities_found = 0
            for entity in entities:
               entity_type = entity.type_
               value = entity.mention_text
               confidence = round(entity.confidence,4)
               table.add_row([entity_type, value, confidence])
            print(table)   
        else:
            print('No entity data returned by the Document AI processor for file'+blob.name)
    else:
        print(f"Skipping non-supported file type {blob.name}")