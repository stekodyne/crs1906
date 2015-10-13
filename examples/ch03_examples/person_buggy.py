"""
person.py - Buggy Person class for Chapter 3 examples.
"""


class Person:
    """Buggy class for unit test demo"""

    def __init__(self, first_name, middle_name, last_name):
        print('Person.__init__()')
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = middle_name

    def __eq__(self, other):
        """Called when Person instances are compared with == operator"""
        return isinstance(other, Person) and \
            other.first_name == self.first_name and \
            other.middle_name == self.middle_name and \
            other.last_name == self.last_name

    def __ne__(self, other):
        """Called when Person instances are compared with != operator"""
        return not self.__eq__(other)

    def __str__(self):
        return "{self.first_name} {self.middle_name} {self.last_name}"\
            .format(self=self)
