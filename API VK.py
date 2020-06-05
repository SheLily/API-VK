import json
import requests
from urllib.parse import urlencode

class User(object):

    def __init__(self, token, domain, owner_id: int):
        self.token = token
        self.domain = domain
        self.owner_id = int(owner_id)

    def get_params(self):
        return {'access_token': self.token, 'v': 5.89,}

    def get_friends(self, count = 5000): # Выводит все друзей пользователя по его ID
        params = self.get_params()
        params['user_id'] = self.owner_id
        params['count'] = count # кол-во друзей в выводе (умолч. - 5000)
        params['fields'] = 'domain'
        URL = 'https://api.vk.com/method/friends.get'
        response = requests.get(URL, params)
        friends_list = []
        for item in response.json()['response']['items']:
            friends_list.append(item)
        return friends_list

    def __and__(self, other_user):
        res = []
        self_friends = self.get_friends()
        other_friends = other_user.get_friends()
        for friend in self_friends:
            for oth in other_friends:
                if friend['id'] == oth['id']:
                    new_user = User(self.token, friend['domain'], friend['id'])
                    res.append(new_user)
        return res

    def __str__(self):
        return ('vk.com/' + self.domain)

if __name__ == "__main__":
    a_token = ''

    user1 = User(a_token, 'id89811485', 89811485)
    user2 = User(a_token, 'dry_ice', 2694475)

    mutual_friends = user1 & user2
    for _user in mutual_friends:
        print(_user)