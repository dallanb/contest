import random
import string
from flask import g
from flask_seeder import Seeder
from src.common import generate_uuid, time_now
from src import services


# All seeders inherit from Seeder
class DefaultSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 10

    @staticmethod
    def run():
        g.user = generate_uuid()
