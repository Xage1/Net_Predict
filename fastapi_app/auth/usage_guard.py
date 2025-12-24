from datetime import date
from fastapi import HTTPException
from django_app.netpredict_core.models import ApiUsage

def check_usage(user, feature: str = None):
    today = date.today()

    usage, _ = ApiUsage.objects.get_or_create(
        user=user,
        date=today
    )

    plan = user.subscription.plan

    # DAILY LIMIT
    if usage.total_requests >= plan.daily_request_limit:
        raise HTTPException(
            status_code=429,
            detail="Daily request limit reached"
        )

    # MONTHLY LIMIT
    monthly_total = ApiUsage.objects.filter(
        user=user,
        date__month=today.month
    ).aggregate(models.Sum("total_requests"))["total_requests__sum"] or 0

    if monthly_total >= plan.monthly_request_limit:
        raise HTTPException(
            status_code=429,
            detail="Monthly request limit reached"
        )

    # FEATURE LIMIT (Exact Score)
    if feature == "exact_score":
        if not plan.allow_exact_score:
            raise HTTPException(status_code=403, detail="Upgrade required")

        if plan.exact_score_monthly_limit:
            exact_total = ApiUsage.objects.filter(
                user=user,
                date__month=today.month
            ).aggregate(models.Sum("exact_score_requests"))["exact_score_requests__sum"] or 0

            if exact_total >= plan.exact_score_monthly_limit:
                raise HTTPException(
                    status_code=429,
                    detail="Exact score monthly quota reached"
                )

    return usage