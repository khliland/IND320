import requests

def get_token(config):
  '''
    Get an access token from the API
    Args:
        config (dict): A dictionary containing the client_id, client_secret, and token_url
    Returns:
        dict: A dictionary containing the access_token, token_type, expires_in, scope
  '''

  if not config['client_id']:
    raise ValueError('client_id must be set in credentials.py')

  if not config['client_secret']:
    raise ValueError('client_secret must be set in credentials.py')

  req = requests.post(config['token_url'],
    data={
        'grant_type': 'client_credentials',
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'scope': 'api'
    },
    headers={'content-type': 'application/x-www-form-urlencoded'})

  req.raise_for_status()
  print('Token request successful')
  return req.json()


def get_request(request, token, config):
  '''
    Get a sample request from the API
    Args:
        token (dict): A dictionary containing the access_token, token_type, expires_in, scope
        config (dict): A dictionary containing the api_base_url
    Returns:
        dict: A dictionary containing the sample request
  '''
  url = f"{config['api_base_url']}{request}"
  headers ={
    'authorization': 'Bearer ' + token['access_token'],
    'content-type': 'application/json',
  }

  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.json()
