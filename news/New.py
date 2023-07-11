"""
New.py is a module that contains the class New.
"""
import hashlib
from datetime import datetime


class New:
    """
    New is a class that contains the attributes of a new.
    """

    def __init__(self, title, url, image_url, summary, category, date):
        """
        Constructor of the class New.
        :param title: title of the new
        :param url: url of the new
        :param image_url: image url of the new
        :param summary: summary of the new (Could be None)
        :param category: category of the new
        :param date: date of the new (Could be None)
        """
        self.title = title
        self.url = url
        if image_url is None:
            self.image_url = ""
        else:
            self.image_url = image_url
        if summary is None:
            self.summary = ""
        else:
            self.summary = summary
        self.category = category
        # if date is None then date is today
        if date is None:  # Save date in format "MM DD, YYYY", EX: "July 11, 2023"
            self.date = datetime.today().strftime("%B %d, %Y")
        else:
            self.date = date
        self.id = self.__hash__()

    def __eq__(self, other):
        """
        Returns True if the objects are equal, False if not.
        :param other: object to compare
        :return: boolean
        """
        if not isinstance(other, New):
            return False
        return self.url == other.url

    def __hash__(self):
        """
        Returns the hash of the object.
        :return: hash of the object
        """
        return int(hashlib.sha256(self.url.encode('utf-8')).hexdigest(), 16) % 10 ** 8

    def __str__(self):
        """
        Returns a string with the attributes of the object.
        :return: string with the attributes of the object
        """
        return ("Title: " + self.title +
                "\nSummary: " + self.summary +
                "\nCategory: " + self.category +
                "\nUrl: " + self.url +
                "\nImage url: " + self.image_url +
                "\nDate: " + self.date)

    def to_json(self):
        """
        Returns a json with the attributes of the object.
        :return:
        """

        return {
            "ID": self.id,
            "Title": self.title,
            "Summary": self.summary,
            "Category": self.category,
            "Url": self.url,
            "Image_url": self.image_url,
            "Date": self.date
        }
