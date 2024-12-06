from openai import OpenAI
import textblob
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
import numpy as np


keyphrases = set()


def sentiment_analysis_with_keywords(reviews):
    results = []
    for review in reviews:
        analysis = textblob.TextBlob(review)
        polarity = analysis.sentiment.polarity


        #keyphrase extraction
        key_phrases = analysis.noun_phrases

        positive_words = [word for word in analysis.words if textblob.TextBlob(word).sentiment.polarity > 0]
        negative_words = [word for word in analysis.words if textblob.TextBlob(word).sentiment.polarity < 0]
        #map polarity from 1-10
        rating = 0 + ((polarity - (-1)) / (1 - (-1))) * (10 - 0)
        keyphrases.update(key_phrases)
        # Append the result
        results.append({
            "review": review,
            "polarity": polarity,
            "rating": rating,
            "key_phrases": key_phrases,
            "positive_words": positive_words,
            "negative_words": negative_words
        })
    return results

reviews = [
    "The course provided me with a more concrete understanding of the underlying algorithms of a technology that I already had a strong interest in. As such, I feel much more confident and more likely to use this technology in my own future research.",
    "There's not a ton of context for assignments but the content is interesting. Get ready to ask a lot of questions! Lectures can get deep and you won't understand a lot of it because there's also little context there.",
    "Hardest class at Northwestern hands down, in all 30 classes I've taken as almost a rising senior now it's actually insane how big the jump was. DO NOT TAKE IT WITH PROF CROTTY",
    "I liked this class. That said, I hoped I would develop more hard skills on platforms like Tableau and ArcGIS and I did not develop those as much as I'd hoped. Smilowitz is really great though and the projects are really interesting.",
    "Great course super interesting case studies, learned more and feel more comfortable with data analytics, given the space to learn but ask questions when needed.",
    "Being part of a great team made my experience in this class awesome and worthwhile. This class is all about teamwork"
]

results = sentiment_analysis_with_keywords(reviews)

# Display results
for result in results:
    print(f"Review: {result['review']}")
    print(f"Polarity: {result['polarity']:.2f}")
    print(f"Assigned Rating: {result['rating']}")
    print(f"Key Phrases: {', '.join(result['key_phrases'])}")
    print(f"Positive Words: {', '.join(result['positive_words'])}")
    print(f"Negative Words: {', '.join(result['negative_words'])}")
    print("-" * 50)


rating = np.mean([result['rating'] for result in results])

# print(f"Here is the average rating for a course from 0-10 and some key words. Return a short general summary. Average: {rating}, Key Words: {[word for word in keyphrases]}")

client = OpenAI(api_key = "api_key")

def get_summary():
    prompt = f"Here is the average rating for a course from 0-10 and some key words. Return a short general summary. Average: {rating}, Key Words: {[word for word in keyphrases]}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ]
    )

    return response

print(get_summary())