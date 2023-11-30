// import { get, post } from './http'
// import { urls } from '../configs'
// import router from '../router'

import auth from './apis/auth'
import collector from './apis/collector'
import student from './apis/student'
import teacher from './apis/teacher'
import admin from './apis/admin'

export default {
    auth,
    collector,
    student,
    teacher,
    admin
}