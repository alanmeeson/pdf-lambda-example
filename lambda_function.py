import json
import boto3
import tempfile
import os
import camelot
import fitz


def lambda_handler(event, context):
    """The main function for AWS Lambda to invoke.
    
    This reads mock_report.pdf from an S3 bucket, extracts the table and the 
    text, and writes them into a DynamoDB table (as specified in the 
    function's DYNAMODB_TABLE environment variable).

    This expects to be given an S3 object creation event.
    """
    table_name = os.environ['DYNAMODB_TABLE']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Get the pdf file and process it
    s3 = boto3.client('s3')
    fileTemp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    try:
        s3.download_fileobj(
            bucket_name,
            object_key,
            fileTemp)
        fileTemp.close()

        record = process_pdf(fileTemp.name)
    finally:
        os.remove(fileTemp.name)

    record['filename'] = object_key

    # write the output to dynamodb
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)

    return {
        'statusCode': 200,
        'body': json.dumps(object_key)
    }


def process_pdf(filename):
    """Process the pdf file to extract the table and text.

    This function used PyMuPDF to parse the PDF and identify where on the 
    page the table can be found (also to extract all the text).
    It then uses camelot-py to extract the table from the PDF.

    Note: this is rather brittle in it's current state, and only works for
    the mock_report.pdf file.

    Args:
        filename: the path to the temporary pdf file downloaded from S3.
    
    Returns:
        A dict with the table and text.
    """

    # Use PyMuPDF to identify where on the page the table is.
    doc = fitz.Document(filename)
    page = doc.loadPage()

    # Find the title of the table section
    header = page.searchFor('This Bit Here')
    if header:
        header = header[0]
    else:
        return {}
    
    # Find the title of the section after the table
    footer = page.searchFor('And Another Bit Here')
    if footer:
        footer = footer[0]
    else:
        return {}

    # Find the page bounds    
    page_bounds = page.bound()

    # Calculate the area the table will be in from the titles and page bounds
    region = ",".join(str(x) for x in [ # co-ordinates from bottom left corner
        header[0], #left
        page_bounds[3] - header[3], #top
        page_bounds[2], # right
        page_bounds[3] - footer[1] # bottom
    ])

    doc.close()

    # Use camelot to read the table
    tables = camelot.read_pdf(filename, flavor='stream', table_areas=[region])
    if tables:
        table = tables[0].df
    
        # Use the first row as column names
        table.columns = table.iloc[0]
        table = table.iloc[1:]
        
        record = {
            'text': page.getText(),
            'table': table.to_dict(orient='row')
        }
    else:
        record = {}
    
    return record

