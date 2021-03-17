from iflowly import client
iflowly = client.IFlowly(api_key='HzV6XzhB.Q57JmUqEmGFQAbkugiBkLiX8FbKkHCQs')
flow = iflowly.get_flow('New Flow')
print(flow.states)
