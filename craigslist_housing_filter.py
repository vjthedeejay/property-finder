from craigslist import CraigslistHousing
from config import DatabaseConfig
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from dateutil.parser import parse

engine = create_engine(DatabaseConfig.SQLALCHEMY_DATABASE_URI, echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class CraigslistHousingFilter(object):
    """
    Class that retreives and filters Craiglist housing listings
    and writes the filtered listings to a database
    """
    def __init__(self, config):
        """
        Set instance attributes and create CraigslistHousing object
        Args:
            config (class): contains configuration data
        """
        self.config = config

        self.cl_h = CraigslistHousing(
            site=config.CRAIGSLIST_SITE,
            area=config.CRAIGSLIST_AREA,
            category=config.CRAIGSLIST_HOUSING_SECTION,
            filters={
                'has_image': True,
                'search_distance': config.SEARCH_DISTANCE,
                'zip_code': config.ZIP_CODE,
                'max_price': config.MAX_PRICE,
                'min_bedrooms': config.MIN_BEDS,
                'laundry': ['w/d in unit'],
            #   'cats_ok': True,
            })

    def get_matching_results(self):
        """
        Method to get and filter results
        """
        results = []

        # get results
        gen = self.cl_h.get_results(
            sort_by='newest', 
            geotagged=True,
            limit=self.config.RESULTS_LIMIT)

        # go through all results
        while True:
            try:
                result = next(gen)
            except StopIteration:
                break
            except Exception:
                continue

            # match is false by default
            match = False

            # check if location of listing is in geolocation box
            if self.is_in_box(result['geotag']):
                match = True
            
            # check if neighborhood matches
            if result['where'] and \
               self.is_in_neighborhood(result['where']):
                match = True

            if match:
                # check if listing exists in database
                listing = session.query(Listing).filter_by(cl_id=result['id']).first()

                # if listing doesn't exist, add to database and append 
                if listing is None:
                    # try parsing the price
                    price = 0
                    try:
                        price = float(result['price'].replace("$", ""))
                    except Exception:
                        pass
                
                    # create listing object
                    listing = Listing(
                        link=result['url'],
                        created=parse(result['datetime']),
                        name=result['name'],
                        price=price,
                        location=result['where'],
                        cl_id=result['id'],
                    )

                    # save the listing
                    session.add(listing)
                    session.commit()
                    
                    # append result
                    results.append(result)

        # return matching results
        return results

    def is_in_box(self, coords):
        """
        Helper method to determine if incoming coordinates exist within a box
        """
        box = self.config.BOXES['north_berkeley']
        if coords is not None and \
           box[0][0] < coords[0] < box[1][0] and \
           box[0][1] < coords[1] < box[1][1]:
            return True
        else:
            return False

    def is_in_neighborhood(self, location):
        """
        Helper method to determine if a location exists within a neighborhood
        """
        for neighborhood in self.config.NEIGHBORHOODS:
            if neighborhood in location:
                return True
        
        return False