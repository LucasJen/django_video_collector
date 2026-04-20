from django.db import models
from urllib import parse
from django.core.exceptions import ValidationError

class Video(models.Model):
    # Create model to store video uploads
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    def save(self, *args, **kwargs): #override save to be able to extract video id from url
        
        # Validates that the url is a youtube url
        if not self.url.startswith('https://www.youtube.com/watch'):
            raise ValidationError(f'Not a Youtube URL: {self.url}')
        
        url_components = parse.urlparse(self.url)
        query_string = url_components.query # i.e  v=1235235
        if not query_string:
            raise ValidationError('Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True) # sets up dictionary strict parsing ensure valid query string
        v_parameters_list = parameters.get('v') # looks for dictionary "v" key
        if not v_parameters_list: # Checking if None or empty list
            raise ValidationError(f'Invalid Youtube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] 

        super().save(*args, **kwargs)

            


    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id}, Notes: {self.notes[:200]}'

    
