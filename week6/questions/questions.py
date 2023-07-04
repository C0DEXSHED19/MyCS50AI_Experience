import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file)) as f:
            s = f.read()
            data[file] = s       
    return data
    raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    res = []
    words = nltk.tokenize.word_tokenize(document.lower())
    for w in words:
        if w in nltk.corpus.stopwords.words('english'):
            continue
        else:
            for char in w:
                if char not in string.punctuation:
                    res.append(w)
                    
                
    return res
    
    
    raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    for doc in documents.keys():
        words = documents[doc]
        
        for word in words:
            if word not in idfs:
                counter = 0
                for d in documents.keys():
                    if word in documents[d]:
                        counter += 1
            idfs[word] = math.log(len(documents) / counter)
            
    return idfs
                
                        
        
    raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    for f in files:
        scores[f] = 0
    for word in query:
        for f in files:
            if word not in files[f]:
                continue
            else:
                counter = 0
                for w in files[f]:
                    if w == word:
                        counter += 1
                scores[f] += counter * idfs[word]
                
    sorting = sorted([fname for fname in files], key = lambda x : scores[x], reverse=True)
    return sorting[:n]
    raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    for sentence in sentences:
        scores[sentence] = {"idf" : 0,"query_w" : 0, "q_score" : 0}
        
    for sentence in sentences:
        subscores = scores[sentence]
        for word in query:
            if word in sentences[sentence]:
                subscores["idf"] += idfs[word]
                subscores["query_w"] += sentences[sentence].count(word)

        subscores['q_score'] = subscores['query_w'] / len(sentence.split())

    sorting = sorted([sentence for sentence in sentences], key = lambda x: (scores[x]["idf"], scores[x]["q_score"]), reverse=True)

    return sorting[:n]
    raise NotImplementedError


if __name__ == "__main__":
    main()
