"""
Задание:
Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
В качестве жертвы, на ком тестировать, можно использовать: https://vk.com/eshmargunov
"""
import os
import sys
from myvk import *
from pprint import pprint
import json

VK_USER = 'eshmargunov'
VK_USER_ID = 171691064

VK_TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'


def write_to_file(filename, groups):
    with open(filename, 'w') as f:
        json.dump(groups, f, indent=2)
    print('Write groups to file {}'.format(filename))


def main(user_id):
    users = VKUsers()
    user = users.get(user_id)

    print('User:', user, user.description())
    friends = user.get_friends()
    print('User has {} friends'.format(len(friends)))
    groups = user.get_groups()
    print('User has {} groups'.format(len(groups)))

    groups_dict = {g.id: g for g in groups}

    friends_ids = list(map(lambda x: x.user_id, friends))
    for group in groups:
        is_member = user.is_memeber_group(group.id, friends_ids)
        for m in is_member:
            if m.member == 1:
                #print('user {} is member group {}'.format(m.user_id, group.id))
                del groups_dict[group.id]
                break

    groups_for_write = []
    for id,g in groups_dict.items():
        #print(g)
        groups_for_write.append({
            'name': g.name,
            'gid': str(g.id),
            'members_count': user.get_group_members_count(g.id)
        })
    print()
    print('Found target groups: {}'.format(len(groups_dict)))
    pprint(groups_for_write)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, 'groups.json ')
    write_to_file(target_file, groups_for_write)


def read_input():
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


if __name__ == "__main__":
    user_id = read_input()
    VKBase.USER_TOKEN = VK_TOKEN
    VKBase.SERVICE_TOKEN = VK_TOKEN
    main(user_id)