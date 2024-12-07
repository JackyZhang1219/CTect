#
# Python program to allow user to upload pdf and parse pdf
#

import json
import boto3
# import os
import base64
import datatier
textract_client = boto3.client('textract')

rds_endpoint = 'pdfstore-database.c5ggmgyguhw5.us-east-2.rds.amazonaws.com'
rds_portnum = '3306'
rds_username = 'admin'
rds_pwd = 'pdfstoragedatabase'
rds_dbname = 'pdfstore'


def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: extract_text**")

    original_file_name = "FILL THIS WITH CODE TO GET THE FILENAME FROM USER INPUT"
    body = json.loads(event['body'])
    file_content = base64.b64decode(body['file'])

    response = textract_client.detect_document_text(
        Document={
            'Bytes': file_content
        }
    )

    extracted_text = ""
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            extracted_text += block['Text'] + '\n'
    
    print(extracted_text)

    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

    insert_query = """
    INSERT INTO jobs (status, originaldatafile, extractedtext)
    VALUES (%s, %s, %s)
    """


    values = ['completed', f"{original_file_name}", extracted_text]

    datatier.perform_action(dbConn, insert_query, values)

    print("data inserted into table")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'extracted_text': extracted_text
        })
    }
    
  except Exception as err:
    print("**ERROR**")
    print(str(err))

    #
    # done, return:
    #    
    return {
      'statusCode': 500,
      'body': json.dumps(str(err))
    }
