from config import CraigslistConfig, SlackConfig, AppConfig
from craigslist_housing_filter import CraigslistHousingFilter
from slack_bot import SlackBot
import time

def main():
    while True:
        # create objects
        cl_filter = CraigslistHousingFilter(CraigslistConfig)
        slack_bot = SlackBot(SlackConfig)

        # get matching Craigslist results
        results = cl_filter.get_matching_results()

        # post results to Slack
        for result in results:
            text = "{0} | {1} | {2} | <{3}>".format(
                result['where'],
                result['price'],
                result['name'],
                result['url']
            )
            slack_bot.post_to_channel(text)

        # sleep for an hour before repeating
        time.sleep(AppConfig.SLEEP_INTERVAL)


if __name__ == "__main__":
    main()
