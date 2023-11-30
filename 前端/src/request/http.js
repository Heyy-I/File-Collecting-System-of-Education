/**axios封装
 * 请求拦截、相应拦截、错误统一处理
 */
import axios from 'axios';
import CryptoJS from 'crypto-js'
import router from '../router/index.js'
import message from './message'
import {api_url} from '../configs'
// 请求超时时间
axios.defaults.timeout = 10000;
//允许跨域携带cookie
axios.defaults.withCredentials = true
// post请求头
axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';
// 地址配置
axios.defaults.baseURL = api_url
// 请求拦截器
axios.interceptors.request.use(
    request => {
        // 每次发送请求之前判断是否存在token，如果存在，则统一在http请求的header都加上token，不用每次请求都手动添加了
        // 即使本地存在token，也有可能token是过期的，所以在响应拦截器中要对返回状态进行判断
        const token = localStorage.getItem('token');
        if (token) {
            request.headers.Authorization = token
            if (request.method == 'post') {
                if (request.headers.enctype) {
                    const form = new FormData();
                    for (var key in request.data) {
                        form.append(key, request.data[key]);
                    }
                    request.data=form
                }
                else {
                    const key = CryptoJS.enc.Hex.parse(localStorage.getItem('AES-key').slice(17)+localStorage.getItem('AES-key').slice(0,17));
                    const iv = CryptoJS.enc.Hex.parse(localStorage.getItem('AES-iv').slice(17)+localStorage.getItem('AES-iv').slice(0,17));
                    let srcs = CryptoJS.enc.Utf8.parse(JSON.stringify(request.data));
                    let encrypted = CryptoJS.AES.encrypt(srcs, key, { iv: iv });
                    request.data = encrypted.ciphertext.toString();
                }
            }
            
        }
        return request;
    },
    error => {
        return Promise.error(error);
    })
function convert_word_array_to_uint8Array(wordArray) {
    var len = wordArray.words.length,
        u8_array = new Uint8Array(len << 2),
        offset = 0, word, i
    ;
    for (i=0; i<len; i++) {
        word = wordArray.words[i];
        u8_array[offset++] = word >> 24;
        u8_array[offset++] = (word >> 16) & 0xff;
        u8_array[offset++] = (word >> 8) & 0xff;
        u8_array[offset++] = word & 0xff;
    }
    return u8_array;
}
// 响应拦截器
axios.interceptors.response.use(
    response => {
        if (response.status === 200) {
            if (response.headers['encryption-algorithm'] == 'AES') {
                const key = CryptoJS.enc.Hex.parse(localStorage.getItem('AES-key').slice(17)+localStorage.getItem('AES-key').slice(0,17));
                const iv = CryptoJS.enc.Hex.parse(localStorage.getItem('AES-iv').slice(17)+localStorage.getItem('AES-iv').slice(0,17));
                if (key != null && iv != null) {
                    let encryptedHexStr = CryptoJS.enc.Hex.parse(response.data);
                    let srcs = CryptoJS.enc.Base64.stringify(encryptedHexStr);
                    let decrypted = CryptoJS.AES.decrypt(srcs, key, { iv: iv });
                    if (response.headers['content-disposition']) {
                        response.data = new Blob([convert_word_array_to_uint8Array(decrypted)],{type:response.headers['content-type']})
                        response.data.file_name = decodeURI(escape(response.headers["content-disposition"].split("filename=")[1]))
                    }
                    else {
                        response.data = JSON.parse(decrypted.toString(CryptoJS.enc.Utf8));
                    }
                }
            }
            return Promise.resolve(response);
        } else {
            return Promise.reject(response);
        }
    },
    // 服务器状态码不是200的情况
    error => {
        if (error.response.status) {
            switch (error.response.status) {
                // 201: 验证码校验失败
                // 无需操作
                case 201:
                    break;
                // 401: 鉴权出错
                // 未登录则跳转登录页面，并携带当前页面的路径
                case 401:
                    message.error({title:"授权无效，请重新登录",message:""})
                    localStorage.removeItem('token')
                    localStorage.removeItem('AES-key')
                    localStorage.removeItem('AES-iv')
                    router.replace({
                        path: '/',
                    });
                    break;
                // 403 token过期
                // 登录过期对用户进行提示
                // 清除本地token
                // 跳转到登录页面
                case 403:
                    message.error({title:"未被授权访问此页面，请重新登录",message:""})
                    localStorage.removeItem('token')
                    localStorage.removeItem('AES-key')
                    localStorage.removeItem('AES-iv')
                    router.replace('/')
                    break;
                // 404请求内容不存在
                case 404:
                    message.error({title:'404',message:'网络请求不存在'})
                    break;
                // 其他错误，直接抛出错误提示
                default:
                    message.error(error.response.data.message);
            }
            return Promise.reject(error.response);
        }
    }
);
/**
 * get方法，对应get请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
export function get(url, params){
    return new Promise((resolve, reject) =>{
        axios.get(url, {
            params: params
        })
        .then(res => {
            resolve(res.data);
        })
        .catch(err => {
            reject(err.data)
        })
    });
}
/**
 * post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 */
export function post(url, params,config=null) {
    return new Promise((resolve, reject) => {
        // if (typeof params == 'object') {
        //     const form = new FormData();
        //     for (var key in params) {
        //         form.append(key, params[key]);
        //     }
        //     params=form
        // }
        axios.post(url, params, config)
        .then(res => {
            resolve(res.data);
        })
        .catch(err => {
            reject(err.data)
        })
    });
}

export function download(url, params) {
    return post(url, params)
    // new Promise((resolve, reject) => {
    //     // if(typeof params == 'object'){
    //     //     const form = new FormData();
    //     //     for (var key in params) {
    //     //         form.append(key, params[key]);
    //     //     }
    //     //     params=form
    //     // }
        
    //     axios.post(url, params, { responseType: 'blob' })
    //     .then(res => {
    //         resolve(res);
    //     })
    //     .catch(err => {
    //         reject(err.data)
    //     })
    // });
}
