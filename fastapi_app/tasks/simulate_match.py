from celery import shared_task
from ml.simulation.monte_carlo import simulate_match

@shared_task(bind=True)
def simulate_match_task(self, lambda_home, lambda_away):
    return simulate_match(lambda_home, lambda_away, sims=20000)
