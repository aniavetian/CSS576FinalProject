"""
Ani Avetian
Christian Bergh
Saja Faham Alsulami
CSS 576 Final Project - email processing

File contains the code to build the backup email processing
"""
import email
import os
from pathlib import Path
import numpy as np
import csv


class Processor:
    def __init__(self):
        self.search_dictionary = ['make',
                                  "address",
                                  "all",
                                  "3d",
                                  "our",
                                  "over",
                                  "remove",
                                  "internet",
                                  "order",
                                  "mail",
                                  "receive",
                                  "will",
                                  "people",
                                  'report',
                                  'addresses',
                                  'free',
                                  'business',
                                  'email',
                                  'you',
                                  'credit',
                                  'your',
                                  'font',
                                  '000',
                                  'money',
                                  'hp',
                                  'hpl',
                                  'george',
                                  '650',
                                  'lab',
                                  'labs',
                                  'telnet',
                                  '857',
                                  'data',
                                  '415',
                                  '85',
                                  'technology',
                                  '1999',
                                  'parts',
                                  'pm',
                                  'direct',
                                  'cs',
                                  'meeting',
                                  'original',
                                  'project',
                                  're',
                                  'edu',
                                  'table',
                                  'conference',
                                  ';',
                                  '(',
                                  '[',
                                  '!',
                                  '$',
                                  '#',
                                  ]
        self.processed_output = []

    def process_text(self, text):
        """
        process the text for keywords to search
        :param text:
        :return: csv
        """
        word_count = max(1, len(text.split()))
        output = []
        for word in self.search_dictionary:
            count = text.count(word)
            percent = count / word_count
            output.append(percent)
        return output

    def process_file(self, file):
        """
        process a file for csv
        :param file:
        """
        with open(os.path.join(os.getcwd(), file), 'r', encoding='utf8', errors='ignore') as f:
            email_string = f.read()
        e_mail = email.message_from_string(email_string)
        text = ""
        if e_mail.is_multipart():
            for part in e_mail.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    payload = part.get_payload(decode=True)
                    text = payload.decode(errors='ignore')
        else:
            payload = e_mail.get_payload(decode=True)
            text = payload.decode(errors='ignore')
        output = self.process_text(text)
        folder = os.path.dirname(file)
        label = 0
        if folder.__contains__("Spam"):
            label = 1
        output.append(label)
        self.processed_output.append(output)

    def process_directory(self, folder):
        """
        process a folder to a csv output
        :param folder:
        """
        path = os.path.join('.', folder)
        for file in Path(path).rglob('*.txt'):
            self.process_file(file)
        a = np.array(self.processed_output)
        with open('processed_output.csv', 'w', newline='') as file:
            my_writer = csv.writer(file)
            header = self.search_dictionary
            header.append('label')
            my_writer.writerow(header)
            my_writer.writerows(a)

def main():
    p = Processor()
    p.process_directory("data")