import {MessageBox, Message, Notification} from 'element-ui'

const message = (msg, type) => {
    Message({
        showClose: true,
        message: msg,
        type: type
    });
}

const notify = ({type, title, message, iconClass}) => {
    Notification({type, title, message, iconClass, showClose: false})
}

const success = ({title,message}) => {
    notify({type:'success', title:title, message:message})
}

const info = ({title,message}) => {
    notify({type:'info', title:title, message:message})
}

const error = ({title,message}) => {
    notify({type:'error', title:title, message:message})
}

const warning = ({title,message}) => {
    notify({type:'warning', title:title, message:message})
}



const success_message = (msg) => {
    message(msg, 'success')
}

const info_message = (msg) => {
    message(msg, 'info')
}

const error_message = (msg) => {
    message(msg, 'error')
}

const warning_message = (msg) => {
    message(msg, 'warning')
}

//ElMessageBox
const alert = ({title, msg, okBtnText, func}) => {
    if (!title) {
        title = '提示'
    }
    if (!msg) {
        msg = '错误'
    }
    if (!okBtnText) {
        okBtnText = '确定'
    }
    MessageBox.alert(msg, title, {
        confirmButtonText: okBtnText,
    }).then(func ? func : () => {})
}

const confirm = ({title, msg, func, cFunc}) => {
    MessageBox.confirm(msg, title ? title:'提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
    }).then(func ? func : () => {}).catch(cFunc ? cFunc : () => {})
}

export default {
    notify,
    success,
    info,
    error,
    warning,
    success_message,
    info_message,
    error_message,
    warning_message,
    alert,
    confirm,
}