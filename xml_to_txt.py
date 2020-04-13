import os
from bs4 import BeautifulSoup
REPLACEMENTS = {"- " : "", "&lt;" : "<", "&gt;" : ">", "&amp;" : "&"}
# keep_test = "\n\nFigure 24–39 The processing of an extracellular protein antigen for presentation to a helper T cell. This simplified depiction shows how peptide–class-II-Mhc complexes are formed in endosomes and delivered via vesicles to the cell surface. Viral envelope glycoproteins can also be processed by this pathway for presentation to helper T cells (not shown): these glycoproteins are normally made in the er and transported via the Golgi for insertion into the plasma membrane; although most of these glycoproteins will be incorporated into the envelope of budding viral particles, some will be endocytosed and enter endosomes, from where they can enter the class II Mhc processing pathway. RECOGNITION BY HELPER T CELL DELIVERY OF PEPTIDE– MHC COMPLEX TO PLASMA MEMBRANE FOR RECOGNITION BY HELPER T CELL Golgi apparatus trans Golgi class II MHC protein late endosome early endosome folded protein antigenplasma membrane DENDRITIC OR TARGET CELL LIMITED PROTEOLYSIS OF ANTIGEN AND INVARIANT CHAIN LEAVES FRAGMENT OF INVARIANT CHAIN IN BINDING GROOVE OF MHC PROTEIN RELEASE OF INVARIANT CHAIN FRAGMENT AND BINDING OF ANTIGEN-DERIVED PEPTIDE INVARIANT CHAIN DIRECTS CLASS II MHC PROTEIN TO LATE ENDOSOME ENDOCYTOSIS AND DELIVERY TO ENDOSOME fragment of invariant chain CYTOSOL antigenic peptide "
# remove_text = "+ + + + + + + + + + + + + MS1 MS2inert gas"
def load_filenames():
    """
    load xml files in xml directory
    """
    os.chdir('xml')
    files = os.listdir()
    filenames= [filename for filename in files if filename[-4:]=='.xml']
    os.chdir('..')
    # return filenames
    return filenames
def confirm_directory():
    """
    asserts we are in the parent directory of the xml and txt files
    """
    assert('xml' in os.listdir() and 'raw_txt' in os.listdir())

class xml_txt:
    def __init__(self):
        confirm_directory()
        self.filenames = load_filenames()
        confirm_directory()
    def convert_xmls(self):
        for filename in self.filenames:
            self.convert_xml(filename)
            confirm_directory()
    def convert_xml(self, xml_filename):
        #parse xml
        confirm_directory()
        os.chdir('xml')
        data = self.parse_xml(xml_filename)
        os.chdir('../raw_txt')
        txt_filename = xml_filename[:-3]+"txt"
        self.export_txt(txt_filename, data)
        os.chdir('..')
        confirm_directory()

    def parse_xml(self, filename):
        assert(filename in os.listdir())
        assert(filename[-3:]=='xml')
        data = BeautifulSoup(open(filename, 'r'), "lxml")
        #we remove table entries
        for each in data.find_all("table"):
            each.decompose()
        for each in data.find_all("figure"):
            text = each.get_text()
            if ((not '.' in text) and (not ',' in text) and (not '?' in text) and (not '!' in text)):
                each.decompose()
        return data

    def export_txt(self, filename, data):
        text = self.format_text(data)
        assert(filename[-3:]=='txt')
        with open(filename, "w") as output:
            output.write(text)
    def format_text(self, data):
        assert(self.replace_text("- &lt;&gt;&amp;") == "<>&")
        text = data.get_text()
        return self.replace_text(text)

    def replace_text(self, text):
        for char, conversion in REPLACEMENTS.items():
            text = text.replace(char, conversion)
        return text
if __name__ == "__main__":
    converter = xml_txt()
    converter.convert_xmls()
