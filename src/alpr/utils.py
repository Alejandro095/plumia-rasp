import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

def format_license(text):
    
    if (text is None):
        return None

    formated_text = text.upper().strip().replace(' ', '-')

    if (len(formated_text) < 9):
        return None
    if (formated_text[3] != '-'):
        return None
    if (formated_text[6] != '-' and formated_text[7] != '-'):
        return None
    
    formated_text = formated_text[:9]

    first_char: str = formated_text[0]

    if (not first_char.isalpha()):        
        if (first_char in dict_int_to_char):
            first_char = dict_int_to_char[first_char]
        else:
            return None


    second_char: str = formated_text[1]

    if (not second_char.isalpha()):
        if (second_char in dict_int_to_char):
            second_char = dict_int_to_char[second_char]
        else:
            return None

    three_char = formated_text[2]

    if (not three_char.isalpha()):
        if (three_char in dict_int_to_char):
            three_char = dict_int_to_char[three_char]
        else:
            return None
        
    four_char: str = formated_text[4]

    if (not four_char.isnumeric()):
        if (four_char in dict_char_to_int):
            four_char = dict_char_to_int[four_char]
        else:
            return None
        
    five_char: str = formated_text[5]

    if (not five_char.isnumeric()):
        if (five_char in dict_char_to_int):
            five_char = dict_char_to_int[five_char]
        else:
            return None
    
    result = first_char + second_char + three_char + '-' + four_char + five_char
    
    if (formated_text[6] == '-'):

        six_char: str = formated_text[7]

        if (not six_char.isnumeric()):
            if (six_char in dict_char_to_int):
                six_char = dict_char_to_int[six_char]
            else:
                return None
            
        seven_char: str = formated_text[8]

        if (not seven_char.isnumeric()):
            if (seven_char in dict_char_to_int):
                seven_char = dict_char_to_int[seven_char]
            else:
                return None
            
        return result + '-' + six_char + seven_char
    else:
        six_char: str = formated_text[6]

        if (not six_char.isnumeric()):
            if (six_char in dict_char_to_int):
                six_char = dict_char_to_int[six_char]
            else:
                return None
            
        seven_char: str = formated_text[8]

        if (not seven_char.isalpha()):
            if (seven_char in dict_char_to_int):
                seven_char = dict_char_to_int[seven_char]
            else:
                return None
        
        return result + six_char + '-' + seven_char


def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        formated_text = format_license(text)
        
        if (formated_text is not None):
            return formated_text;

        