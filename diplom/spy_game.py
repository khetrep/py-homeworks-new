"""
Задание:
Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
В качестве жертвы, на ком тестировать, можно использовать: https://vk.com/eshmargunov
"""
import json
import os
import sys
from pprint import pprint
from myvk import VKBase, VKException, VKUsers


def write_to_file(filename, groups):
    with open(filename, 'w') as f:
        json.dump(groups, f, indent=2)
    print('Write groups to file {}'.format(filename))


def read_user_id():
    env_var = os.environ.get('VK_USER_ID')
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        print('Use user id from command arguments:', user_id)
        return user_id
    elif env_var:
        user_id = env_var
        print('Use user id from env VK_USER_ID:', user_id)
        return
    else:
        text = input('Введите логин или идентификатор пользователя VK: ')
        return text


def read_secret_token():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    secret_file = os.path.join(current_dir, 'secret.json')
    with open(secret_file, 'r') as f:
        store = json.load(f)
        return store['token']


def main(user_id):
    users = VKUsers()
    try:
        user = users.get(user_id)
    except VKException as e:
        print('Error on get user {}: {}'.format(user_id, e))
        return

    print('User:', user, user.description())
    friends = user.get_friends()
    print('User has {} friends'.format(len(friends)))
    groups = user.get_groups()
    print('User has {} groups'.format(len(groups)))

    groups_dict = {g.id: g for g in groups}

    friends_ids = list(map(lambda x: x.user_id, friends))
    for group in groups:
        is_member = user.is_member_group(group.id, friends_ids)
        for m in is_member:
            if m.get('member') == 1:
                # print('user {} is member group {}'.format(m.user_id, group.id))
                del groups_dict[group.id]
                break

    groups_for_write = []
    for group_id, g in groups_dict.items():
        groups_for_write.append({
            'name': g.name,
            'gid': str(g.id),
            'members_count': g.members_count
        })
    print('\n\nFound target groups: {}'.format(len(groups_dict)))
    pprint(groups_for_write)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, 'groups.json ')
    write_to_file(target_file, groups_for_write)


if __name__ == "__main__":
    VKBase.service_token = read_secret_token()

    main(read_user_id())

    VKBase.debug()
