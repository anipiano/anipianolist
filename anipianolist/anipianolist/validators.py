# H/t https://www.learningaboutelectronics.com/Articles/How-to-restrict-the-size-of-file-uploads-with-Python-in-Django.php
# "I'm not lazy, I'm just conserving energy" ~ Oreki Houtarou from Hyouka

from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 10*1024*1024:
        raise ValidationError("The maximum file size that can be uploaded is 10MB, baka!")
    else:
        return value
