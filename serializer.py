from editor import *
import pickle, sys, time


class Serializer(object):
    MAPS_INFO = [{"OBS_PARAMS" : DEFAULT_MAP.getObsParams(), "GOALS_PARAMS" : DEFAULT_MAP.getGoalsParams()}]
    BRAINS_INFO = []
    PARAMS_INFO = []

    SAVES = None

    MAPS = []

    @classmethod
    def addMapsInfo(cls, _map):
        cls.MAPS_INFO.append({"OBS_PARAMS" : _map.getObsParams(), "GOALS_PARAMS" : _map.getGoalsParams()})
        cls.makeMaps()


    @classmethod
    def dump(cls, first = False):
        if not first:
            for i in xrange(len(cls.MAPS)):
                cls.MAPS_INFO[i] = {"OBS_PARAMS" : cls.MAPS[i].getObsParams(), "GOALS_PARAMS" : cls.MAPS[i].getGoalsParams()}

            cls.SAVES = {"MAPS_INFO" : cls.MAPS_INFO, "BRAINS_INFO" : cls.BRAINS_INFO, "PARAMS_INFO" : cls.PARAMS_INFO}

        with open("saves.picle", "wb") as file:
            pickle.dump(cls.SAVES, file)


    @classmethod
    def load(cls):
        try:
            with open("saves.picle", "rb") as file:
                cls.SAVES = pickle.load(file)
                if cls.SAVES:
                    cls.MAPS_INFO = cls.SAVES["MAPS_INFO"]
                    cls.BRAINS_INFO = cls.SAVES["BRAINS_INFO"]
                    cls.PARAMS_INFO = cls.SAVES["PARAMS_INFO"]

        except IOError:
            cls.dump(True)


        if not cls.SAVES:
            cls.SAVES = {"MAPS_INFO" : cls.MAPS_INFO, "BRAINS_INFO" : cls.BRAINS_INFO, "PARAMS_INFO" : cls.PARAMS_INFO}

    @classmethod
    def makeMaps(cls):
        cls.MAPS = []
        for i in xrange(len(cls.MAPS_INFO)):
            new_map = Map([], [])
            new_map.makeObs(cls.SAVES["MAPS_INFO"][i]["OBS_PARAMS"])
            new_map.makeGoals(cls.SAVES["MAPS_INFO"][i]["GOALS_PARAMS"])
            cls.MAPS.append(new_map)

Serializer.load()
Serializer.makeMaps()
