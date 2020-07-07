import argparse
import sys

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from csv import writer
import re
import textract


def convert_pdf_to_txt(path):
    text = textract.process(path, method='pdfminer').decode()
    return text


def build_paragraph(input_text):
    sentences = input_text.split('\n\n')[:-1]  # Remove final page feed
    final_paragraphs = list()
    paragraph = ''
    for sentence in sentences:
        if sentence.split('.')[0].isnumeric():
            if paragraph != '' or \
                    paragraph[:-1] == '.' or \
                    paragraph[:-1] == '!' or \
                    paragraph[:-1] == '?':
                final_paragraphs.append(paragraph)
            paragraph = sentence.strip('\f')
        else:
            paragraph += sentence.strip('\f')
    final_paragraphs.append(paragraph)

    return final_paragraphs


def get_sentences(input_text):
    sentences = re.sub(r'(\fC.*\d\n)', '', input_text)  # Remove Page Headers
    sentences = re.sub(r'(\n\d+ \n)', '', sentences)  # Remove Page Numbers
    sentences = re.sub(r'\n+[A-Z| ]+\n+', '\n\n', sentences)  # Remove Section Titles
    sentences = re.sub(r'([I|V|X|C|M|D]+\.[A-Z|a-z| |\.|\'|\’|-|-|\n]+)\n[\d|A-Z]', '\n\n',
                       sentences)  # Remove Roman Numeral Section Titles
    sentences = re.sub(r'(\n{3,}|\n\n )', '', sentences)  # Apply Consistent Paragraph Spacing
    sentences = re.sub(r'  ', ' ', sentences)  # Apply Consistent Text Spacing
    sentences = re.sub(r'(\S)(\n\n)([A-z|a-z])', r'\1 \3', sentences)
    return build_paragraph(sentences)


def zip_sentences(list1, list2):
    return list(zip(list1, list2))


def create_csv(data):
    with open('output/Matched_Paragraphs.csv', 'w', newline='') as csvfile:
        writer(csvfile, delimiter=',').writerows([('Document1', 'Document2')])
        writer(csvfile, delimiter=',').writerows(data)
    return 'Files created.'


def main(argv):
    parser = argparse.ArgumentParser(description='Match numbered paragraphs from a PDF and store them in a CSV file.')
    parser.add_argument('input', metavar='I', type=str, nargs=2, help='two files to match and store')
    parser.add_argument('output', metavar='O', type=str, nargs=1, help='name of output file')
    parser.add_argument('-r', '--raw', default=False, action='store_true', help='convert PDFs to raw text')

    args = parser.parse_args()

    print('\nColumn A source: ' + args.input[0] +
          '\nColumn B source: ' + args.input[1])

    if args.raw:
        doc_1_dest = '../output/document1.txt'
        doc_2_dest = '../output/document2.txt'
        print('\nStoring inputs as raw text.' +
              '\nDocument 1 destination: ' + doc_1_dest +
              '\nDocument 2 destination: ' + doc_2_dest)
        with open(doc_1_dest, 'w') as file:
            file.write(convert_pdf_to_txt(args.input[0]))
        with open(doc_2_dest, 'w') as file:
            file.write(convert_pdf_to_txt(args.input[1]))
    else:
        print('\nOutput File: ' + args.output[0] + '\n')

        text_first_file = convert_pdf_to_txt(args.input[0])
        text_second_file = convert_pdf_to_txt(args.input[1])

        filtered_text = zip_sentences(get_sentences(text_first_file), get_sentences(text_second_file))
        print(create_csv(filtered_text))


if __name__ == '__main__':
    main(sys.argv[1:])
