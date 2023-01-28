from mimetypes import MimeTypes
from urllib.request import pathname2url

mime = MimeTypes()
url = pathname2url('Daddy.jpg')
mime_type = mime.guess_type(url)
print( mime_type )
# ('application/xml', None)

def get_maintype(file_path : str) -> list:
        mime = MimeTypes()
        url = pathname2url(file_path)
        return ( mime.guess_type(url) )[0].split('/')

print( get_maintype('IMAGE 2023-01-19 22_43_10.pdf') )