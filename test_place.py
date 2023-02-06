with open(r'C:\Users\major\Documents\GitHub\stash\pdf_editor\src\Сертификат_участника.pdf', 'rb') as file:
    text = (file.read())
    with open("first_page.txt", 'wb') as output_file:
         output_file.write(text)
