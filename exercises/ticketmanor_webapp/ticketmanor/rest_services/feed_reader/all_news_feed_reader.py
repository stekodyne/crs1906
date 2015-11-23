"""
all_news_feed_reader.py - reads multiple RSS news feeds to populate the
Read All News page.
"""
from threading import Thread

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from time import sleep
from ticketmanor.rest_services.feed_reader.feed_reader import (
    FeedReader,
)


class AllNewsFeedReader:
    """Reads news feeds for music, concerts, and sports"""
    def __init__(self):
        self.feed_reader = FeedReader()

    def get_news(self, max_items=0):
        """
        Get news items of all news types.

        If max_items > 0, return no more than max_items news items.
        Otherwise, return all news items.
        """
        concert_news = self.worker('concerts', max_items)
        sports_news = self.worker('sports', max_items)
        movie_news = self.worker('movies', max_items)
        return {
            'concerts': concert_news,
            'sports': sports_news,
            'movie': movie_news
        }

    def worker(self, news_type, max_items):
        sleep(1)  # pause, to simulate a slow response (needed for ex 9.2)
        return self.feed_reader.fetch_news_items(news_type, max_items)
