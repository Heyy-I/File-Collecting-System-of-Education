import { get, post } from '../http'
// import { urls } from '../../configs'
// import router from '../../router'
import message from '../message'
import { urls } from '../../configs'

const get_collection_list = () => {
    return get(urls.student.get_collection_list)
}
const get_collection_items = (collection_id) => {
    return post(urls.student.get_collection_items,{'collection_id':collection_id})
}
const collection_upload = (item, success_recall) => (params) => {
    message.success({ title: "上传", message: "上传文件大小要求小于100M" })
    const file = params.file
    var flag=false
    if (item.type != '0[*]') {
        if (item.type.match(/0\[(.+)\]/)[1].indexOf(file.name.match(/.+\.(.+)/)[1]) == -1) {//文件格式不在允许范围内
            message.error({ title:"上传文件错误", message:"只能上传允许的文件格式!" });
            flag=true
        }
    }
    if (file.size / 1024 / 1024 > 100) {//100M文件大小限制
        message.error({ title: "上传文件错误", message: "上传文件大小要求小于100M" });
        flag=true
    }
    return post(urls.student.collection_upload, { "file": file, "item": JSON.stringify(item) }, flag?null:{ headers: { "enctype": "multipart/form-data" } })
        .then(success_recall)
}
const roll_back = (collection_id,index) => {
    return post(urls.student.roll_back,{'collection_id':collection_id,'index':index})
}

const get_class_list = () => {
    return get(urls.student.get_class_list)
}

const student_join_class = (class_id) => {
    return post(urls.student.student_join_class,{'class_id':class_id})
}
const student_quit_class = (class_id) => {
    return post(urls.student.student_quit_class,{'class_id':class_id})
}
    
export default {
    get_collection_list,
    get_collection_items,
    collection_upload,
    roll_back,
    get_class_list,
    student_join_class,
    student_quit_class,
}