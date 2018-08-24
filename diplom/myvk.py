import time
import requests

ERROR_CODE_TOO_MANY_REQUESTS = 6
USER_IDS_LIMIT = 500
TRY_REQUEST_LIMIT = 1


class VKException(Exception):

    def __init__(self, json):
        if isinstance(json, dict):
            self.error_code = json.get('error_code')
            self.error_msg = json.get('error_msg')
            self.request_params = json.get('request_params')

    def __repr__(self):
        return '{} {}'.format(self.error_code, self.error_msg)

    def __str__(self):
        return '{} {}'.format(self.error_code, self.error_msg)


class VKBase:
    VK_AUTH_URL = 'https://oauth.vk.com/authorize'
    VK_API_URL = 'https://api.vk.com/method/'
    VK_URL = 'https://vk.com/'
    VK_API_VERSION = '5.80'

    TIMEOUT = 2

    req_counter = 0
    resp_error_counter = 0
    resp_ok_counter = 0

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def debug(cls):
        print('Requests {}, error responses {}, ok responses {}'.format(cls.req_counter, cls.resp_error_counter,
                                                                        cls.resp_ok_counter))

    def _try_get_request(self, url, params, attempt):
        print('.', end='')
        try:
            VKBase.req_counter += 1
            response = requests.get(url, params=params)
            error = response.json().get('error')
            if error:
                VKBase.resp_error_counter += 1
                if error.get('error_code') == ERROR_CODE_TOO_MANY_REQUESTS:
                    if attempt <= 0:
                        raise Exception('Attempt limit {} exceeded for retry requests.'.format(TRY_REQUEST_LIMIT))
                    print('"Too many requests per second", wait {} seconds and retry'.format(self.TIMEOUT))
                    time.sleep(self.TIMEOUT)
                    response = self._try_get_request(url, params, attempt - 1)
                else:
                    raise VKException(error)
            else:
                VKBase.resp_ok_counter += 1
        except requests.ReadTimeout:
            VKBase.resp_error_counter += 1
            if attempt <= 0:
                raise Exception('Attempt limit {} exceeded for retry requests.'.format(TRY_REQUEST_LIMIT))
            print('Handle ReadTimeout, wait {} seconds and retry'.format(self.TIMEOUT))
            time.sleep(self.TIMEOUT)
            response = self._try_get_request(url, params, attempt - 1)
        return response

    def make_get_request(self, method, data, token=None):
        url = self.VK_API_URL + method
        params = dict(
            access_token=token if token else self.service_token,
            v=self.VK_API_VERSION
        )
        if data:
            params = {**params, **data}
        return self._try_get_request(url, params, TRY_REQUEST_LIMIT)


class VKGroup(VKBase):

    def __init__(self, json):
        if isinstance(json, dict):
            self.id = json.get('id')
            self.name = json.get('name')
            self.member = json.get('member')
            self.user_id = json.get('user_id')
            self.members_count = json.get('members_count')


class VKUser(VKBase):

    def __init__(self, json):
        if isinstance(json, dict):
            self.user_id = json.get('id')
            self.first_name = json.get('first_name')
            self.last_name = json.get('last_name')
            self.nickname = json.get('nickname')
            self.site = json.get('site')

    def __hash__(self):
        return hash(self.user_id)

    def __repr__(self):
        return '{} {} {}'.format(self.user_id, self.first_name, self.last_name)

    def __str__(self):
        return '{}id{}'.format(self.VK_URL, self.user_id)

    def description(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_friends(self, user_id=None):
        # Returns a list of user IDs or detailed information about a user's friends.
        data = dict(
            user_id=user_id if user_id else self.user_id,
            count=1000,
            fields=['nickname', 'site'],
        )
        response = self.make_get_request('friends.get', data)
        items = response.json()['response']['items']
        return list(map(VKUser, items))

    def get_groups(self, user_id=None):
        # Returns a list of user groups.
        data = dict(
            user_id=user_id if user_id else self.user_id,
            count=1000,
            fields=['description', 'status', 'followers_count', 'counters', 'members_count'],
            extended=1
        )
        response = self.make_get_request('groups.get', data)
        items = response.json()['response']['items']
        return list(map(VKGroup, items))

    def _is_member_group(self, group_id, user_ids):
        data = dict(
            group_id=group_id,
            user_ids=','.join(map(str, user_ids)),
            extended=1
        )
        response = self.make_get_request('groups.isMember', data)
        return response.json()['response']

    def is_member_group(self, group_id, user_ids):
        if len(user_ids) <= USER_IDS_LIMIT:
            return self._is_member_group(group_id, user_ids)
        else:
            members = []
            for a in [user_ids[i:i + USER_IDS_LIMIT] for i in range(0, len(user_ids), USER_IDS_LIMIT)]:
                members.extend(self._is_member_group(group_id, a))
            return members


class VKUsers(VKBase):

    def get(self, user_id):
        # Returns detailed information on users
        data = dict(
            user_ids=user_id,
            fields=['nickname', 'site']
        )
        response = self.make_get_request('users.get', data=data)
        response_data = response.json().get('response')
        return VKUser(response_data[0])
