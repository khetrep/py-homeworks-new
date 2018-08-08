"""
Задание:
Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
В качестве жертвы, на ком тестировать, можно использовать: https://vk.com/eshmargunov
"""
from myvk import *
from pprint import pprint

VK_USER = 'eshmargunov'
VK_USER_ID = 171691064

VK_TOKEN = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'

def main(user_id):
    users = VKUsers()
    user = users.get(user_id)

    print('User:', user, user.description())
    friends = user.get_friends()
    print('User friends({}): {}'.format(len(friends), friends))
    groups = user.get_groups()
    print('User groups({}): {}'.format(len(groups), groups))
    #print('User 2:', user2, user2.description())

    groups_dict = { g.id : g for g in groups }

    friends_ids = list(map(lambda x: x.user_id, friends))
    print(friends_ids)
    for group in groups:
        is_member = user.is_memeber_group(group.id, friends_ids)
        for m in is_member:
            if m.member == 1:
                print('user {} is member group {}'.format(m.user_id, group.id))
                del groups_dict[group.id]
                break
        print(is_member)

    #for friend in friends:
    #    friend_groups = friend.get_groups()
    print('Result groups({}): {}'.format(len(groups_dict), groups_dict))

    # print('Результат поиска общих друзей, используя API VK(friends.getMutual):')
    # pprint(users.get_friends_mutual(44625516, 356860670))
    # print('')
    #
    # common_friends = user1 & user2
    # print('Common friends of users {} and {}:'.format(user1.user_id, user2.user_id))
    # pprint(common_friends)


def read_input():
    text = input('Введите логин или идентификатор пользователя VK: ')
    return text


if __name__ == "__main__":
    VKBase.USER_TOKEN = VK_TOKEN
    VKBase.SERVICE_TOKEN = VK_TOKEN
    main(VK_USER_ID)
