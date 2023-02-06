from PyPDF2 import PdfReader

from PyPDF2 import PdfWriter

from PyPDF2.generic import DecodedStreamObject, EncodedStreamObject, NameObject

from pathlib import Path
from pprint import pprint

pdf_path = "pdf_editor\src\Сертификат_участника.pdf"

pdf = PdfReader(pdf_path)

pdf_writer = PdfWriter()

for page in pdf.pages:
    print( page.extract_text() )
    
    text = page.extract_text()
    text = text.replace('Фамилия', 'Пыня')
    text = text.replace('Имя', 'Владимирович')
    text = text.replace('____', 'Дохуя')
    
    print(text)
    # page.writeToStream()
        
    pdf_writer.add_page(page)

with open("first_page.pdf", 'wb') as output_file:
    pdf_writer.write(output_file)

