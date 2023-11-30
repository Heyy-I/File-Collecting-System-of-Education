import { get, post } from '../http'
import { urls } from '../../configs'
// import router from '../../router'
// import message from '../message'

const admin_get_user_list = () => {
    return get(urls.admin.admin_get_user_list)
}

const reset_user_password = (id) => {
    return post(urls.admin.reset_user_password,{'id':id})
}

const get_unactivated_user = () => {
    return get(urls.admin.get_unactivated_user)
}

const activate_permission_user = (activate_code) => {
    return post(urls.admin.activate_permission_user,{'activate_code':activate_code})
}

const delete_user = (id) => {
    return post(urls.admin.delete_user,{'id':id})
}

export default {
    admin_get_user_list,
    reset_user_password,
    get_unactivated_user,
    activate_permission_user,
    delete_user
}