from django.conf import settings
from django.db import models

# Create your models here.
class Lifetime(models.Model):
    user = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    player = models.PositiveSmallIntegerField()
    fgm = models.PositiveSmallIntegerField(default=0)
    fga = models.PositiveSmallIntegerField(default=0)
    threepm = models.PositiveSmallIntegerField(default=0)
    threepa = models.PositiveSmallIntegerField(default=0)
    ftm = models.PositiveSmallIntegerField(default=0)
    fta = models.PositiveSmallIntegerField(default=0)
    oreb = models.PositiveSmallIntegerField(default=0)
    dreb = models.PositiveSmallIntegerField(default=0)
    ast = models.PositiveSmallIntegerField(default=0)
    stl = models.PositiveSmallIntegerField(default=0)
    blk = models.PositiveSmallIntegerField(default=0)
    tov = models.PositiveSmallIntegerField(default=0)
    pf = models.PositiveSmallIntegerField(default=0)
    games = models.PositiveSmallIntegerField(default=1)
    @property
    def fgave(self):
        if self.fga == 0:
            return "0%"
        else:
            fgave = self.fgm / self.fga * 100
            fgave = "%.1f" % fgave
            return fgave + "%"
    @property
    def threepave(self):
        if self.threepa == 0:
            return "0%"
        else:
            threepave = self.threepm / self.threepa * 100
            threepave = "%.1f" % threepave
            return threepave + "%"
    @property
    def ftave(self):
        if self.fta == 0:
            return "0%"
        else:
            ftave = self.ftm / self.fta * 100
            ftave = "%.1f" % ftave
            return ftave + "%"
    @property
    def orebave(self):
        orebave = self.oreb / self.games
        orebave = "%.1f" % orebave
        return orebave
    @property
    def drebave(self):
        drebave = self.dreb / self.games
        drebave = "%.1f" % drebave
        return drebave
    @property
    def rebave(self):
        rebave = (self.oreb + self.dreb) / self.games
        rebave = "%.1f" % rebave
        return rebave
    @property
    def astave(self):
        astave = self.ast / self.games
        astave = "%.1f" % astave
        return astave
    @property
    def stlave(self):
        stlave = self.stl / self.games
        stlave = "%.1f" % stlave
        return stlave
    @property
    def blkave(self):
        blkave = self.blk / self.games
        blkave = "%.1f" % blkave
        return blkave
    @property
    def tovave(self):
        tovave = self.tov / self.games
        tovave = "%.1f" % tovave
        return tovave
    @property
    def pfave(self):
        pfave = self.pf / self.games
        pfave = "%.1f" % pfave
        return pfave
    @property
    def ptsave(self):
        ptsave = (self.fgm * 2 + self.threepm * 3 + self.ftm) / self.games
        ptsave = "%.1f" % ptsave
        return ptsave

    def __str__(self):
        return str(self.user)


class Boxscore(models.Model):
    user = models.CharField(max_length=30)
    team_name = models.CharField(max_length=30)
    opponent = models.CharField(max_length=30)
    player = models.PositiveSmallIntegerField()
    fgm = models.PositiveSmallIntegerField(default=0)
    fga = models.PositiveSmallIntegerField(default=0)
    threepm = models.PositiveSmallIntegerField(default=0)
    threepa = models.PositiveSmallIntegerField(default=0)
    ftm = models.PositiveSmallIntegerField(default=0)
    fta = models.PositiveSmallIntegerField(default=0)
    oreb = models.PositiveSmallIntegerField(default=0)
    dreb = models.PositiveSmallIntegerField(default=0)
    ast = models.PositiveSmallIntegerField(default=0)
    stl = models.PositiveSmallIntegerField(default=0)
    blk = models.PositiveSmallIntegerField(default=0)
    tov = models.PositiveSmallIntegerField(default=0)
    pf = models.PositiveSmallIntegerField(default=0)

    @property
    def fgave(self):
        if self.fga == 0:
            return "0%"
        else:
            fgave = self.fgm / self.fga * 100
            fgave = "%.1f" % fgave
            return fgave + "%"

    @property
    def threepave(self):
        if self.threepa == 0:
            return "0%"
        else:
            threepave = self.threepm / self.threepa * 100
            threepave = "%.1f" % threepave
            return threepave + "%"

    @property
    def ftave(self):
        if self.fta == 0:
            return "0%"
        else:
            ftave = self.ftm / self.fta * 100
            ftave = "%.1f" % ftave
            return ftave + "%"

    @property
    def reb(self):
        return self.oreb + self.dreb

    @property
    def pts(self):
        return self.fgm * 2 + self.threepm * 3 + self.ftm

    def submit(self):
        self.save()

    def __str__(self):
        return self.team_name

class Team(models.Model):
    team_cap = models.CharField(max_length=30) # should be the user who create this
    team_name_under_Team = models.CharField(max_length=30) # will be link to boxscore, maybe by primary key

class Game(models.Model):
    user_under_game = models.CharField(max_length=30)
    us = models.CharField(max_length=30)
    opponent = models.CharField(max_length=30)
