from google.cloud import documentai_v1beta3 as documentai
from google.cloud import storage
from prettytable import PrettyTable
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'univ-pertahanan-poc-59fedef57d83.json'

processor_id = 'ecf99942554dfb65' #TO Replace with a valid Processor ID   
    
project_id = 'universitas-pertahanan-poc'
location = 'us'           # Replace with 'eu' if processor does not use 'us' location
gcs_input_bucket  = project_id   # Bucket name only, no gs:// prefix
gcs_input_prefix  = "rapor-file/"                     # Input bucket folder e.g. input/
gcs_output_bucket = project_id   # Bucket name only, no gs:// prefix
gcs_output_prefix = "output/"                    # Input bucket folder e.g. output/
timeout = 300

client_options = {"api_endpoint": "{}-documentai.googleapis.com".format(location)}
client = documentai.DocumentProcessorServiceClient(client_options=client_options)
storage_client = storage.Client()

input_configs = []

blobs = storage_client.list_blobs(gcs_input_bucket)

input_configs = []
print("Input Files:")
for blob in blobs:
    print(blob)
    if ".pdf" in blob.name:
        source = "gs://{bucket}/{name}".format(bucket = gcs_input_bucket, name = blob.name)
        print(source)
        input_config = documentai.types.document_processor_service.BatchProcessRequest.BatchInputConfig(
            gcs_source=source, mime_type="application/pdf"
        )
        input_configs.append(input_config)

destination_uri = f"gs://{gcs_output_bucket}/{gcs_output_prefix}"
output_config = documentai.types.document_processor_service.BatchProcessRequest.BatchOutputConfig(
    gcs_destination=destination_uri
)

name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
request = documentai.types.document_processor_service.BatchProcessRequest(
    name=name,
    input_configs=input_configs,
    output_config=output_config,
)

operation = client.batch_process_documents(request)
# Wait for the operation to finish
operation.result(timeout=timeout)
print ("Batch process  completed.")