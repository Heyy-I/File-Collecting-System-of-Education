<template>
<div>
    <el-form ref="form" :rules="$formRules" :model="form" status-icon label-width="100px" size="mini">

        <el-form-item label="学号" prop="student_id" v-if="form.identity=='student'">
            <el-input type="text" v-model="form.student_id"></el-input>
        </el-form-item>

        <el-form-item label="工号" prop="teacher_id" v-if="form.identity=='teacher'">
            <el-input type="text" v-model="form.teacher_id"></el-input>
        </el-form-item>

        <el-form-item label="姓名" prop="name">
            <el-input type="text"  v-model="form.name"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
            <el-input type="password"  v-model="form.password" show-password @blur="$refs.form.validateField('check_password');"></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="check_password">
            <el-input type="password"  v-model="form.check_password"></el-input>
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
            <el-input type="text" v-model="form.email"></el-input>
        </el-form-item>

        <el-form-item label="学院" prop="academy">
            <el-select v-model="form.academy" placeholder="请选择学院" style="display:block;">
                <el-option
                v-for="academy in academy_list"
                :key="academy.value"
                :label="academy.label"
                :value="academy.value">
                </el-option>
            </el-select>
        </el-form-item>

        <el-form-item label="验证码" prop="captcha">
            <el-col :span="10">
                <el-input v-model="form.captcha"></el-input>
            </el-col>
            <el-col :span="4" :offset="2">
                <el-button type="text" class="el-icon-refresh-right refresh_captcha" @click="refresh_captcha" style="font-size: x-small;padding: 0;vertical-align: top;">
                    <div>看不清<br>换一张</div>
                </el-button>
            </el-col>
            <el-col :span="8">
                <el-image :src="captcha_url" alt="验证码获取错误" @click="refresh_captcha" style="font-size: smaller;"></el-image>
            </el-col>
        </el-form-item>

        <el-form-item prop="identity">
            <el-radio-group  style="margin-left:42px" v-model="form.identity" @input="fetch_academy_list">
                <el-radio label="student">学生</el-radio>
                <el-radio label="teacher">教师</el-radio>
            </el-radio-group>
        </el-form-item>

        <el-form-item style="margin-left:38px" size="large">
            <el-button type="primary" @click="regist()">注册</el-button>
            <el-button @click="resetForm">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>
export default {
data() {
    return {
        form: { identity:'student', captcha:'', password:''},
        captcha_url: '',
        academy_list: [],
    }
},
    created() {
    //添加验证码校验
    this.$formRules.captcha = [
    { required: true, message: "请输入验证码" },
    { pattern: /^[a-zA-Z0-9]{4}$/, message: '验证码格式不正确' },
    {
        validator: (rule, value, callback) => {
            this.$api.auth.verification(value, callback, this)
        }
    }];
    this.$formRules.check_password = [
        { required: true, message: "请再次输入密码" },
        { min: 6, max: 32, message: '长度在 6 到 32 个字符' },
        {
            validator: (rule, value, callback) => {
            if (this.form.password==null || this.form.password==''){
                callback(new Error('首次密码还未填写'))
            }
            else if (this.form.password != this.form.check_password) {
                callback(new Error('两次密码不一致'))
            }
            else {
                callback()
            }
            }
        }];
},
mounted () {
    this.captcha_url = this.$urls.api_url+this.$urls.auth.captcha_url + Math.random();
    this.fetch_academy_list();
},
methods: {
    regist() {
        this.$refs.form.validate()//表单校验
        .then(() => {
            this.$api.auth.regist(this.form)
        })
        .catch(() => {
            this.$notify.warning({
                title: '验证出错',
                message: '您填写的信息并不符合规则'
            });
        })
        this.refresh_captcha();
    },
    resetForm() {
        this.$refs.form.resetFields();
        this.refresh_captcha();
    },
    refresh_captcha() {
        this.form.captcha='';
        this.$refs.form.clearValidate('captcha')
        this.captcha_url = this.$urls.api_url+this.$urls.auth.captcha_url+Math.random();
    },
    fetch_academy_list() {
        this.$api.auth.get_academy_list(this.form.identity)
            .then(resp => { this.academy_list = resp })
    }
},
}
</script>

<style lang="scss" scoped>

</style>