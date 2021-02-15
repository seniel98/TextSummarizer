#Importing the Library
import PyPDF2
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

# #Open File in read binary mode
# pdf_file=open("basak.pdf","rb")
 
# # pass the file object to PdfFileReader
# reader=PyPDF2.PdfFileReader(pdf_file)

# pdfData = ""
# i = 0
# # page = reader.getPage(i)
# # pdfData = pdfData + page.extractText()
# while i<reader.numPages:
#     # getPage will accept index
#     page = reader.getPage(i)
#     #extractText will return the text
#     pdfData = pdfData + page.extractText()
#     i = i+1

txt_file = open("pdf2.txt","r")

# Getting data
doc = txt_file.read()

nlp = spacy.load('en_core_web_sm')

docx = nlp(doc)

extra_words = list(STOP_WORDS)+list(punctuation)+['\n']

# Creating Vocabulary with spaCy
all_words=[word.text for word in docx]

word_freq={}

for w in all_words:
    w1 = w.lower()
    if w1 not in extra_words and w1.isalpha():
        if w1 in word_freq.keys():
              word_freq[w1]+= 1
        else:
              word_freq[w1] = 1

# Assigning a Title – Headline Generation
val=sorted(word_freq.values())
max_freq=val[-3:]
print("Topic of document given :-")
for word,freq in word_freq.items():
    if freq in max_freq:
        print(word ,end=" ")
    else:
        continue

# Term Frequency – Inverse Document Frequency (TFIDF)
# Used to represent how important a given word is to a document on a complete collection relatively.

for word in word_freq.keys():
    word_freq[word] = (word_freq[word]/max_freq[-1])

# Sentence Strength

sent_strength={}
for sent in docx.sents:
    for word in sent :
        if word.text.lower() in word_freq.keys():
            if sent in sent_strength.keys():
                sent_strength[sent]+=word_freq[word.text.lower()]
            else:
                sent_strength[sent]=word_freq[word.text.lower()]
        else: 
            continue

# Getting Important Sentences

top_sentences=(sorted(sent_strength.values())[::-1])
top30percent_sentence=int(0.3*len(top_sentences))
top_sent=top_sentences[:top30percent_sentence]

# Creating the Final Summary
summary=[]
for sent,strength in sent_strength.items():
    if strength in top_sent:
        summary.append(sent)
    else:
        continue

print("")

summary_file = open("summary.txt","a")
for i in summary:
    print(i,end="",file=summary_file)

summary_file.close()
print("")