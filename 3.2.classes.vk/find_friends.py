"""
Домашнее задание к лекции 3.2 «Работа с классами на примере API VK»
Вам предстоит решить задачу поиска общих друзей у пользователей VK.

Ссылка на документацию VK/dev.

Задача №1
Пользователя нужно описать с помощью класса и реализовать метод поиска общих друзей, используя API VK.

Задача №2
Поиск общих друзей должен происходить с помощью оператора &, т.е. user1 & user2 должен выдать список общих друзей
пользователей user1 и user2, в этом списке должны быть экземпляры классов.

Задача №3
Вывод print(user) должен выводить ссылку на профиль пользователя в сети VK
"""
import requests
from pprint import pprint
from urllib.parse import urlencode

SERVICE_TOKEN = ''
USER_TOKEN = ''


def intersect(a, b):
    return list(set(a) & set(b))


class VKBase:
    APP_ID = 6649468  # my
    # APP_ID = 6642949
    VK_AUTH_URL = 'https://oauth.vk.com/authorize'
    VK_API_URL = 'https://api.vk.com/method/'
    VK_URL = 'https://vk.com/'
    VK_API_VERSION = '5.80'

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
        url = self.VK_API_URL + method
        params = dict(
            access_token=token if token else SERVICE_TOKEN,
            v=self.VK_API_VERSION
        )
        if data:
            params = {**params, **data}
        return requests.get(url, params=params)


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
        response = self.make_get_request('friends.areFriends', dict(user_ids=user_ids), token=USER_TOKEN)
        return bool(response.json()['response'][0]['friend_status'])

    def get_friends_mutual(self, user1, user2):
        # Returns a list of user IDs of the mutual friends of two users.
        data = dict(
            source_uid=user1,
            target_uid=user2
        )
        response = self.make_get_request('friends.getMutual', data, token=USER_TOKEN)
        return list(map(self.get, response.json()['response']))


def main():
    users = VKUsers()
    user1 = users.get(44625516)
    user2 = users.get(356860670)

    print('User 1:', user1, user1.description())
    print('User 2:', user2, user2.description())
    print('')

    print('Результат поиска общих друзей, используя API VK(friends.getMutual):')
    pprint(users.get_friends_mutual(44625516, 356860670))
    print('')

    common_friends = user1 & user2
    print('Common friends of users {} and {}:'.format(user1.user_id, user2.user_id))
    pprint(common_friends)


if __name__ == "__main__":
    main()
