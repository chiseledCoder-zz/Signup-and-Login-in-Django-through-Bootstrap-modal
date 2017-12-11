
class UserAccount(models.Model):
	user = models.OneToOneField(User, related_name='userprofile')
	is_corporate = models.BooleanField(default=False, blank=True)
	is_cakemporos_baker = models.BooleanField(default=False, blank=True)
	is_first_time_user = models.BooleanField(default=False, blank=True)
	phone = models.CharField(validators=[phone_regex], blank=False, max_length=20, unique=True)
	user_locality = models.ForeignKey(Locality, blank=True, null=True)
	coupon = models.ManyToManyField(Coupon, default="", blank=True)
	reward_id = models.CharField(max_length=120, default='ABC', unique=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.phone

	class Meta:
		verbose_name_plural = 'User Accounts'
        unique_together = ("id", "phone", "reward_id")