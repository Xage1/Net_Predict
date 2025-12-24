class UserSubscription(models.Model):
    """
    Active subscription for a user.

    - One active subscription per user
    - Decoupled from payment providers
    - Enforces feature and usage access
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def has_feature(self, feature: str) -> bool:
        """
        Generic feature check.
        Example: has_feature("allow_exact_score")
        """
        return self.is_active and getattr(self.plan, feature, False)

    def can_use_exact_score(self, used_this_month: int) -> bool:
        """
        Enforces exact score limits (PRO vs ELITE).
        """
        if not self.plan.allow_exact_score:
            return False

        if self.plan.exact_score_monthly_limit is None:
            return True  # Unlimited (Elite)

        return used_this_month < self.plan.exact_score_monthly_limit

    def __str__(self):
        return f"{self.user.username} → {self.plan.name}"