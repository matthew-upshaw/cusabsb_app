from django.db import models
from teams.models import Team

class Batter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    avg = models.CharField(max_length=50)
    obp = models.CharField(max_length=50)
    slg = models.CharField(max_length=50)
    ops = models.CharField(max_length=50)
    ab = models.CharField(max_length=50)
    runs = models.CharField(max_length=50)
    hits = models.CharField(max_length=50)
    doubles = models.CharField(max_length=50)
    triples = models.CharField(max_length=50)
    homeruns = models.CharField(max_length=50)
    rbi = models.CharField(max_length=50)
    tb = models.CharField(max_length=50)
    bb = models.CharField(max_length=50)
    hbp = models.CharField(max_length=50)
    so = models.CharField(max_length=50)
    gdp = models.CharField(max_length=50)
    sf = models.CharField(max_length=50)
    sh = models.CharField(max_length=50)
    games_played = models.CharField(max_length=50)
    games_started = models.CharField(max_length=50)
    stolen_bases = models.CharField(max_length=50)
    stolen_bases_attempted = models.CharField(max_length=50)
    updated_at = models.DateTimeField()
    is_latest = models.BooleanField()
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name+' '+self.last_name+' - '+self.team.name

class Pitcher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    games_appeared = models.CharField(max_length=50)
    games_started = models.CharField(max_length=50)
    era = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
    wins = models.CharField(max_length=50)
    losses = models.CharField(max_length=50)
    whip = models.CharField(max_length=50)
    cg = models.CharField(max_length=50)
    sho = models.CharField(max_length=50)
    sv = models.CharField(max_length=50)
    hits = models.CharField(max_length=50)
    runs = models.CharField(max_length=50)
    earned_runs = models.CharField(max_length=50)
    bb = models.CharField(max_length=50)
    so = models.CharField(max_length=50)
    doubles = models.CharField(max_length=50)
    triples = models.CharField(max_length=50)
    homeruns = models.CharField(max_length=50)
    ab = models.CharField(max_length=50)
    b_avg = models.CharField(max_length=50)
    wp = models.CharField(max_length=50)
    hbp = models.CharField(max_length=50)
    bk = models.CharField(max_length=50)
    sfa = models.CharField(max_length=50)
    sha = models.CharField(max_length=50)
    updated_at = models.DateTimeField()
    is_latest = models.BooleanField()
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name+' '+self.last_name+' - '+self.team.name
    
class Fielder(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    catches = models.CharField(max_length=50)
    putouts = models.CharField(max_length=50)
    assists = models.CharField(max_length=50)
    errors = models.CharField(max_length=50)
    fld = models.CharField(max_length=50)
    dp = models.CharField(max_length=50)
    sba = models.CharField(max_length=50)
    csb = models.CharField(max_length=50)
    pb = models.CharField(max_length=50)
    ci = models.CharField(max_length=50)
    updated_at = models.DateField()
    is_latest = models.BooleanField()
    year = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name+' '+self.last_name+' - '+self.team.name
    