# data prepocessing 

"""
Import library 
"""
import email
from email import message_from_string
import os
import csv
import re
from collections import Counter
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pandas as pd

import nltk

nltk.download('stopwords')

NON_STANDARD_TAGS = ['<blink', '<marquee', '<table']
HIDDEN_TAGS = ['style', 'font']
KEYWORDS = []

"""To find the most popular word in email"""


def getKeywords():
    with open('keywords.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            line = line.lower()
            KEYWORDS.append(line)


"""
Method creates the CSV file to write results to.
"""


def createResultsCSV():
    header = ['from', 'to', 'subject', 'textBody', 'non_standard_html_tag_count', 'spam_ham_keywords',
              'total_links', 'total_keywords_in_subject', 'total_keywords_in_body', 'frequency', 'classification']
    if not os.path.isfile('ham.csv'):
        with open('ham.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)


"""
Method to check the content is directory or string 
"""


def extract_info(directory_or_string):
    try:
        if os.path.isdir(directory_or_string):
            # Input is a directory
            for filename in os.listdir(directory_or_string):
                with open(os.path.join(directory_or_string, filename), encoding='UTF8', errors='ignore') as file:
                    rawEmail = file.read()
                    # email_message = email.message_from_string(rawEmail)
                    fillCsv(rawEmail)
        else:
            # Input is a string
            if isinstance(directory_or_string, str):
                # email_message = email.message_from_string(directory_or_string)
                fillCsv(directory_or_string)
    except():
        pass


"""Fill the csv file """


def fillCsv(rawEmail):
    email_message = email.message_from_string(rawEmail)

    fromWho = email_message['From']
    to = email_message['To']
    match = re.search(r"<(.*?)>", fromWho)
    if match:
        fromWho = match.group(0)
    else:
        fromWho = ''

    subject = email_message['Subject']

    totalKeywordsInSubject = 0
    textBody = None
    # jibberishSubject = False

    for keyword in KEYWORDS:
        if subject and keyword in subject.lower():
            totalKeywordsInSubject += 1

    totalNonStandardTags = 0
    totalHiddenTags = 0
    totalLinks = 0
    totalKeywords = 0

    try:
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type in ["text/plain"]:
                textBody = part.get_payload(decode=True)
                textBody = textBody.decode()
                textBody = textBody.lower()

                word_freq = Counter(textBody)
                # word_fq = {word: word_freq for word, word_freq in textBody}

                word_fq = word_freq.most_common(1)
                frequency = word_fq[0][1]

                for keyword in KEYWORDS:
                    if keyword in textBody:
                        totalKeywords += 1

                # Remove unwanted characters, punctuations (commas) from the body of the email
                textBody = re.sub(r'[^\w\s\.\?!]', ' ', textBody)
                textBody = textBody.lower()
                textBody = re.sub(r',', '', textBody)
                textBody = textBody.strip()
                # textBody = word_tokenize(textBody) # only
                # textBody = [word for word in textBody if word not in stopwords.words("english")]

            if content_type in ["text/html"]:
                body = part.get_payload(decode=True)
                body = body.decode()
                body = body.lower()

                for tag in NON_STANDARD_TAGS:
                    if tag in body:
                        totalNonStandardTags += 1

                for tag in HIDDEN_TAGS:
                    pattern = re.compile(r'<' + tag + r'\b[^>]*>(.*?)</' + tag + r'>')
                    totalHiddenTags += len(re.findall(pattern, body))

                urlPattern = re.compile(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                totalLinks += len(re.findall(urlPattern, body))
        encoder = LabelEncoder()
        from_enc = encoder.fit_transform(fromWho)
        if textBody:
            result = [fromWho, to, subject, textBody, totalNonStandardTags, totalHiddenTags, totalLinks,
                      totalKeywordsInSubject, totalKeywords, frequency, "Ham"]
            textBody = None
        else:
            result = [fromWho, to, subject, '', totalNonStandardTags, totalHiddenTags, totalLinks,
                      totalKeywordsInSubject, totalKeywords, frequency, "Ham"]

        with open('ham.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(result)
    except Exception as e:
        print("Error")
        print(e)


def combin_Spam_ham(Spam, ham):
    ham_df = pd.read_csv(ham)
    spam_df = pd.read_csv(Spam)

    combined_df = pd.concat([ham_df, spam_df])
    # combined_df.dropna(inplace=True)
    contains_spam = combined_df['classification'].str.contains('spam', case=False)
    contains_ham = combined_df['classification'].str.contains('ham', case=False)

    # drop rows that do not contain either "spam" or "ham"
    combined_df = combined_df[contains_spam | contains_ham]

    with open('combine_data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(combined_df.columns.tolist())
        writer.writerows(combined_df.values.tolist())

    # combined_df.dropna(inplace=True)
    # combined_df.to_csv('Final_data.csv', index=False, encoding='utf-8-sig')
    # writer.writerows(combined_df.values.tolist())


""" do labeling and delete the empty value """


def spam_ham_data():
    df = pd.read_csv('dataset_spam_ham.csv')
    df = df.drop_duplicates(keep='first')
    encoder = LabelEncoder()
    df['classification'] = encoder.fit_transform(df['classification'])
    df.to_csv('dataset_spam_ham.csv', index=False)
    # print(df.head())
    df.to_csv('dataset_spam_ham_processed.csv', index=False)
    df = df.dropna()
    print(df.head())
    counts = df['classification'].value_counts()
    print("Number of ham messages:", counts[0])
    print("Number of spam messages:", counts[1])
    print(df.duplicated().sum())


def main():
    spam_ham_data()

    # To read raw data
    directory_spam = 'cleanedSpam'
    directory_ham = 'cleanedHam'

    # combine the file of ham and file of Spam
    ham = 'ham.csv'
    Spam = 'spam.csv'
    combin_Spam_ham(ham, Spam)
    getKeywords()
    createResultsCSV()
    # send the data to the method to fill the csv file
    extract_info(directory_ham)


#   fillCsv()


if __name__ == '__main__':
    main()

"""
from
to
subject
body
html tags in subject
links in body
keywords like 'free', 'congrats'
use of non standard html

"""




