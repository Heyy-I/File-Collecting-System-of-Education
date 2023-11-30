<template>
    <el-aside id="sideBar" width="200px">
        <el-menu default-active="default" class="el-menu-vertical" router >
            
            <!-- 一级菜单项 -->
            <el-menu-item v-for="item in menu_dict.items" :index="item.index" :key="item.index">
                <i :class=item.i_class></i>
                <span>{{item.name}}</span>
            </el-menu-item>
            
            <!-- 二级子菜单 -->
            <el-submenu v-for="menu in show_menus" :index="menu.index" :key="menu.index">
                <template slot="title">
                    <i :class=menu.i_class></i>
                    <span>{{menu.name}}</span>
                </template>

                <!-- 二级菜单项 -->
                <el-menu-item v-for="item in menu.items" :index="item.index" :key="item.index" v-show="menu.items">
                    <i :class=item.i_class></i>
                    <span>{{item.name}}</span>
                </el-menu-item>

                <!-- 三级子菜单 -->
                <el-submenu v-for="submenu in menu.submenus" :index="submenu.index" :key="submenu.index" v-show="menu.submenus">
                    <template slot="title">
                        <i :class=submenu.i_class></i>
                        <span>{{submenu.name}}</span>
                    </template>

                    <!-- 三级菜单项 -->
                    <el-menu-item v-for="item in submenu.items" :index="item.index" :key="item.index">
                        <i :class=item.i_class></i>
                        <span>{{item.name}}</span>
                    </el-menu-item>
                </el-submenu>
            </el-submenu>
        </el-menu>
    </el-aside>
</template>

<script>
import {menu_dict} from '../../configs'
export default {
data () {
        return {
            permission_code:0,
            menu_dict:menu_dict
    };
},

components: {
    
},
mounted() {
    this.$api.auth.get_permission_code().then((p_code)=>{this.permission_code=p_code})
},
computed: {
    show_menus() {//通过计算属性过滤掉无权限的菜单
        return this.menu_dict.menus.filter(menu => {
            return menu.permission_code & this.permission_code;//两个权限代码按位与运算
        })
    }
},
methods: {
    
}
}
</script>

<style scoped>
#sideBar{
    float: left;
    overflow-x:hidden;
    color: #333;
    border-right: solid 1px #00000020;
    min-height: 100vh;
}
</style>