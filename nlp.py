import spacy

nlp = spacy.load('en_core_web_sm')

def token_allowed(token):
	if (not token or not token.string.strip() or token.is_stop or token.is_punct):
		return False
	return True

def preprocess(token):
	return token.lemma_.strip().lower()

if __name__ == "__main__":
	msg = ('Hey, can I get a small tree with lots of fruit and few leaves. '
		   'It should start pink and end blue, and have blue fruits and its leaves have to be green.')

	test = ('I want a small tree with blue fruits.')

	msg_doc = nlp(msg)
	test_doc = nlp(test)

	processed_test_doc = [token for token in test_doc if token_allowed(token)]
	for chunk in msg_doc.noun_chunks:
		print(chunk)

