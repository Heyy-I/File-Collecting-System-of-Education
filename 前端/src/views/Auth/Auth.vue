<template>
<div class="banner">
<div class="circle circle-1"></div>
<div class="circle circle-2"></div>
<div class="circle circle-3"></div>
<div class="circle circle-4"></div>
<div class="circle circle-5"></div>

<div id="authApp">
    <el-radio-group v-model="action">
        <el-radio-button label="登录"></el-radio-button>
        <el-radio-button label="注册"></el-radio-button>
    </el-radio-group>
    <loginForm v-if="action=='登录'"></loginForm>
    <registForm v-if="action=='注册'"></registForm>
</div>
</div>

</template>

<script>
export default {
    components: {
        loginForm : ()=>import('./loginForm.vue'),
        registForm: ()=>import('./rigistForm.vue')
    },
    data() {
        return {
            action: '登录',
        }
    },
    mounted() {
    },
    methods: {
    }
}
</script>

<style scoped>
#authApp{
    background: white;
    margin: auto;
    margin-top: 60px;
    margin-bottom: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 560px;
    box-shadow: 0 6px 12px #ffffff70, 0 0 15px #0000000a;
}

.el-radio-group{
    margin: 40px;
    text-align: center;
}




.banner {
    height: 100vh;
    background-color: #0c2140;
    position: relative;
    overflow: hidden;
}

.circle {
    background: linear-gradient(to bottom, #ffffff0d, #ffffff2a);
    border-radius: 50%;
}

.circle-1 {
    height: 50px;
    width: 50px;
    position: absolute;
    top: 30px;
    left: 50px;
}

.circle-2 {
    height: 300px;
    width: 300px;
    position: absolute;
    top: 100px;
    left: 40px;
}

.circle-3 {
    height: 300px;
    width: 300px;
    position: absolute;
    top: -50px;
    left: 250px;
}

.circle-4 {
    height: 50px;
    width: 50px;
    position: absolute;
    top: 30px;
    right: 500px;
}

.circle-5 {
    height: 300px;
    width: 300px;
    position: absolute;
    top: -150px;
    right: -150px;
}
</style>