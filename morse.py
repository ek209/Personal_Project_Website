#This code translates English strings into morse code.

#Dictionary for morse code translations
#Codes end with space to account for singular 
#Space needed after letters too account for character spacing in morse code
morse_dict = {'a' : '.- ', 'b' : '-... ', 'c' : '-.-. ',
              'd' : '-.. ', 'e' : '. ', 'f' : '..-. ',
              'g' : '--. ', 'h' : '.... ', 'i' : '.. ',
              'j' : '.--- ', 'k' : '-.- ', 'l' : '.-.. ',
              'm' : '-- ', 'n' : '-. ', 'o' : '--- ', 
              'p' : '.--. ', 'q' : '--.- ', 'r' : '.-. ',
              's' : '... ', 't' : '- ', 'u' : '..- ',
              'v' : '...- ', 'w' : '.-- ', 'x' : '-..- ',
              'y' : '-.-- ', 'z' : '--.. ', '0' : '----- ',
              '1' : '.---- ', '2' : '..--- ', '3' : '...-- ',
              '4' : '....- ', '5' : '..... ', '6' : '-.... ',
              '7' : '--... ', '8' : '---.. ', '9' : '----. ',
              '.' : '.-.-.- ', ',' : '--..-- ', '?' : '..--.. ',
              "'" : '.----. ', '!' : '-.-.--', '/' : '-..-. ',
              '(' : '-.--. ', ')' : '-.--.- ', '&' : '.-... ',
              ':' : '---... ', ';' : '-.-.-. ', '=' : '-...- ',
              '+' : '.-.-. ', '-' : '-....- ', '_' : '..--.- ',
              '"' : '.-..-. ', '$' : '...-..- ', '@' : '.--.-. ',
              ' ' : '/ '}

#Creates a new dict with key, value swap and reorders by 
#key length
def dict_key_len_reorder():
    orig_list = [[value, key] for key, value in morse_dict.items()]
    orig_list.sort(reverse=True, key = lambda x: len(x[0]))
    return { kv_pair[0] : kv_pair[1] for kv_pair in orig_list}

reverse_morse_dict = dict_key_len_reorder()


#Converts morse string back to english
#Converting dictionary needs to be in descending order
#of the key length to translate correctly
def morse_to_english(text):
    text = text.lower()
    special_key_dict = {'-' : '@@dash@@',
                        '.' : '@@dot@@',
                        '/' : '@@slash@@'}
    reverse_special_key_dict = {value : key for key, value in special_key_dict.items()}
    for key, value in reverse_morse_dict.items():
        if key in text:
            if value in special_key_dict.keys():
                text = text.replace(key, special_key_dict[value])
            else:
                text = text.replace(key, value)
    for key, value in reverse_special_key_dict.items():
        text = text.replace(key, value)
    return text

#Converts string to morse
def english_to_morse(text):
    text = text.lower()
    morse_table = str.maketrans(morse_dict)
    return text.translate(morse_table)



