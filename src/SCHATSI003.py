# SCHATSI003 - Data Cleansing

import re


"""
SCHATSI003.1: Counting words for a paper

1. string_preparation:
- at first: lower all letters, so that there is no difference between "Apple" and "apple"
- split the string in two parts: the text and the references

2. count_words: All words in the 'low_string_without_references' -> Total Words (in the moment with all filling Words
    (later this filling words will be filtered out)

"""


def string_preparation(input_text):
    # lower all letters, so theres no difference between words like "Computer" and "computer" for example
    low_string = input_text.lower()

    try:
        # Position in the string, where the last occurence of "reference" starts
        last_time_reference = low_string.rindex("\nreference")
    except:
        # If the string didnt contain the word "reference", which means that there arent any references (for example
        # when the pdf is just an abstract) the whole document is used as text and the reference string is empty
        low_string_without_references = low_string
        references = ""
    else:
        # Only consider the part of the string without the references -> Use this string for text analysis
        low_string_without_references = low_string[0:last_time_reference]
        # Text which contains all references
        references = low_string[last_time_reference:]

    return low_string_without_references, references

# Function to count all words in the text (without references), iterating over the string, when a seperator char like " " or a break like "\n" is found and the letter after that is neither a sep or a break a new word was found and the number of words increases by 1
def count_words(input_text):
    num_words = 0
    past_letter = " "
    for i in input_text:
        actual_letter = i
        if past_letter == " " or past_letter == "\n" or past_letter == "\t":
            if actual_letter != " " and actual_letter != "\n" and actual_letter != "\t":
                num_words = num_words + 1
        past_letter = actual_letter

    # total_num_words = len(input_text.strip().split(" "))
    return num_words


"""SCHATSI003.2: Extract the Metadata from the Paper
    - Author
    - Year of publication 
    - title
    - origin, like the book, a database or a convention paper
"""

# The Extraction of meta data couldn't be realised in the past, because the place in the papers where this informations appear are not normed -> high effort for correct detection
def metadata_author(input_text):
    pass


def metadata_year(input_text):
    pass


def metadata_title(input_text):
    pass


def metadata_origin(input_text):
    pass


"""SCHATSI003.3: Extract all References from the paper and store the Information in a new file -> one for each paper

"""
# The functions to find and cut the references from the String were implemented in the past, will not be called in the moment in the main-function, because the papers references and citation styles aren't normalized, so that the quality of detection varies fromm paper to paper
# In the moment, the year could be found quite good, other parts need an update
# Problems are, that there are far more different styles for the references and that the start char chain could appear in the middle of a citation, which disturbes the algorithm, for example when a digit appears in the title of a string like "1. Time ....."

# A possible solution could be the usage of "regular expression to modell different styles and detect them better.
# Another one could be to search in the references line-wise and detect when a reference ends, so it would not be nessesary to search for seperators
def reference_data_cutting(input_text):
    # Input: String, every String contains 1 reference
    # for different sorts of literature the cutting could be different
    if input_text == "":
        return "No REFERENCES FOUND" "NO REFERENCES FOUND" "NO REFERENCES FOUND"
    reference_year = ""
    # search for the year
    numbers_in_string = re.findall('([0-9]*)', input_text)
    for element in numbers_in_string:
        # for every Reference, there can only be one number for the year
        # and the will appear before other numbers like the DOI
        # if found: break out
        try:
            if (int(element) > 1950) and (int(element) < 2040):
                reference_year = element
                break
        except:
            continue
    # search for the author
    reference_author = input_text[:input_text.find(":")]

    # search for the title
    reference_title = input_text[input_text.find(":")+1:]
    if "In:" in reference_title:
        reference_title = reference_title[:reference_title.find("In:")]
    elif "available at:" in reference_title:
        reference_title = reference_title[:reference_title.find("available at:")]
    elif ". " in reference_title:
        reference_title = reference_title[:reference_title.find(". ")]
    elif "(" in reference_title:
        reference_title = reference_title[:reference_title.find("(")]
    elif str(reference_year) in reference_title:
        reference_title = reference_title[:reference_title.find(reference_year)]

    # print("REFERENCE AUTHOR: " + reference_author + " REFERENCE YEAR: " + reference_year + " REFERENCE TITLE: "
    # + reference_title)
    return reference_author, reference_year, reference_title

# This function tries to seperate the particular references by finding their start char chain, for example [1]......[2].....[3]... or pure 1 ..... 2....
# 4 Styles are detected in the moment: [1], 1., 1 and a pure citation one after another, which will be seperated by a line-break \n
def references(input_text):

    ref_list = []
    number = 1

    # check if there are any References in the File: If empty, return empty list
    if len(input_text) == 0 or len(input_text) == 1:
        return ref_list

    else:
        # Seperatorstyle detection if the reference string is not empty -> search for the start string to find out which style is used
        if input_text.find("[1]") >= 0:
            seperator = "[" + str(number) + "] "
            next_sep = "[" + str(number+1) + "] "
            style = 0
        elif input_text.find("1.") >= 0:
            seperator = str(number) + ". "
            next_sep = str(number+1) + ". "
            style = 1
        elif input_text.find("1 ") >= 0:
            seperator = str(number) + " "
            next_sep = str(number+1) + " "
            style = 2
        else:
            # Files which lists the references without any seperator
            seperator = "\n"
            next_sep = "\n"
            style = 3
        # Textpreparation: Cutting of all things before the first appearence of the seperator
        first_appearence_sep = input_text.find(seperator)
        pure_references = input_text[first_appearence_sep:]

        # input here: Text, which starts with a seperator
        # For Style 0,1,2:
        if style < 3:
            while next_sep in pure_references:
                # For every reference style create a seperator for the beginning and for the end of one reference
                if style == 0:
                    seperator = "[" + str(number) + "]"
                    next_sep = "[" + str(number + 1) + "]"
                elif style == 1:
                    seperator = str(number) + "."
                    next_sep = str(number + 1) + "."
                elif style == 2:
                    seperator = str(number) + " "
                    next_sep = str(number + 1) + " "

                # If there are more then one Reference
                if next_sep in pure_references:
                    ref = pure_references[pure_references.find(seperator):pure_references.find(next_sep)]
                    pure_references = pure_references[pure_references.find(next_sep):]
                    ref = ref.replace(seperator, "", 1)
                    #print(ref)
                    ref_list.append(ref)

                    number = number + 1
                # for the last reference -> Everything left from the input-text into the last entry
                else:
                    ref = pure_references[pure_references.find(seperator):]
                    ref = ref.replace(seperator, "", 1)
                    #print(ref)
                    ref_list.append(ref)
                    number = number + 1
        # For style 3, which dont use numbers
        else:
            #print("\nStyle 3 Condition arrived\n")
            n = 0
            while len(pure_references) > 1:
                sep1 = pure_references.find(seperator)
                sep2 = pure_references.find(seperator, sep1+1)
                ref = pure_references[sep1:sep2]

                #print("seperator position: ", sep1)
                #print("next sep. position: ", sep2)
                #print("\"", ref, "\"\n")

                n = n+1
                pure_references = pure_references.replace(ref, "", 1)
                ref = ref.replace(seperator, "", 1)

                ref_list.append(ref)
        # Output is a python list which contains the seperated reference strings -> In this strings the title, year etc. could be found
        return ref_list
