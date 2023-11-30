<template>
    <el-container>
        <sideBar></sideBar>
        <el-container direction="vertical">
            <headBar></headBar>
            <el-main>
                <router-view/>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
data () {
    return {

    };
},

components: {
    sideBar:()=>import('./sideBar.vue'),
    headBar:()=>import('./headBar.vue')
},
mounted() {
},

methods: {
    
}
}
</script>

<style>
</style>