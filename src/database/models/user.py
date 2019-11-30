from django.db import models
from django.contrib.auth.models import User # This is so the built in user is added

# Write down user models here

# Abstract UserType model/class
class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta: # Makes sure it is an abstract user model/class
        abstract = True

# Abstract Staff Class

class Staff(UserType):
    STATUS_CHOICES = [ # No need for status table, this also works
        ('L', 'Laid Off'),
        ('N', 'Not Hired'),
        ('H', 'Hired')
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default="N"
    )

    warnings = models.IntegerField(default=0)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


# Non-Staff user types

class Customer(UserType):
    pass


class Manager(UserType):
    pass # All needed fields are inherited, restaurant references manager


# Staff User Types

class Cook(Staff):
    food_drops = models.IntegerField(default=0)
    
    def update_status(self, newRating):
    #TODO query last 2 order ratings from Orders DB based on self.restaurant, store as rating1, rating2
        avg_rating = (rating1 + rating2 + newRating) / 3

        if (avg_rating < 2):
            #TODO remove food from Food DB
            self.food_drops+=1
            self.warnings = self.food_drops%2

        if (self.warnings > 3):
            self.status = 'L'

class Deliverer(Staff):
    pass # All needed fields are inherited

class Salesperson(Staff):
    # TODO: Add the following
    commission = models.FloatField(default = 100)