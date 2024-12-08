#
# Python program to run sentiment analysis on extracted text
#

import json
import boto3

def lambda_handler(event, context):
  try:
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-2')
    
    # Get text input from the event
    prompt = json.loads(event["body"])["prompt"]
    
    model_id = 'us.anthropic.claude-3-5-sonnet-20240620-v1:0'

    native_request = {
      "anthropic_version": "bedrock-2023-05-31",
      "max_tokens": 512,
      "temperature": 0.5,
      "messages": [
          {
              "role": "user",
              "content": [{"type": "text", "text": prompt}],
          }
      ],
    }
    
    # Invoke the Bedrock model
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(native_request)
    )
    
    # Parse the response
    result = json.loads(response['body'].read())

    response = result['content'][0]['text']
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps({'result': response})
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