import csv
import xml.etree.ElementTree as ET

def parseDrug(drugData):
    '''
    Parses input XML data of an individual drug given by {drugData}
    and returns a condensed JSON representation.

        Parameters:
            drugData (XML Element)
                    ElementTree Element Object holding drug information from DrugBank

        Returns:
            A JSON representation of drug name mapping data with formatting
              * generic_name (string)
              * brand_names (list of strings)

        Requires:
            {drugData} formatting is consistent with DrugBank formatting

        Ensures:
            {parseDrug} = [a JSON representation of a subset of the data contained
            in {drugData}, with the formatting described in {Returns}]. If {drugData}
            is not consistent with DrugBank formatting, an error is thrown and
            program execution stops
    '''
    # Obtain generic_name attribute from {drugData}
    try:
        drugGenericName = drugData.find('{http://www.drugbank.ca}name').text.lower()
    except:
        print("Error: could not retrieve generic name data of drug")
        exit()


    # Obtain brand_name attribute from {drugData}
    drugBrandNames = set()
    try:
        products = drugData.find('{http://www.drugbank.ca}products')
        for product in products.findall('{http://www.drugbank.ca}product'):
            brandName = product.find('{http://www.drugbank.ca}name').text.lower()
            drugBrandNames.add(brandName)
    except KeyError:
        print("Error: could not retrieve brand name data of drug")
        exit()

    # Create and populate condensed JSON representation of drug
    drugDataRep = {}
    drugDataRep["generic_name"] = drugGenericName
    drugDataRep["brand_names"] = drugBrandNames

    return drugDataRep

def parseFile(inputFile, out):
    '''
    Parses input XML data given by {inputFile} and appends drug name mapping data 
    for all properly formatted drugs in {inputFile} to {out}.

        Parameters:
            inputFile (string)
                    file path of DrugBank input file
            out (DictWriter)
                    output stream to csv file

        Updates:
            out

        Requires:
            {inputFile} is a valid file path to a readable XML file in proper DrugBank format,
            {out} is open,
            {out} contains a valid csv header with two features

        Ensures:
            The content of {out} is updated to contain all drug name mappings contained in
            {inputFile}. If the input file cannot be opened or read, an error is thrown and 
            program execution stops
    '''
    # Open and read in data from {inputFile}
    try:
        tree = ET.parse(inputFile)
    except:
        print("Error: could not read in data from file " + inputFile);
        exit()

    root = tree.getroot()

    # Parse and print data of each drug in {inputFile}
    for drug in root:
        drugMapping = parseDrug(drug)
        # Prints a new line for every unique brand name associated with each generic name
        for brandName in drugMapping["brand_names"]:
            row = {}
            row["brand_name"] = brandName
            row["generic_name"] = drugMapping["generic_name"]
            out.writerow(row)

def main():
    '''
    Main method for drugBankParser.
    Outputs a csv file with mappings between drug brand names and drug generic names.
    All input text is converted to lowercase. Otherwise, output mappings are as
    exactly as they appear in input.

    Data is read in from xml file with relative path {DATA_FILE}.
    Output file is named {OUTPUT_FILE_PATH} and follows formatting {FIELD_NAMES}.
    If output file already exists, all data will be overridden.
    '''
    # Configuration constants
    DATA_FILE = "rawData.xml"
    OUTPUT_FILE_PATH = "drugMapping.csv"
    FIELD_NAMES = ["brand_name", "generic_name"]

    # Open output stream and initialize with csv header
    outputFile = open(OUTPUT_FILE_PATH, "w")
    writer = csv.DictWriter(outputFile, fieldnames=FIELD_NAMES)
    writer.writeheader()

    # Parse and print data from input file
    parseFile(DATA_FILE, writer)

if __name__ == "__main__":
    main()
