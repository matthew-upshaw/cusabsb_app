from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    mascot = models.CharField(max_length=50)
    #logo = models.ImageField(upload_to='team_logos', blank=True, null=True)
    abbreviation = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
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
