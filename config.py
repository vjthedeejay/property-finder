import os
basedir = os.path.abspath(os.path.dirname(__file__))

class DatabaseConfig(object):
    """ 
    Database configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'listings.db')

class CraigslistConfig(object):
    """
    Craigslist configuration
    """
    # URL data
    CRAIGSLIST_SITE = "sfbay"
    CRAIGSLIST_AREA = "eby"
    CRAIGSLIST_HOUSING_SECTION = "apa"
    
    # Filtering data
    MAX_PRICE = 4000
    ZIP_CODE = 94706        # Albany / N Berkeley
    SEARCH_DISTANCE = 3     # miles
    MIN_BEDS = 2

    # Additional filtering data
    BOXES = {
        "north_berkeley": [
            [37.870078, -122.307248],
            [37.904286, -122.260127]
        ]
    }
    NEIGHBORHOODS = [
        "berkeley north", 
        "albany",
    ]
    RESULTS_LIMIT = 100

class SlackConfig(object):
    """
    Slack configuration
    """
    SLACK_CHANNEL = "#housing"
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN') or ''

class AppConfig(object):
    """
    Application configuration
    """
    SLEEP_INTERVAL = 60 * 60 # 20 mins
