from rest_framework.throttling import UserRateThrottle

class WatchlistThrottle(UserRateThrottle):
    scope = 'watchlist'
