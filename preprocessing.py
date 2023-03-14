# data prepocessing 

"""
Import library 
"""
import csv
import email
import os
import re
from pathlib import Path

import pandas as pd

NON_STANDARD_TAGS = ['<blink', '<marquee', '<table']
HIDDEN_TAGS = ['style', 'font']
KEYWORDS = []
URL_PATTERN = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

"""To find the most popular word in email"""


def getKeywords():
    with open('keywords.txt') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            line = line.lower()
            KEYWORDS.append(line)


"""Fill the csv file """


def fillCsv(rawEmail):
    output = [0] * len(KEYWORDS)
    email_message = email.message_from_string(rawEmail)

    subject = email_message['Subject']

    totalKeywordsInSubject = 0

    for keyword in KEYWORDS:
        if subject and keyword in subject.lower():
            totalKeywordsInSubject += 1

    totalNonStandardTags = 0
    totalHiddenTags = 0
    totalLinks = 0
    totalKeywords = 0

    for part in email_message.walk():
        content_type = part.get_content_type()
        if content_type in ["text/plain"]:
            textBody = part.get_payload(decode=True)
            textBody = textBody.decode(errors='ignore')
            textBody = textBody.lower()

            # Remove unwanted characters, punctuations (commas) from the body of the email
            textBody = re.sub(r'[^\w\s\.\?!]', ' ', textBody)
            textBody = textBody.lower()
            textBody = re.sub(r',', '', textBody)
            textBody = textBody.strip()

            for index, keyword in enumerate(KEYWORDS):
                count = textBody.count(keyword)
                totalKeywords += count
                output[index] += count

        if content_type in ["text/html"]:
            body = part.get_payload(decode=True)
            body = body.decode(errors='ignore')
            body = body.lower()

            for tag in NON_STANDARD_TAGS:
                if tag in body:
                    totalNonStandardTags += 1

            for tag in HIDDEN_TAGS:
                pattern = re.compile(r'<' + tag + r'\b[^>]*>(.*?)</' + tag + r'>')
                totalHiddenTags += len(re.findall(pattern, body))

            totalLinks += len(re.findall(URL_PATTERN, body))
    output.append(totalKeywords)
    output.append(totalHiddenTags)
    output.append(totalLinks)
    output.append(totalKeywordsInSubject)
    output.append(totalKeywords)

    return output



""" do labeling and delete the empty value """


def spam_ham_data():
    df = pd.read_csv('dataset.csv')
    print(df.head())
    counts = df['classification'].value_counts()
    print("Number of ham messages:", counts[0])
    print("Number of spam messages:", counts[1])


def process_directory(folder):
    path = os.path.join('.', folder)
    csv_rows = []
    for filename in Path(path).rglob('*.txt'):
        with open(filename, encoding='UTF8', errors='ignore') as file:
            rawEmail = file.read()
            csv_row = fillCsv(rawEmail)
            classification = 0
            path = filename.__str__()
            if path.__contains__("Spam"):
                classification = 1
            csv_row.append(classification)
            csv_rows.append(csv_row)
    with open('dataset.csv', 'w', newline='', encoding='UTF8') as file:
        my_writer = csv.writer(file)
        header = KEYWORDS
        header.extend(['non_standard_html_tag_count', 'spam_keywords', 'total_links', 'total_keywords_in_subject',
                       'total_keywords_in_body', 'classification'])
        my_writer.writerow(header)
        my_writer.writerows(csv_rows)


def main():
    getKeywords()
    process_directory('data')
    spam_ham_data()


if __name__ == '__main__':
    main()
