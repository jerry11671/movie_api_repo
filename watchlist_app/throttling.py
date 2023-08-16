from rest_framework.throttling import UserRateThrottle

class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    
class ReviewDetailThrottle(UserRateThrottle):
    scope = 'review-detail'