import spacy

# load model once
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text):
    doc = nlp(text)

    tokens = []

    for token in doc:
        if token.is_stop:
            continue
        if token.is_punct:
            continue
        if token.is_space:
            continue

        tokens.append(token.lemma_.lower())

    return " ".join(tokens)