import os
import re
def load_filenames():
    """
    load xml files in xml directory
    """
    os.chdir('txt')
    files = os.listdir()
    filenames= [filename for filename in files if filename[-4:]=='.txt']
    os.chdir('..')
    # return filenames
    return filenames
def confirm_directory():
    """
    asserts we are in the parent directory of the xml and txt files
    """
    assert('txt' in os.listdir() and 'sentence' in os.listdir())

def txt_to_sentences(data):
    text = data.split("\n")
    for paragraph in text:
        for line in paragraph.split('.'):
            line_cleaned = re.sub(r'([^a-zA-Z0-9\.])', " ", line).strip()
            line_cleaned = re.sub(' +', ' ', line_cleaned)
            for sentence in line_cleaned.split("."):
                if len(sentence) < 5:
                    continue
                yield sentence

def group(filename):
    sentences = None
    with open(filename, 'r') as fp:
        sentences = txt_to_sentences(fp.read())
    return sentences

class ProcessTXT:
    def __init__(self):
        confirm_directory()
        self.filenames = load_filenames()
        confirm_directory()
    def convert_txts(self):
        for filename in self.filenames:
            self.convert_txt(filename)
            confirm_directory()
    def convert_txt(self, txt_filename):
        #parse xml
        confirm_directory()
        os.chdir('txt')
        data = self.parse_txt(txt_filename)
        os.chdir('../sentence')
        self.export_txt(txt_filename, data)
        os.chdir('..')
        confirm_directory()

    def parse_txt(self, filename):
        assert(filename in os.listdir())
        assert(filename[-3:]=='txt')
        data = None
        with open(filename, 'r') as fp:
            data = fp.read()
        return txt_to_sentences(data)

    def export_txt(self, filename, data):
        assert(filename[-3:]=='txt')
        data = [each for each in data]
        with open(filename, "w") as output:
            for sentence in data:
                output.write(sentence+"\n")
if __name__ == "__main__":
    processor = ProcessTXT()
    processor.convert_txts()
