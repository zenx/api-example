import redis

from settings.base import config


r = redis.StrictRedis(host=config.get('redis', 'host'),
                      port=config.getint('redis', 'port'),
                      db=config.getint('redis', 'db'))
