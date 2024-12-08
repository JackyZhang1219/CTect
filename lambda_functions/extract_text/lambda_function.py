import json
import boto3
import base64
import pymysql

textract_client = boto3.client('textract')

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: extract_text**")
    body = json.loads(event['body'])
    original_file_name = body["filename"]
    classname = body['classname']
    file_content = base64.b64decode(body['data'])

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
        'password': 'pdfstoragedatabase',
        'host': 'pdfstore-database.c5ggmgyguhw5.us-east-2.rds.amazonaws.com',
        'database': 'pdfstore'
    }

    dbConn = pymysql.connect(**db_config)
    dbCursor = dbConn.cursor()

    insert_query = """
    INSERT INTO jobs (status, classname, extractedtext)
    VALUES (%s, %s, %s)
    """

    values = ('completed', f"{classname}", extracted_text)

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
