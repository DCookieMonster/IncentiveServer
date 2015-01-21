__author__ = 'dor'
from Alg import IncentiveAlgorithm,getIncentiveID
import sched, time
from apscheduler.schedulers.background import BackgroundScheduler


class StupidAlg(IncentiveAlgorithm):
    def __init__(self, request):
        self.s = sched.scheduler(time.time, time.sleep)
        self.owner=request.user
        self.incentvesId = []
        self.usersId = []
        self.sched = BackgroundScheduler()

    def getAllIncentiveRagted(self, request):
        """
        return all the Incentives IDs in order by the top to the lowest
        :param request:GET
        :return:list of incentives IDs
        """
        return self.incentvesId

    @staticmethod
    def getIncentiveForUser(self, request, userID):
        """
        Give the best Incentive for a specific user
        :param request: GET
        :param userID: a userID for the data Set
        :return: Incentive ID
        """
        return self.incentvesId[0]

    def getTheBestIncentive(self,request):
        """
        The Best Incentive for all the data set.
        what was the best of all.
        :param request: GET
        :return:Incentive ID
        """
        return self.incentvesId[0]

    def start(self, request, *args, **kwargs):
        """
        start the algorithm with giving incentives and Data Set
        :param request:POST
        :param args:
        :param kwargs:
        :return: Success if everything is working and Error if not
        """
        IdList = getIncentiveID(self, request.owner)
        self.incentvesId = sorted(IdList)

    def init(self, request):
       # self.sched.add_job(self.start(self,request), 'interval', minutes=2)
        self.sched.add_job(lambda: self.start(self,request), 'interval', id="start", name="start", minutes=60)
        self.start(self, request)
        self.sched = BackgroundScheduler.start(self.sched)

    def clear(self,request, *args, **kwargs):
        """
        clear all the information about this data set
        :return: Suceess
        """
        if request.user == self.owner:
            self.sched.remove_all_jobs()
            self.usersId = []
            self.incentvesId = []