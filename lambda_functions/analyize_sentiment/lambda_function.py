#
# Python program to run sentiment analysis on extracted text
#

import json
import boto3

def lambda_handler(event, context):
  try:
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-2')
    
    # Get text input from the event
    input_text = event["text"]
    
    # Define custom prompt
    custom_prompt = f"""
    Provide a 50 word summary for the following text, answering whether the class is worth taking:
    "{input_text}"
    """
    
    model_id = 'amazon.titan-text-lite-v1'
    
    # Invoke the Bedrock model
    response = bedrock_client.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=json.dumps({"input": custom_prompt})
    )
    
    # Parse the response
    result = json.loads(response['body'].read())
    
    # Return the result
    return {
        'statusCode': 200,
        'body': json.dumps({'result': result})
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
