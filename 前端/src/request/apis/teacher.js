import { get,post } from '../http'
import { urls } from '../../configs'
// import router from '../../router'
import message from '../message'

const get_class_info=(class_id) => {
    return get(urls.teacher.get_class_info+class_id)
}

const get_class_list = () => {
    return get(urls.teacher.get_class_list)
}

const cover_upload = (class_id) =>
    (params) => {
    const file = params.file,
    fileType = file.type,
    isImage = fileType.indexOf("image") != -1,
    isLt4M = file.size / 1024 / 1024 < 4;//4M文件大小限制
    if (!isImage) {
        message.error({ title:"上传封面错误", message:"只能上传图片格式png、jpg、gif" });
        return;
    }
    if (!isLt4M) {
        message.error({ title: "上传封面错误", message: "上传图片大小要求小于4M" });
        return;
    }
    return post(urls.teacher.cover_upload, {"file": file, "class_id": class_id}, { headers: {"enctype": "multipart/form-data"}})
}

const update_class = (class_id, field, data) => {
    return post(urls.teacher.update_class, {'field':field,'class_id':class_id,[field]:data})
}

const student_adjust = (class_id, student_id_list, flag) => {
    return post(urls.teacher.student_adjust,
        { 'class_id': class_id, 'student_id_list': student_id_list, 'flag': flag }
    ).then(() => {
            message.success({ title: '调整成功', message: '调整班级成员成功!' })
    })
}

const delete_class = (class_id) => {
    return post(urls.teacher.delete_class, {'class_id':class_id})
}

const create_class = (class_name) => {
    return post(urls.teacher.create_class, {'class_name':class_name})
}

export default {
    get_class_info,
    get_class_list,
    cover_upload,
    update_class,
    student_adjust,
    delete_class,
    create_class
}