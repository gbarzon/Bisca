import requests
import ast

class requestHandler():
  
  def __init__(self):
    self.URL = ''

  def insertURL(self, myURL):
    self.URL = myURL
    if myURL == 'casa':
      self.URL = 'http://127.0.0.1:5000'
    elif myURL == 'taverna':
      self.URL = 'http://jack96bjo.pythonanywhere.com/server_bisca'

  def sendRequest(self, myDict):
    # sending get request and saving the response as response object
    try:
      r = requests.get(url = self.URL, params = myDict)
      #r = requests.post(url = self.URL, data = myDict)
    except:
      print('Error in sending request')
      return -1

    print('Risposta: ', r.content)
    data = r.content
    print(data)
    data = data.decode("UTF-8")
    print(data)
    data = ast.literal_eval(data)
    print(data)
    print(type(data))
    return(data)
    '''
    try:
      # extracting data in json format
      data = r.content
      data = data.decode("UTF-8")
      data = ast.literal_eval(data)
      return(data)
    except:
      print('Error in opening receive data')
      return -1
    '''
