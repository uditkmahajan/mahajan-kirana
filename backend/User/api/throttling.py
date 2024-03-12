from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class AnnonThrottle(AnonRateThrottle) :
    rate = '100/hour' 

class UserThrottle(UserRateThrottle) :
    rate = '10/hour'
