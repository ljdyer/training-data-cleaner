import nltk
import re

# Japanese sentence splitter
sentence_splitter = nltk.RegexpTokenizer(u'[^！？。]*[！？。]')

raw_file_path = 'kirin_jp_wiki.txt'
sent_file_path = 'kirin_jp_wiki_sents.txt'

# ====================
def tokenize_sents(text: str) -> list:
    """Perform sentence tokenization on the given text and return a list of
    sentences."""
    sents = sentence_splitter.tokenize(text)
    return sents

with open(raw_file_path, encoding='utf8') as f:
    text = f.read()
text = re.sub(r'\[[^\]]*\]', '', text)
sents = [s.replace('\n', '') for s in tokenize_sents(text) if not s.isspace()]

with open(sent_file_path, 'w', encoding='utf8') as f:
    f.write('\n'.join(sents))