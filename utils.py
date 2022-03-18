import re

def validate_number(number):
    if re.search(r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$', number):
        return True
    else:
        return False
