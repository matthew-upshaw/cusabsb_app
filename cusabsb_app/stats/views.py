from django.shortcuts import render
from django.db.models import IntegerField, F
from django.db.models.functions import Cast

from stats.models import (
    Batter,
    Pitcher,
    Fielder,
)

from teams.models import (
    Team,
    Record,
)

def stat_home(request):
    batters = Batter.objects.all()
    pitchers = Pitcher.objects.all()
    fielders = Fielder.objects.all()

    current_avg_leaders = Batter.objects.annotate(
        games_played_int=Cast('games_played',output_field=IntegerField())
    ).filter(
        is_latest=True,games_played_int__gte=10
    ).order_by(
        '-avg'
    )[:5]

    current_ops_leaders = Batter.objects.annotate(
        games_played_int=Cast('games_played',output_field=IntegerField())
    ).filter(
        is_latest=True,games_played_int__gte=10
    ).order_by(
        '-ops'
    )[:5]

    current_hr_leaders = Batter.objects.annotate(
        games_played_int=Cast('games_played',output_field=IntegerField())
    ).annotate(
        homeruns_int=Cast('homeruns',output_field=IntegerField())
    ).filter(
        is_latest=True,games_played_int__gte=10
    ).order_by(
        '-homeruns_int'
    )[:5]

    standings = Record.objects.filter(
        year=2022
    ).annotate(
        win_percentage=(1*F('wins_conf')+0.5*F('ties_conf'))/(F('wins_conf')+F('ties_conf')+F('losses_conf'))
    ).order_by(
        '-win_percentage'
    )

    context = {
        'batters': batters,
        'pitchers': pitchers,
        'fielders': fielders,
        'current_avg_leaders': current_avg_leaders,
        'current_ops_leaders': current_ops_leaders,
        'current_hr_leaders': current_hr_leaders,
        'standings': standings,
    }

    return render(request, 'stat_home.html', context)
