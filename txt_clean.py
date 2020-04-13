import os
import re
DESCRIPTION_WORDS = ['the ', 'The ', " are ", ' with ', ' as ', ' is ', ' because ', ' of ', ' to ']
LOWER = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'}
UPPER = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}
def load_filenames():
    """
    load xml files in xml directory
    """
    os.chdir('raw_txt')
    files = os.listdir()
    filenames= [filename for filename in files if filename[-4:]=='.txt']
    os.chdir('..')
    # return filenames
    return filenames
def confirm_directory():
    """
    asserts we are in the parent directory of the xml and txt files
    """
    assert('raw_txt' in os.listdir() and 'txt' in os.listdir())
def isalphanum(char):
    return char.isalpha() or char.isdigit()
def ends_with_punctuation(each):
    if len(each)==0:
        return False
    elif each[-1] in ".?!":
        return True
    else:
        return False
def count_alphanum(txt):
    result = 0
    for char in txt:
        if isalphanum(char):
            result+=1
    return result
def fix_cutwords(sentence):
    """
    fixes sentence with a minus cutoff. Later possibly
    """
    if "-" in sentence:
        minus_index = sentence.find("-")
        if minus_index == len(sentence)-1:
            return sentence
        i = minus_index + 1
        while sentence[i] == " ":
            i+=1
        if sentence[i] in LOWER:
            print(sentence)
            print(sentence[:minus_index] + sentence[i:])
            return sentence[:minus_index] + fix_cutwords(sentence[i:])
    return sentence

def clean_text(keep):
    cleaned = []
    for string in keep:
        sentence = re.sub("ﬁ\s*", "fi", string)
        # if "-" in sentence:
        #     sentence = fix_cutwords(sentence)
        cleaned.append(sentence)
    return cleaned
def fix_broken_lines(keep):
    """
    removes line breaks in the middle of paragraphs. Input list of paragraphs that may
    have bad line breaks
    """
    fix = []
    previous_strings = ""
    for each in keep:
        string = each.strip()
        lowercase = string[0]==string[0].lower()
        punctuated = ends_with_punctuation(string)
        if punctuated:
            if lowercase:
                fix.append(previous_strings + string)
                previous_strings = ""
            else:
                if len(previous_strings):
                    fix.append(previous_strings.strip())
                    previous_strings = ""
                fix.append(string)
        else:
            if lowercase:
                previous_strings += string+" "
            else:
                if len(previous_strings):
                    fix.append(previous_strings.strip())
                previous_strings = string + " "

    if len(previous_strings):
        fix.append(previous_strings)
    return fix

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
        os.chdir('raw_txt')
        data = self.parse_txt(txt_filename)
        assert(len(data))
        os.chdir('../txt')
        self.export_txt(txt_filename, data)
        os.chdir('..')
        confirm_directory()

    def parse_txt(self, filename):
        assert(filename in os.listdir())
        assert(filename[-3:]=='txt')
        data = None
        with open(filename, 'r') as fp:
            data = fp.read()
        return data

    def export_txt(self, filename, data):
        assert(filename[-3:]=='txt')
        text = self.format_text(filename, data)
        with open(filename, "w") as output:
            output.write(text)
    def format_text(self, filename, data):
        data_split1 = data.splitlines()
        data_split = [each for each in data_split1 if count_alphanum(each) > 0]
        rgx_1 = "[\.,?:]"
        keep = []
        for each in data_split:
            matches = re.findall(rgx_1, each)
            # print(matches)
            punctuation = len(matches) >= 1
            if "■" == each[0] and filename=="Anatomy_Gray.txt":
                keep.append(each[2:])
            elif filename == "Biochemistry_Lippincott.txt" and each.find("Figure ")==0:
                pass
            elif punctuation or self.description_word(each):
                keep.append(each)
            else:
                pass
        keep = fix_broken_lines(keep)
        keep = clean_text(keep)
        text = '\n\n'.join(keep)
        return text #re.fin("\n+","\n", text)
    def description_word(self, sentence):
        for each in DESCRIPTION_WORDS:
            if each in sentence:
                return True
        return False
if __name__ == "__main__":
    processor = ProcessTXT()
    processor.convert_txts()
