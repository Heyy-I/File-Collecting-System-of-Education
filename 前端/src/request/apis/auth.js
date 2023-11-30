import { get, post } from '../http'
import { urls } from '../../configs'
import router from '../../router'
import message from '../message'

const get_permission_code = () => get_token_payload('permission_code')

const get_user_name = () => get_token_payload('name')


const get_token_payload = (field) => new Promise((resolve, reject) => {
    get(urls.auth.get_token_payload + field)
        .then(res => resolve(res[field]))
        .catch(err => reject(err))
});

const auto_login = () => {
    if (localStorage.getItem('token')) {
        get(urls.auth.auto_login).then(() => {
            console.log(auto_login)
            router.push('home')
        })
    }
}

const login = form => post(urls.auth.login_url, form)
    .then(response => {
        localStorage.setItem('token', response.token)
        localStorage.setItem('AES-key', response.key)
        localStorage.setItem('AES-iv', response.iv)
        router.push('home')
        message.success(response)
    }).catch(error => message.error(error))

const regist = form => post(urls.auth.regist_url, form)
    .then((response) => {
        router.go(0)
        message.success(response)
    }
    ).catch(error => message.error(error))

const verification = (value, callback, vv) =>
    post(urls.auth.verification_url, { captcha: value })
        .then(
            callback()
        )
        .catch(() => {
            callback(new Error('验证码错误'))
            vv.form.captcha = '';
            vv.$refs.form.clearValidate('captcha')
            vv.captcha_url = urls.api_url+urls.auth.captcha_url+Math.random();
        });

const get_academy_list = (identity) => get(urls.auth.academy_list_url + identity)



//****************  myspace  **************/
const get_my_info = () => get(urls.auth.get_my_info)

const change_name = (name) => {
    return post(urls.auth.change_name,{'name':name})
}
const change_password = (form) => {
    return post(urls.auth.change_password,form)
}
const change_email = (email) => {
    return post(urls.auth.change_email,{'email':email})
}
export default {
    get_permission_code,
    get_user_name,
    auto_login,
    login,
    regist,
    verification,
    get_academy_list,

    get_my_info,
    change_name,
    change_password,
    change_email
}