import requests
from urllib.parse import urlencode
from pprint import pprint
import json
import time

def intersect(a, b):
    return list(set(a) & set(b))


class VKBase:
    SERVICE_TOKEN = ''
    USER_TOKEN = ''

    TIMEOUT = 2

    APP_ID = 6649468  # my
    # APP_ID = 6642949
    VK_AUTH_URL = 'https://oauth.vk.com/authorize'
    VK_API_URL = 'https://api.vk.com/method/'
    VK_URL = 'https://vk.com/'
    VK_API_VERSION = '5.80'

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def get_auth_url():
        auth_data = {
            'client_id': VKUser.APP_ID,
            'redirect_url': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': 'friends, status',
            'response_type': 'token',
            'v': VKUser.VK_API_VERSION
        }
        return '?'.join((VKUser.VK_AUTH_URL, urlencode(auth_data)))

    def make_get_request(self, method, data, token=None):
        print('.', end='')
        url = self.VK_API_URL + method
        params = dict(
            access_token=token if token else self.SERVICE_TOKEN,
            v=self.VK_API_VERSION
        )
        if data:
            params = {**params, **data}
        try:
            response = requests.get(url, params=params)
            error = response.json().get('error')
            if error and error.get('error_code') == 6:
                # Too many requests per second
                print('Handle "Too many requests per second", wait {} seconds and retry'.format(self.TIMEOUT))
                time.sleep(self.TIMEOUT)
                response = requests.get(url, params=params)
        except requests.ReadTimeout:
            print('Handle ReadTimeout, wait {} seconds and retry'.format(self.TIMEOUT))
            time.sleep(self.TIMEOUT)
            response = requests.get(url, params=params)
        return response


class VKGroup(VKBase):
    id = None
    name = None

    @staticmethod
    def json2group(json):
        group = VKGroup()
        group.__dict__.update(json)
        return group


class VKUser(VKBase):
    user_id = None
    first_name = None
    last_name = None
    nickname = None
    site = None

    def __init__(self, user_id):
        self.user_id = user_id

    def __hash__(self):
        return hash(self.user_id)

    def __repr__(self):
        return '{} {} {}'.format(self.user_id, self.first_name, self.last_name)

    def __str__(self):
        return '{}id{}'.format(self.VK_URL, self.user_id)

    def description(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __lt__(self, other):
        return self.user_id < other.user_id

    def ___le__(self, other):
        return self.user_id <= other.user_id

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __ne__(self, other):
        return self.user_id != other.user_id

    def __gt__(self, other):
        return self.user_id > other.user_id

    def __ge__(self, other):
        return self.user_id >= other.user_id

    @staticmethod
    def json2user(json):
        user = VKUser(json.get('id'))
        user.first_name = json.get('first_name')
        user.last_name = json.get('last_name')
        user.nickname = json.get('nickname')
        user.site = json.get('site')
        return user

    def get_friends(self, user_id=None):
        # Returns a list of user IDs or detailed information about a user's friends.
        data = dict(
            user_id=user_id if user_id else self.user_id,
            count=1000,
            fields=['nickname', 'site'],
            # fields=['nickname', 'domain', 'sex', 'city', 'country'],
        )
        response = self.make_get_request('friends.get', data)
        items = response.json()['response']['items']
        return list(map(VKUser.json2user, items))

    def __and__(self, other):
        friends1 = self.get_friends()
        friends2 = other.get_friends()
        common_friends = intersect(friends1, friends2)
        common_friends.sort()
        return common_friends

    def get_groups(self, user_id=None):
        # Returns a list of user groups.
        data = dict(
            user_id=user_id if user_id else self.user_id,
            count=1000,
            fields=['description', 'status', 'followers_count', 'counters'],
            extended=1
        )
        response = self.make_get_request('groups.get', data)
        items = response.json()['response']['items']
        return list(map(VKGroup.json2group, items))

    def get_group_members_count(self, group_id):
        # Returns a list of user groups.
        data = dict(
            group_id=group_id,
            count=0,
            fields=['common_count', 'counters']
        )
        response = self.make_get_request('groups.getMembers', data)
        return response.json()['response']['count']

    def is_memeber_group(self, group_id, user_ids):
        data = dict(
            group_id=group_id,
            user_ids=str(user_ids),
            extended=1
        )
        response = self.make_get_request('groups.isMember', data)
        #print(response.json())
        items = response.json()['response']
        return list(map(VKGroup.json2group, items))

    def get_groups_memebers(self, group_id):
        data = dict(
            group_id=group_id,
            count=1000
        )
        response = self.make_get_request('groups.getMembers', data)
        #print(response.json())
        items = response.json()['response']
        return items


class VKUsers(VKBase):

    def get(self, user_id):
        # Returns detailed information on users
        data = dict(
            user_ids=user_id,
            fields=['nickname', 'site']
        )
        response = self.make_get_request('users.get', data=data)
        response_data = response.json().get('response')
        if not response_data:
            raise Exception(response.json().get('error'))
        return VKUser.json2user(response_data[0])

    def are_friends(self, user_ids):
        # Checks the current user's friendship status with other specified users.
        response = self.make_get_request('friends.areFriends', dict(user_ids=user_ids), token=self.USER_TOKEN)
        return bool(response.json()['response'][0]['friend_status'])

    def get_friends_mutual(self, user1, user2):
        # Returns a list of user IDs of the mutual friends of two users.
        data = dict(
            source_uid=user1,
            target_uid=user2
        )
        response = self.make_get_request('friends.getMutual', data, token=self.USER_TOKEN)
        return list(map(self.get, response.json()['response']))
