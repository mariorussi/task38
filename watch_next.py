import spacy
import string

nlp = spacy.load("en_core_web_md")
stop_words = nlp.Defaults.stop_words

def preprocess(text):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.text.lower() not in stop_words and not token.is_punct:
            tokens.append(token.lemma_.lower())
    return " ".join(tokens)

def get_similar_movie(description):
    with open("movies.txt", "r") as file:
        movies = file.readlines()

    max_similarity = -1
    most_similar_movie = ""
    similarities = []

    description = preprocess(description)

    for movie in movies:
        title, desc = movie.strip().split(":")
        desc = preprocess(desc)
        similarity = nlp(desc).similarity(nlp(description))
        similarities.append(similarity)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_movie = title

    return most_similar_movie, similarities

hulk_desc = "Will he save their world or destroy it? When the Hulk becomes too dangerous for the Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery and trained as a gladiator."
most_similar, similarities = get_similar_movie(hulk_desc)

print(f"Most similar movie: {most_similar}")
print(f"Cosine similarities for all movies: {similarities}")
