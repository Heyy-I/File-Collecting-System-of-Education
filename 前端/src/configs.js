const server_url = "http://192.168.31.95:5432/"
// const server_url = "http://192.168.3.36:5432/"
const api_url = server_url + "api/"
const urls = {
    api_url: api_url,
    //公用模块
    auth: {
        captcha_url:         "captcha/",               //获取图形验证码
        verification_url:    "verification",           //后端校验验证码
        login_url:           "login",                  //登录表单提交
        regist_url:          "regist",                 //注册表单提交
        auto_login:          "auto_login",             //自动登录
        academy_list_url:    "academy_list/",          //获取学院列表
        get_token_payload:   "get_token_payload/",     //获取token内包含的信息
        get_cover:           "get_cover/",             //通过class_id获取班级封面
        
        //myspace
        get_my_info:        "get_my_info",              //获取登录用户的信息
        change_name:        "change_name",              //修改姓名
        change_password:    "change_password",          //修改密码
        change_email:       "change_email",             //修改邮箱
    },
    //学生模块
    student: {
        get_collection_list: "get_collection_list",     //获取学生所在班级的收集任务
        get_collection_items: "get_collection_items",   //通过收集id获取收集任务的各项
        collection_upload:   "collection_upload",       //提交作业
        roll_back:           "roll_back",               //撤回提交
        get_class_list:      "student_get_class_list",  //获取该学生所在的所有班级的信息
        student_join_class:  "student_join_class",      //加入班级
        student_quit_class:  "student_quit_class",      //退出班级
    },
    //收集者模块
    collector: {
        get_class_list:     "get_class_list_collector", //获取该教师的所有班级的信息
        get_collections_by_class_id: "get_collections_by_class_id",  //根据班级id获取此班级的所有收集任务

        new_collection:     "new_collection",           //新建收集任务
        delete_collection:  "delete_collection",        //删除收集任务
        update_collection:  "update_collection",        //更新字段
        download_collection_zip: "download_collection_zip",     //下载收集文件
        email_collection_zip:"email_collection_zip",    //收集文件发到邮箱
        send_remind_email:  "send_remind_email",        //发送提醒交作业的邮件
    },
    //教师模块
    teacher: {
        get_class_info:     "get_class_info/",          //通过class_id获取班级信息
        get_class_list:     "teacher_get_class_list",   //获取该教师的所有班级的信息
        cover_upload:       "cover_upload",             //上传班级封面
        update_class:       "update_class",             //更新班级数据
        student_adjust:     "student_adjust",           //调整班级拥有的学生
        delete_class:       "delete_class",             //删除班级
        create_class:       "create_class",             //新增班级
    },
    //管理员模块
    admin: {
        admin_get_user_list: "admin_get_user_list",     //获取所管理的用户的列表
        reset_user_password: "reset_user_password",     //重置用户密码,返回新的密码
        get_unactivated_user:"get_unactivated_user",    //获取该管理员所管理的待激活账号
        activate_permission_user: "activate_permission_user",//根据activate_code修改activate_permission并激活用户
        delete_user:         "delete_user",             //删除用户
    },
}

const menu_dict= {
    items:[
        // { index: 'messages', name: '消息', i_class: 'el-icon-message-solid' },
        { index: 'myspace', name: '个人空间', i_class: 'el-icon-turn-off' },
    ],
    menus: [
    {
        index: 'student', name: '学生', i_class: 'el-icon-user-solid', permission_code:0b1,
            items: [
            { index: 'Student_classes', name: '我的班级', i_class: 'el-icon-s-home' },
            { index: 'Student_collections', name: '作业空间', i_class: 'el-icon-upload' },
        ],
        submenus: null,
    },
    {
        index: 'collector', name: '收集者', i_class: 'el-icon-folder-opened', permission_code:0b10,
        items: [
            { index: 'Collector_classes', name: '收集空间', i_class: 'el-icon-folder-opened' },
        ],
        submenus: null,
    },
    {
        index: 'teacher', name: '教师', i_class: 'el-icon-s-custom', permission_code:0b100,
        items: [
            { index: 'Teacher_myclass', name: '我的班级', i_class: 'el-icon-s-grid' },
        ],
        submenus: null,
    },
    {
        index: 'admin', name: '管理员', i_class: 'el-icon-s-management', permission_code:0b1000,
        items: [
            
        ],
        submenus: [
            {
                index: 'user_manage', name: '用户管理', i_class: 'el-icon-s-management', items: [
                    { index: 'Admin_user_manage', name: '用户管理', i_class: 'el-icon-user-solid' },
                    { index: 'Admin_activate_teacher', name: '激活教师账号', i_class: 'el-icon-s-custom' }
                ]
            },
        ],
    },
]
}

const formRules={
    id: [
        {required: true, message: "请输入账户"},
        {pattern:/^[a-zA-Z0-9_]+$/,message: '账户只能由数字，小写字母与大写字母组成'}
    ],
    password: [
        {required: true,message: "请输入密码"},
        {min: 6, max: 32, message: '密码长度要在 6 到 32 个字符之间' },
        {pattern:/^.*(?=.{6,32})(?=.*\d)(?=.*[A-Za-z])(?=.*[#?!@$%^&*-_.]).*$/,message: '密码强度不足, 应包含英文字母,数字和一个特殊符号'},
    ],
    old_password: [
        {required: true,message: "请输入密码"},
        {min: 6, max: 32, message: '密码长度要在 6 到 32 个字符之间' },
        {pattern:/^.*(?=.{6,32})(?=.*\d)(?=.*[A-Za-z])(?=.*[#?!@$%^&*-_.]).*$/,message: '密码强度不足, 应包含英文字母,数字和一个特殊符号'},
    ],
    new_password: [
        {required: true,message: "请输入密码"},
        {min: 6, max: 32, message: '密码长度要在 6 到 32 个字符之间' },
        {pattern:/^.*(?=.{6,32})(?=.*\d)(?=.*[A-Za-z])(?=.*[#?!@$%^&*-_.]).*$/,message: '密码强度不足, 应包含英文字母,数字和一个特殊符号'},
    ],
    name: [
        {required: true, message: "请输入姓名" },
        {pattern:/^[\u4E00-\u9FA5]{2,10}(·[\u4E00-\u9FA5]{2,10}){0,2}$/,message: '请输入正确的中文姓名'},
    ],
    student_id:[
        {required: true,message: "请输入学号"},
        {pattern:/^\d{10}$/,message: '学号由10位数字组成'}
    ],
    teacher_id:[
        {required: true,message: "请输入工号"},
        {pattern:/^\d{8}$/,message: '工号由8位数字组成'}
    ],
    email: [
        {required: true,message: "请输入邮箱地址"},
        {type: 'email', message: "请输入正确的邮箱地址", trigger: ['blur', 'change']}
    ],
    academy:[
        {required: true,message: "请选择学院"}
    ],
    class_name:[
        { required: true, message: "请填写班级名" },
        {min: 2, max: 30, message: '班级名长度在 2 到 30 个字符之间' },
    ],
    collection_name:[
        { required: true, message: "请填写收集名" },
        {min: 2, max: 30, message: '收集名称长度在 2 到 30 个字符之间' },
    ],
    collection_start_time:[
        { required: true, message: "请填写收集开始时间" },
    ],
    collection_end_time:[
        { required: true, message: "请填写收集截止时间" },
    ],

}

export default {
    api_url,
    urls,
    formRules
}

export {
    api_url,
    urls,
    formRules,
    menu_dict
}
