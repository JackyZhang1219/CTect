import json
import boto3
import base64
import datatier
import pymysql
from openai import OpenAI
import nltk
import textblob
nltk_data_path = '/tmp/nltk_data'
nltk.download('punkt', download_dir=nltk_data_path)  # WordNet lemmatizer
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)
nltk.download('punkt_tab', download_dir=nltk_data_path)
nltk.download('brown', download_dir=nltk_data_path)
nltk.download('wordnet', download_dir=nltk_data_path)
nltk.data.path.append(nltk_data_path)

db_config = {
    'user': 'admin',
    'password': 'pw',
    'host': 'dbendpoint',
    'database': 'pdfstore'
}



def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: get_summary**")

    print(event)

    # body = json.loads(event['body'])
    classname = event['classname']

    # print(body)

    dbConn = pymysql.connect(**db_config)
    dbCursor = dbConn.cursor()
    select_query = """
    SELECT * FROM jobs WHERE classname = %s
    """


    dbCursor.execute(select_query, (classname,))

    result = dbCursor.fetchone()

    print(result)
    text = result[3]

    analysis = textblob.TextBlob(text)
    polarity = analysis.sentiment.polarity


    #keyphrase extraction
    key_phrases = analysis.noun_phrases
    keyphrases = set()
    positive_words = [word for word in analysis.words if textblob.TextBlob(word).sentiment.polarity > 0]
    negative_words = [word for word in analysis.words if textblob.TextBlob(word).sentiment.polarity < 0]
    #map polarity from 1-10
    rating = 0 + ((polarity - (-1)) / (1 - (-1))) * (10 - 0)
    keyphrases.update(key_phrases)

    results = {
      "polarity": polarity,
      "rating": rating,
      "key_phrases": list(keyphrases),
      "positive_words": positive_words,
      "negative_words": negative_words
    }

    client = OpenAI(api_key = "sample_key")

    prompt = f"Here is the average rating for a course from 0-10 and some key words. Return a short general summary. Average: {results['rating']}, Key Words: {[word for word in results['key_phrases']]}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    return {
        'statusCode': 200,
        'body': json.dumps({
            'rating': results['rating'],
            'summary': json.dumps(response.choices[0].message.content)
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
