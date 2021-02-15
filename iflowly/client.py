import requests

class Flow():

	FLOW_GET_URL = 'https://api.iflowly.com/v1/flows/{flow_name}/'

	def __init__(self, api_key, flow_name):
		self.api_key = api_key
		self.get_flow(flow_name)

	def get_flow(self, flow_name):
		kwargs = {
			'headers': {
				'X-Api-Key': self.api_key
			}
		}
		response = requests.request('get', self.FLOW_GET_URL.format(flow_name=flow_name), **kwargs)
		response.raise_for_status()
		self.flow_dict = response.json()

	def run_event(self, event_name):
		URL = 'https://api.iflowly.com/v1/flows/{flow_id}/execute-event/{event_name}/'.format(flow_id=self.flow_dict.get('id'), event_name=event_name)
		kwargs = {
			'headers': {
				'X-Api-Key': self.api_key
			}
		}
		response = requests.request('post', URL, **kwargs)
		response.raise_for_status()
		return response.json()


	def run_trigger(self, trigger_name):
		URL = 'https://api.iflowly.com/v1/flows/{flow_id}/execute-trigger/{trigger_name}/'.format(flow_id=self.flow_dict.get('id'), trigger_name=trigger_name)
		kwargs = {
			'headers': {
				'X-Api-Key': self.api_key
			}
		}
		response = requests.request('post', URL, **kwargs)
		response.raise_for_status()
		return response.json()

	def get_initial_state(self):
		raise NotImplementedError('Not yet implemented')


class IFlowly():

	def __init__(self, api_key):
		self.api_key = api_key

	def get_flow(self, flow_name):
		return Flow(self.api_key, flow_name)
