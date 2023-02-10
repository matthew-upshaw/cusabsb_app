from django.db import models
from django.core.exceptions import ValidationError
import xml.etree.cElementTree as et
from PIL import Image

def validate_svg(f):
    f.seek(0)
    tag = None
    try:
        for event, el in et.iterparse(f, ('start',)):
            tag = el.tag
            break
    except et.ParseError:
        pass

    if tag != '{http://www.w3.org/2000/svg}svg':
        raise ValidationError('Uploaded file is not an SVG file.')
    
    f.seek(0)

    return f


class Team(models.Model):
    name = models.CharField(max_length=50)
    mascot = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='team_logos', blank=True, null=True)
    logo_svg = models.FileField(upload_to='team_logos', validators=[validate_svg], blank=True, null=True)
    year_joined = models.CharField(max_length=50)
    year_left = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    bsb_page = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)
        width, height = img.size
        new_height = 64
        new_width = int(new_height/height*width)
        img.thumbnail((new_width, new_height))
        img.save(self.logo.path)
    
class Record(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    wins_overall = models.IntegerField()
    losses_overall = models.IntegerField()
    ties_overall = models.IntegerField()
    wins_conf = models.IntegerField()
    losses_conf = models.IntegerField()
    ties_conf = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return self.team.name+' '+str(self.year)
