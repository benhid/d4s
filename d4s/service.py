from abc import ABC, abstractmethod
from urllib.parse import urlencode

import requests

from d4s.context import context
from d4s.storage import Item


class Service(ABC):
    """
    Class representing D4Science services.
    """

    def __init__(self, vre_url):
        self.vre_url = vre_url

    @property
    @abstractmethod
    def url(self):
        pass

    @property
    def token(self):
        return context.token


class DataMiner(Service):
    """
    Interface to interact with gCube DataMiner service.
    """

    def __init__(self):
        super().__init__(vre_url='http://dataminer-prototypes.d4science.org/wps')

    def run(self, params):
        """ Execute the service.
        """
        data = {
            'Version': '1.0.0',
            'request': 'Execute',
            'service': 'WPS',
            'lang': 'en-US'
        }
        data.update(**params)
        x = requests.get(self.url, params=urlencode(data))

        return x.text

    @property
    def url(self):
        return f'{self.vre_url}/WebProcessingService?gcube-token={self.token}'


class DataMinerKmeans(DataMiner):

    def run(self, item: Item, **kwargs):
        k = kwargs.get('k', 3)
        feature = kwargs.get('feature', 'variety')
        maxruns = kwargs.get('max_runs', 10)
        maxsteps = kwargs.get('max_optimization_steps', 5)
        minpoints = kwargs.get('min_points', 2)

        params = {
            'Identifier': 'org.gcube.dataanalysis.wps.statisticalmanager.synchserver.mappedclasses.clusterers.KMEANS',
            'DataInputs': f'OccurrencePointsTable={item.public_url};'
                          f'OccurrencePointsClusterLabel=Classification;'
                          f'FeaturesColumnNames={feature};k={k};max_runs={maxruns};max_optimization_steps={maxsteps};min_points={minpoints}'
        }

        return super().run(params=params)
