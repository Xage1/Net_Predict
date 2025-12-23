class UserSubscription(models.Model):
    """
    Active subscription per user.
    Decoupled from payment provider.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def has_access(self, feature: str) -> bool:
        return getattr(self.plan, feature, False)