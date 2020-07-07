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
    matches = re.split(r'(\n\n)(\d+\.\s)', input_text)[2:]
    result = ['']
    old_paragraph_number = 0
    for i in range(0, len(matches), 3):
        paragraph_number = int(matches[i].split('.')[0])
        if paragraph_number != old_paragraph_number + 1:
            error_message = 'ERROR Parsing Paragraph {0} detected {1}. '.format(
                old_paragraph_number + 1, paragraph_number)
            if paragraph_number >= old_paragraph_number:
                result.append(error_message)
                result.append(re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip()))
            else:
                result.append(error_message + ' ' + re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip()))
            if paragraph_number in range(old_paragraph_number, old_paragraph_number + 3):
                old_paragraph_number = paragraph_number
        else:
            result.append(re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip()))
            old_paragraph_number = paragraph_number
    return result[1:]


def get_sentences(input_text):
    sentences = re.sub(r'(\fC.*\d\n)', '', input_text)  # Remove Page Headers
    sentences = re.sub(r'(\n\d+ \n)', '', sentences)  # Remove Page Numbers
    sentences = re.sub(r'\n+[A-Z ]+\n+', '\n\n', sentences)  # Remove Section Titles
    sentences = re.sub(r'([IVXCMD]+\.[A-Za-z \.\'\’\n-]+)\n[\dA-Z]', '\n\n',
                       sentences)  # Remove Roman Numeral Section Titles
    sentences = re.sub(r'(\n{3,}|\n\n )', '', sentences)  # Apply Consistent Paragraph Spacing
    sentences = re.sub(r'  ', ' ', sentences)  # Apply Consistent Text Spacing
    sentences = re.sub(r'(\S)(\n\n)([A-Za-z])', r'\1 \3', sentences)  # Handle EOL without a space
    sentences = re.sub(r'(\n\) )(1\.\s)', r'\n\n\2', sentences, 1)  # Make first paragraph match others
    return build_paragraph('\n\n' + sentences) # \n\n to match test files with real datasets


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
