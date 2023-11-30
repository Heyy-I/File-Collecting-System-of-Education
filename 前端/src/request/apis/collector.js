import { get, post,download } from '../http'
import { urls } from '../../configs'
// import router from '../../router'
// import message from '../message'

const get_class_list = () => {
    return get(urls.collector.get_class_list)
}

const get_collections_by_class_id = (class_id) => {
    return post(urls.collector.get_collections_by_class_id,{'class_id':class_id})
}


const new_collection = (form) => {
    return post(urls.collector.new_collection,form)
}
const delete_collection = (collection_id) => {
    return post(urls.collector.delete_collection,{'collection_id':collection_id})
}
const update_collection = (collection_id, field, data) => {
    return post(urls.collector.update_collection, {'collection_id':collection_id,'field':field,'data':data})
}

const download_collection_zip = (collection_id) => {
    return download(urls.collector.download_collection_zip,{'collection_id':collection_id})
}
const send_remind_email = (collection_id) => {
    return post(urls.collector.send_remind_email,{'collection_id':collection_id})
}
const email_collection_zip = (collection_id) => {
    return post(urls.collector.email_collection_zip,{'collection_id':collection_id})
}

export default {
    get_class_list,
    get_collections_by_class_id,
    new_collection,
    delete_collection,
    update_collection,
    download_collection_zip,
    send_remind_email,
    email_collection_zip
}