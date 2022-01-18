from rest_framework.throttling import UserRateThrottle

class OTPBurst(UserRateThrottle):
    scope = 'otp_burst'

class OTPSustained(UserRateThrottle):
    scope = 'otp_sustained'

class OTPRate(UserRateThrottle):
    scope = 'otp_rate'
