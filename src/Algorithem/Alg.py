__author__ = 'dor'
from signups.models import Incentive

class IncentiveAlgorithm(object):

    def getAllIncentiveRagted (self,request):
        """
        return all the Incentives IDs in order by the top to the lowest
        :param request:GET
        :return:list of incentives IDs
        """
        raise NotImplementedError("Should have implemented this")

    def getIncentiveForUser (self,request,userID):
        """
        Give the best Incentive for a specific user
        :param request: GET
        :param userID: a userID for the data Set
        :return: Incentive ID
        """
        raise NotImplementedError("Should have implemented this")

    def getTheBestIncentive(self,request):
        """
        The Best Incentive for all the data set.
        what was the best of all.
        :param request: GET
        :return:Incentive ID
        """
        raise NotImplementedError("Should have implemented this")

    def start(self, request, *args, **kwargs):
        """
        start the algorithm with giving incentives and Data Set
        :param request:POST
        :param args:
        :param kwargs:
        :return: Success if everything is working and Error if not
        """
        raise NotImplementedError("Should have implemented this")

    def clear(self,request, *args, **kwargs):
        """
        clear all the information about this data set
        :return: Suceess
        """
        raise NotImplementedError("Should have implemented this")

def getIncentiveID(self, owner):
    incentives=Incentive.objects.filter(owner=owner)
    idList=[]
    for incentive in incentives:
        idList.append(incentive.schemeID)
    return idList