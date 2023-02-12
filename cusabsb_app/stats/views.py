from django.shortcuts import render
from django.db.models import IntegerField, FloatField, F, Prefetch
from django.db.models.functions import Cast

from stats.models import Batter, Pitcher, Fielder
from teams.models import Team, Record

def stat_home(request,year):
    batters = Batter.objects.filter(year=year, is_latest=True).order_by('-ops')
    pitchers = Pitcher.objects.filter(year=year, is_latest=True).order_by('era')
    fielders = Fielder.objects.filter(year=year, is_latest=True)

    qualified_batters = (
        Batter.objects.filter(year=year, is_latest=True)
        .annotate(games_played_float=Cast('games_played', output_field=FloatField()))
        .annotate(ab_float=Cast('ab', output_field=FloatField()))
        .annotate(ab_per_game=F('ab_float')/F('team_games'))
        .annotate(gp_ratio=F('games_played_float')/F('team_games'))
        .filter(ab_per_game__gte=2, gp_ratio__gte=0.75)
        .order_by('-ops')
    )

    qualified_pitchers = (
        Pitcher.objects.filter(year=year, is_latest=True)
        .annotate(ip_float=Cast('ip', output_field=FloatField()))
        .annotate(ip_per_game=F('ip_float')/F('team_games'))
        .filter(ip_per_game__gte=1)
        .order_by('era')
    )

    current_avg_leaders = (
        Batter.objects.annotate(games_played_int=Cast('games_played',output_field=IntegerField()))
        .filter(is_latest=True,games_played_int__gte=10)
        .order_by('-avg')[:5]
    )

    current_ops_leaders = (
        Batter.objects.annotate(games_played_int=Cast('games_played',output_field=IntegerField()))
        .filter(is_latest=True,games_played_int__gte=10)
        .order_by('-ops')[:5]
    )

    current_hr_leaders = (Batter.objects.annotate(games_played_int=Cast('games_played',output_field=IntegerField()))
        .annotate(homeruns_int=Cast('homeruns',output_field=IntegerField()))
        .filter(is_latest=True,games_played_int__gte=10)
        .order_by('-homeruns_int')[:5]
    )

    standings = (
        Record.objects.filter(year=year)
        .annotate(win_percentage=(1*F('wins_conf')+0.5*F('ties_conf'))/(F('wins_conf')+F('ties_conf')+F('losses_conf')))
        .order_by('-win_percentage')
    )

    context = {
        'batters': batters,
        'pitchers': pitchers,
        'fielders': fielders,
        'qualified_batters': qualified_batters,
        'qualified_pitchers': qualified_pitchers,
        'current_avg_leaders': current_avg_leaders,
        'current_ops_leaders': current_ops_leaders,
        'current_hr_leaders': current_hr_leaders,
        'standings': standings,
        'year': year,
    }

    return render(request, 'stat_home.html', context)
