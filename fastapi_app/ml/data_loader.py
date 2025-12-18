import pandas as pd 
from django_app.netpredict_core.models import Team, Player, Match, PlayerMatchStats, Odds, League

class DataLoader:
    @staticmethod
    def load_matches(start_date=None, end_date=None, leagues=None):
        """
        Returns a Pandas DataFrame of matches filtered by date and leagues.
        """

        qs = Match.objects.select_related('league', 'home_team', 'away_team')
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        if leagues:
            qs = qs.filter(league__name__in=leagues)

        data = []
        for m in qs:
            data.append({
                "match_id": str(m.id),
                "date": m.date,
                "league": m.league.name,
                "home_team": m.home_team.name,
                "away_team": m.away_team.name,
                "home_goals": m.home_goals,
                "away_goals": m.away_goals,
                "home_xg": m.home_xg,
                "away_xg": m.away_xg,
                "home_red_cards": m.home_red_cards,
                "away_red_cards": m.away_red_cards,
            })
        return pd.DataFrame(data)

    @staticmethod
    def load_odds():
        """
        Returns match odds for calibration.
        """

        qs = Odds.objects.select_related('match')
        data = []
        for o in qs:
            data.append({
                "match_id": str(o.match.id),
                "home_win": o.home_win,
                "draw": o.draw,
                "away_win": o.away_win,
            })
        return pd.DataFrame(data)