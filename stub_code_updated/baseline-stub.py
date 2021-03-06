#!/usr/bin/env python
'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import sys, nltk, operator, re

# Read the file from disk
def read_file(filename):
    fh = open(filename, 'r')
    text = fh.read()
    fh.close()
    
    return text

# The standard NLTK pipeline for POS tagging a document
def get_sentences(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    
    return sentences	

def get_bow(tagged_tokens, stopwords):
    return set([t[0].lower() for t in tagged_tokens if t[0].lower() not in stopwords])
	
def find_phrase(tagged_tokens, qbow):
    for i in range(len(tagged_tokens) - 1, 0, -1):
        word = (tagged_tokens[i])[0]
        if word in qbow:
            return tagged_tokens[i+1:]
	
# qtokens: is a list of pos tagged question tokens with SW removed
# sentences: is a list of pos tagged story sentences
# stopwords is a set of stopwords
def baseline(qbow, sentences, stopwords):
    # Collect all the candidate answers
    answers = []
    for sent in sentences:
        # A list of all the word tokens in the sentence
        sbow = get_bow(sent, stopwords)
        
        # Count the # of overlapping words between the Q and the A
        # & is the set intersection operator
        overlap = len(qbow & sbow)
        
        answers.append((overlap, sent))
        
    # Sort the results by the first element of the tuple (i.e., the count)
    # Sort answers from smallest to largest by default, so reverse it
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)

    # Return the best answer
    best_answer = (answers[0])[1]    
    return best_answer
	
#def get_question(question):
#    #quest = re.compile('Question: "(.*)"')
#    #test = quest.findall(quest)
#    test = re.search(r'Question: "(.*)"', question)
#    print(test)
#    return ""#str(test.group(1))
	
def process_questions(text, question_text, stopwords):
    text_list = question_text.splitlines()
    id_list = [] #three separate lists, but they'll be added to in order so indexing will be the same
    question_list = []
    type_list = []
    for line in text_list:
        current_id_re = re.search(r'QuestionID: (.*)', line)#lots of short searches, don't really need regex but lol
        current_question_re = re.search(r'Question: (.*)', line)
        current_type_re = re.search(r'Type: (.*)', line)
        if current_id_re is not None:
            id_list.append(current_id_re.group(1))
        elif current_question_re is not None:
            current_question = current_question_re.group(1)
            question_list.append(current_question)
        elif current_type_re is not None:
            if "Sch" in line: #try to use sch if can
                type_list.append("Sch")
            else:
                type_list.append("Story")
    
    for i in range(len(id_list)):
        #print(id_list[i] + question_list[i] + type_list[i])
        #the below things are used on a question sentence itself
        qbow = get_bow(get_sentences(question_list[i])[0], stopwords)
        sentences = get_sentences(text)
        answer = baseline(qbow, sentences, stopwords)
        answer_sentence = ""
        for word in answer:
            answer_sentence = answer_sentence + word[0] + " "
        print("Question ID: " + id_list[i] + "\nAnswer: " + answer_sentence + "\n")
        
if __name__ == '__main__':
    text_file = "fables-01.sch"
    question_file = "fables-01.questions"
	
    stopwords = set(nltk.corpus.stopwords.words("english"))
    text = read_file(text_file)
    question_text = read_file(question_file)
    #question = "Where was the crow sitting?"
	
    answer = process_questions(text, question_text, stopwords)
    #qbow = get_bow(get_sentences(question)[0], stopwords)
    #sentences = get_sentences(text)
	
    #answer = baseline(qbow, sentences, stopwords)
	
    #print(" ".join(t[0] for t in answer))
