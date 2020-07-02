import argparse
import sys

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from csv import writer
import re


# implementation from:
# https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def get_sentences(input_text):
    sentences = re.compile(r'(\d+\. (?:\n\n[^\d+\.]\S|\S| |\.)+)\n\n').findall(input_text)
    return [sentence.replace('\f', '').replace('\n\n', ' ').replace('  ', ' ') for sentence in sentences]


def zip_sentences(list1, list2):
    return list(zip(list1, list2))


def create_csv(data):
    with open('../output/Matched_Paragraphs.csv', 'w', newline='') as csvfile:
        writer(csvfile, delimiter=',').writerows([('Document1', 'Document2')])
        writer(csvfile, delimiter=',').writerows(data)
    return 'Files created.'


def main(argv):
    parser = argparse.ArgumentParser(description='Match numbered paragraphs from a PDF and store them in a CSV file.')
    parser.add_argument('input', metavar='I', type=str, nargs=2, help='two files to match and store')
    parser.add_argument('output', metavar='O', type=str, nargs=1, help='name of output file')
    args = parser.parse_args()

    print('\nColumn A source: ' + args.input[0] +
          '\nColumn B source: ' + args.input[1] +
          '\nOutput File: ' + args.output[0] + '\n')

    text_first_file = convert_pdf_to_txt(args.input[0])
    text_second_file = convert_pdf_to_txt(args.input[1])

    filtered_text = zip_sentences(get_sentences(text_first_file), get_sentences(text_second_file))
    print(create_csv(filtered_text))

if __name__ == '__main__':
    main(sys.argv[1:])
