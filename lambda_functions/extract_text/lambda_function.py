#
# Python program to allow user to upload pdf and parse pdf
#

import json
import boto3
# import os
import base64
import mysql.connector

textract_client = boto3.client('textract')

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

    db_config = {
          'user': 'admin',
          'password': 'your_database_password',
          'host': 'your_rds_endpoint',
          'database': 'your_database_name'
    }

    dbConn = mysql.connector.connect(**db_config)
    dbCursor = dbConn.cursor()

    insert_query = """
    INSERT INTO jobs (status, originaldatafile, extractedtext)
    VALUES (%s, %s, %s)
    """


    values = ('completed', f"{original_file_name}", extracted_text)

    dbCursor.execute(insert_query, values)
    dbConn.commit()

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
