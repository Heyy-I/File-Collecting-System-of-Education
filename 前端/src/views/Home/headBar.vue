<template>
<el-header id="header">
    <span id="user_name">{{username}}</span>
    <el-button-group>
        <el-button type="primary" plain icon="el-icon-user-solid" @click="$router.push('/myspace')">个人空间</el-button>
        <!-- <el-button type="primary" plain icon="el-icon-message-solid">消息</el-button> -->
        <el-button 
        type="primary" plain 
        icon="el-icon-switch-button"
        @click="logout"
        >退出登录</el-button>
    </el-button-group>
</el-header>
</template>

<script>

export default {
data () {
    return {
        username:'',
    };
},

components: {
    
},
mounted() {
    this.$api.auth.get_user_name().then((name) => { this.username = name})
},

methods: {
    logout() {
        localStorage.removeItem('token')
        localStorage.removeItem('AES-key')
        localStorage.removeItem('AES-iv')
        this.$router.push('/')
    }
}
}
</script>

<style scoped>
#header{
    padding: 10px;
    display: inline-block;
    width: 100%;
    border-bottom: solid 1px #00000020;
    text-align: right;
}

#user_name{
    color: #409EFF;
    margin-right: 15px;
}
</style>