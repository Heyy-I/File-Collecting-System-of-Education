<template>
<div>
    <el-form ref="form" :rules="$formRules" :model="form" status-icon label-width="100px" size="mini">
        <el-form-item label="账号" prop="id">
            <el-input type="text" v-model="form.id" placeholder="可通过学号、工号或邮箱进行登录"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
            <el-input type="password"  v-model="form.password" show-password></el-input>
        </el-form-item>

        <el-form-item label="验证码" prop="captcha">
            <el-col :span="10">
                <el-input  v-model="form.captcha"></el-input>
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

        <el-form-item prop="remember_me">
            <el-checkbox style="margin-left: 0px;" v-model="form.remember_me">下次自动登录</el-checkbox>
        </el-form-item>
        <el-form-item  style="margin-left:38px" size="large">
            <el-button type="primary" @click="login">登录</el-button>
            <el-button @click="resetForm">重置</el-button>
        </el-form-item>
    </el-form>
</div>
</template>

<script>

export default {
data() {
    return {
        form: {
            captcha : '',
            remember_me : true
        },
        captcha_url:'',
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
},
mounted() {
    this.captcha_url = this.$urls.api_url+this.$urls.auth.captcha_url + Math.random()
    this.$api.auth.auto_login()
},
methods: {
    login(){
        this.$refs.form.validate()//表单校验
        .then(() => {
            this.$api.auth.login(this.form)
        })
        .catch(() => {
            this.$notify.error({
                title: '验证出错',
                message: '请检查您填写的信息是否符合格式'
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
    }
},
}
</script>

<style lang="scss" scoped>
</style>