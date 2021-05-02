from mhyt import yt_download
import string, json, random, os, redis
from youtubesearchpython import SearchVideos
from messages import welcome_message, main_menu
from messages import search_results, download_options

conn = redis.StrictRedis('localhost', decode_responses=True)


class Response:
  def __init__(self, message, message_to):
    self.message = message
    self.message_to = message_to

  def get_response(self):
    if self.message.lower() == 'hi' or self.message.lower() == 'hie':
      message = {'type': 'text', 'text': welcome_message}
    elif self.message.lower() == 'menu':
      message = {'type': 'text', 'text': main_menu}
    elif self.message in self.check_if_download_id():
      conn.hset(self.message_to, 'download', self.message)
      searchresults = conn.hget(self.message_to, 'searchresults')
      title = json.loads(searchresults).get(self.message).get('title')
      message = {'type': 'text', 'text': download_options.format(title)}
    else:
      if self.message == '1':
        message = self.downloadYouTube(self.getdownloadlink(), True)
      elif self.message == '2':
        message = self.downloadYouTube(self.getdownloadlink(), False)
      else:
        message = self.startsearching()
    return message

  def check_if_download_id(self):
    searchresults = conn.hget(self.message_to, 'searchresults')
    return json.loads(searchresults).keys() if searchresults else []

  def getdownloadlink(self):
    download_id = conn.hget(self.message_to, 'download')
    searchresults = conn.hget(self.message_to, 'searchresults')
    return json.loads(searchresults).get(download_id).get('link')

  def startsearching(self):
    searchresults = {}
    message_to_user = 'Here are your search results\n'
    search = SearchVideos(self.message, offset=1, mode='json', max_results=5).result()
    for result in json.loads(search).get('search_result'):
      link = result.get('link')
      download_id = self.id_generator()
      duration = result.get('duration')
      title = result.get('title')[:28] + bool(result.get('title')[28:]) * '...'
      searchresults[download_id] = {'title': title.capitalize(), 'link': link}
      message_to_user += search_results.format(title.capitalize(), duration, download_id)
    conn.hset(self.message_to, 'searchresults', json.dumps(searchresults))
    return {'type': 'text', 'text': f'{message_to_user}\n\nreply with *download id* to download the file'}

  def downloadYouTube(self, media_url, is_audio):
    message = {'type': 'file'}
    filename = self.id_generator(20)
    dirpath = os.path.join(os.getcwd(), 'downloads')
    filepath = os.path.join(dirpath, filename)
    if not os.path.exists(dirpath):
      os.makedirs(dirpath)
    #? ================ download video or audio =============
    if is_audio:
      yt_download(media_url, f'{filepath}.mp3', ismusic=True)
      message['filename'] = f'{filename}.mp3'
      message['fileurl'] = os.path.join('..', 'server', 'downloads', f'{filename}.mp3')
    else:
      yt_download(media_url, f'{filepath}.mp4')
      message['filename'] = f'{filename}.mp4'
      message['fileurl'] = os.path.join('..', 'server', 'downloads', f'{filename}.mp4')
    return message

  def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))