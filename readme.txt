Readme:

To set up the server, a layer is first required to be able to run the sentiment analysis models, SQL queries, as well as LLM calls. This layer includes the following key packages:
NLTK, the key NLP library
TextBlob, a Sentiment Analysis model built on NLTK’s corporas
openai
pymysql
regex

For NLTK and TextBlob to function properly without raising a regex issue, the Python Runtime specified in layer creation MUST match the python version in CloudShell, which at the time of writing is 3.9.x. 

Lambda functions must be created for each of the upload, chat, and summary calls; details are as follows:
Upload: after pasting source code, attach a policy allowing the lambda function to interact with AWS Textract for key PDF extraction functionality
Chat: attach a policy for Bedrock Invoke Model.
Summary: Adjust memory to 512mb as 128 is insufficient to run the Sentiment Analysis models provided by TextBlob. No policies are required.

API Gateway can then be set up with the following pathways and URLs: 
Upload: POST endpoint /upload
Chat: POST endpoint /chat
Summary: POST endpoint /summary

No authorization or request validators are required. 

Client python script will run by default; endpoint variable “baseurl” must be changed for proper functionality. 
