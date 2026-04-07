

import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict

def print_secret_message(doc_url: str) -> None:
  
    response = requests.get(doc_url)
    response.raise_for_status()  
    
    soup = BeautifulSoup(response.text, 'html.parser')
    full_text = soup.get_text(separator='\n')
    
    pattern = r'[^\d]*(\d+)[^\d]*(\d+)[^\d]*([^\s\n]+)'
    matches = re.findall(pattern, full_text)
    
    char_map = defaultdict(lambda: ' ')
    max_x = 0
    max_y = 0
    
    for match in matches:
        if len(match) != 3:
            continue
        x_str, y_str, char_part = match
        try:
            x = int(x_str)
            y = int(y_str)
        except ValueError:
            continue
        
        char = char_part.strip()
        if char.startswith('U+'):
            try:
                char = chr(int(char[2:], 16))
            except ValueError:
                pass
        
        char_map[(x, y)] = char
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    if max_x == 0 and max_y == 0:
        print("No valid coordinates found.")
        return
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append(char_map[(x, y)])
        print(''.join(row))

print_secret_message("https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1")
