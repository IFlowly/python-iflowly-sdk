import requests
from .utils import RequestConstructor
from .exceptions import TriggerError
from .constants import BASE_API_URL, LATEST_API_VERSION

class IFlowly():

    def __init__(self, api_key):
        self.requester = RequestConstructor(api_key)

    def get_flow(self, flow_name, version='latest'):
        return Flow(flow_name, self.requester, version)


class State():
    pass


class States():

    def transform_url(self):
        return self.flow.requester.transform_url('flows', self.flow.id) + 'advanced/options/' + self.flow.version.id + '/'

    def __init__(self, flow, _type='FlowVersion'):
        self.flow = flow
        self._type = _type
        self.__states = self.__get_states()

    def __set_attrs_from_response(self, response):
        print(response)

    def __get_states(self):
        url = self.transform_url()
        params = {
            'type': 'FlowVersion'
        }
        response = self.flow.requester.request('get', url, params=params)
        self.__set_attrs_from_response(response)

class Version():

    def transform_url(self):
        return self.flow.requester.transform_url('flows', self.flow.id) + 'versions/'

    def __init__(self, flow, version):
        self.flow = flow
        self.__get_version(version)

    def __set_attrs_from_response(self, response):
        self.id = response.get('id')
        self.locked = response.get('locked')
        self.version = response.get('version')
        self.latest = response.get('latest')

    def __get_version(self, version):
        url = self.transform_url()
        params = {
            'version': version
        }
        response = self.flow.requester.request('get', url, params=params)
        self.__set_attrs_from_response(response)


class Flow():

    def __init__(self, flow_name, requester, version='latest'):
        self.requester = requester
        self.__get_flow(flow_name)
        self.version = Version(self, version)
        self.states = States(self)

    def __set_attrs_from_response(self, response):
        self.id = response.get('id')
        self.name = response.get('name')
        self.deleted = response.get('deleted')
        self.active = response.get('active')

    def __get_flow(self, flow_name):
        url = self.requester.transform_url('flows', flow_name)
        response = self.requester.request('get', url)
        self.__set_attrs_from_response(response)

    def run_event(self, event_name):
        PATH = '{flow_id}/execute-event/{event_name}'.format(flow_id=self.id, event_name=event_name)
        URL = self.requester.transform_url('flows', PATH)
        self.requester.request('post', URL)
        return 'Success'

    def run_trigger(self, trigger_name):
        PATH = '{flow_id}/execute-trigger/{trigger_name}'.format(flow_id=self.id, trigger_name=trigger_name)
        URL = self.requester.transform_url('flows', PATH)
        try:
            self.requester.request('post', URL)
            return 'Success'
        except requests.exceptions.HTTPError as e:
            response_json = e.response.json()
            detail = response_json.get('detail')
            raise TriggerError(detail) from None
