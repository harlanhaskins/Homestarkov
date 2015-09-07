from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from pymarkovchain import MarkovChain
from pylru import lrudecorator

class MarkovCache(object):
    @classmethod
    @lrudecorator(100)
    def get(cls, path):
        query = Homestarkov.objects.filter(path=path)
        if not query.exists():
            return None
        character = query.get()
        _generator = MarkovChain("./markovgeneratorfiles/markov-%s" % path)
        _generator.generateDatabase(character.corpus)
        return _generator

class Homestarkov(models.Model):
    path = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    corpus = models.TextField()
    submitter = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    def new_string(self):
        return MarkovCache.get(self.path).generateString()

    def deactivate(self):
        self.active = False
        self.save()

    def json_object(self):
        return {
            "name": self.name,
            "path": self.path,
            "tagline": self.tagline
        }