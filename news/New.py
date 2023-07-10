"""
New.py is a module that contains the class New.
"""


class New:
    """
    New is a class that contains the attributes of a new.
    """

    def __init__(self, title, url, image_url, summary, category):
        """
        Constructor of the class New.
        :param title: title of the new
        :param url: url of the new
        :param image_url: image url of the new
        :param summary: summary of the new
        :param category: category of the new
        """
        self.title = title
        self.url = url
        self.image_url = image_url
        self.summary = summary
        self.category = category
        self.id = self.__hash__()  # id is the hash of the object

    def __hash__(self):
        """
        Returns the hash of the object.
        :return: hash of the object
        """
        return hash(self.title + self.url + self.image_url + self.summary + self.category)

    def __eq__(self, other):
        """
        Returns True if the objects are equal, False otherwise.
        :param other: object to compare
        :return: True if the objects are equal, False otherwise
        """
        if isinstance(other, New):
            return (self.title == other.title and
                    self.url == other.url)

    def __str__(self):
        """
        Returns a string with the attributes of the object.
        :return: string with the attributes of the object
        """
        return ("Title: " + self.title +
                "\nSummary: " + self.summary +
                "\nCategory: " + self.category +
                "\nUrl: " + self.url +
                "\nImage url: " + self.image_url)

