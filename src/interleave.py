import argparse
import sys
from csv import writer
import re
import textract
import itertools


def convert_pdf_to_txt(path):
    text = textract.process(path, method='pdfminer').decode()
    return text


def build_paragraphs(input_text):
    matches = re.split(r'(\n\n)(\d+\.\s)', input_text)[2:]
    result = ['']
    old_paragraph_number = 0
    for i in range(0, len(matches), 3):
        paragraph_number = int(matches[i].split('.')[0])
        if paragraph_number != old_paragraph_number + 1:
            result[-1] += re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip())
        else:
            result.append(re.sub(r'[\n\f]', '', ''.join(matches[i:i + 2]).strip()))
            old_paragraph_number = paragraph_number
    return result[1:]


def remove_headers(input_text):
    sentences = re.sub(r'(\fC.*\d\n)', '', input_text)  # Remove Page Headers
    sentences = re.sub(r'(\n\d+ \n)', '', sentences)  # Remove Page Numbers
    sentences = re.sub(r'\n+[A-Z ]+\n+', '\n\n', sentences)  # Remove Section Titles
    sentences = re.sub(r'([IVXCMD]+\.[A-Za-z .\'’\n-]+)\n(?!\dA-z)', ' \n\n',
                       sentences)  # Remove Roman Numeral Section Titles but don't conflict with next rule
    sentences = sentences.replace(chr(160), '\n')  # Remove nbsp Page Breaks
    return sentences


def prepare_body_text(input_text):
    sentences = re.sub(r'(\n{3,}|\n\n )', '\n\n', input_text)  # Apply Consistent Paragraph Spacing
    sentences = re.sub(r' {2}', ' ', sentences)  # Apply Consistent Text Spacing
    sentences = re.sub(r'(\S)(\n\n)([A-Za-z])', r'\1 \3', sentences)  # Handle EOL without a space
    sentences = re.sub(r'(\n\) )(1\.\s)', r'\n\n\2', sentences, 1)  # Make first paragraph match others
    return sentences


def remove_trailing_content(input_text):
    sentences = re.split(r'\n\nTable 1:', input_text)[0]  # Remove tables that follow document body
    sentences = re.split(r'\s/s/', sentences)[0]  # Remove EPA-style signature blocks
    sentences = re.split(r'Respectfully submitted,', sentences)[0]  # Remove EPA-style signature blocks
    return sentences


def sanitize_text(input_text):
    sentences = remove_headers(input_text)
    sentences = prepare_body_text(sentences)
    sentences = remove_trailing_content(sentences)
    return sentences


def zip_sentences(list1, list2):
    return list(itertools.zip_longest(list1, list2))


def create_csv(data, path, source_tuple):
    with open(path, 'w', newline='') as csvfile:
        writer(csvfile, delimiter=',').writerows([source_tuple])
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
        doc_1_dest = '../output/' + args.input[0].split('/')[-1].split('.')[0] + '.txt'
        doc_2_dest = '../output/' + args.input[1].split('/')[-1].split('.')[0] + '.txt'
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
        # \n\n to match test files with real datasets
        filtered_text = zip_sentences(build_paragraphs('\n\n' + sanitize_text(text_first_file)),
                                      build_paragraphs('\n\n' + sanitize_text(text_second_file)))
        print(create_csv(filtered_text, args.output[0], (args.input[0], args.input[1])))


if __name__ == '__main__':
    main(sys.argv[1:])
