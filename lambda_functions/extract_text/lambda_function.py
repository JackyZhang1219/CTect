#
# Python program to allow user to upload pdf and parse pdf
#

import json
import boto3
# import os
import base64

textract_client = boto3.client('textract')

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: extract_text**")

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
