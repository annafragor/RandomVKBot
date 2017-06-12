import vk_api
import settings


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def own_auth():
    vk_session = vk_api.VkApi(settings.login, settings.password, auth_handler=auth_handler)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
    # vk = vk_session.get_api()
    return vk_session


def group_auth():
    vk_group = vk_api.VkApi(token=settings.token)
    vk_group.auth()
    return vk_group
