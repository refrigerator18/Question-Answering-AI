import nltk
import sys
import math
import os
from collections import Counter
import operator

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
    corpus = {}
    for text_file in os.listdir(directory):
        path = os.path.join(directory, text_file)
        with open(path) as text:
            corpus[text_file] = text.read()
    return corpus
 

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = {word for word in nltk.corpus.stopwords.words("english")}

    pre = nltk.word_tokenize(document)
    processed = []
    for word in pre:
        if word.isalpha() and word.lower() not in stopwords:
            processed.append(word.lower())
    return processed



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # def check_documents(value):
    #     occured = 0
    #     for key in documents.keys():
    #         for word in documents[key]:
    #             if value == word:
    #                 occured += 1
    #                 break
    #     return occured

    idf_values = {}
    total_docs = len(documents.keys())
    for key in documents.keys():
        for value in documents[key]:
            occured = sum(value in documents[filename] for filename in documents)
            idf_values[value] = math.log((total_docs / occured))

    return idf_values



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    counter = Counter()
    for file_key in files.keys():
        total = 0
        for word in query:
            tf = 0
            for word2 in files[file_key]:
                if word == word2:
                    tf += 1
            tf_idf = tf * idfs[word]
            total += tf_idf
        counter[file_key] = total


    top_files = [a for a, _ in counter.most_common(n)]
    return top_files




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    counter = Counter()
    for sentence in sentences.keys():
        used_words = set()
        for word in sentences[sentence]:
            if word in query and word not in used_words:
                counter[sentence] += idfs[word]
                used_words.add(word)
    top_sentences = [[a, b] for a, b in counter.most_common()]

    for pair in top_sentences:
        sentence = pair[0]
        density = 0
        for word in sentences[sentence]:

            if word in query:
 
                density += 1
        density = density / len(sentences[sentence])
        pair.append(density)

    top_sentences = sorted(top_sentences, key = operator.itemgetter(1, 2))
    top_sentences.reverse()
    result = [pair[0] for pair in top_sentences]

    
    return result[:n]








if __name__ == "__main__":
    main()
