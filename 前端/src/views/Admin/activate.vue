<template>
<div>
<el-row style="margin-bottom: 14px;">
    <el-col :span="8">
    <el-autocomplete placeholder="搜索用户名称或用户id（支持正则）" v-model="search_content" clearable :fetch-suggestions="querySearch" style="width:100%"></el-autocomplete>
    </el-col>
    <el-col :span="4" :offset="1">
        <el-select v-model="filter_academy" placeholder="学院筛选" clearable style="margin-left: 20px;">
            <el-option v-for="academy in academys" :key="academy.value" :label="academy.label" :value="academy.value"></el-option>
        </el-select>
    </el-col>
</el-row>

<el-table :data="show_users" :border=true :fit=true height="610">
<el-table-column align="center" label="id" prop="id" width="180">
</el-table-column>
<el-table-column align="center" label="姓名" prop="name" width="180">
</el-table-column>
<el-table-column align="center" label="邮箱" prop="email" width="240">
</el-table-column>
<el-table-column align="center" label="学院" prop="academy">
</el-table-column>
<el-table-column align="center" label="身份" prop="identity" width="180">
    <template v-slot="scope">
        <el-tag style="font-size: medium;" :type="identity_map[scope.row.identity].tag_type">{{ identity_map[scope.row.identity].text }}</el-tag>
    </template>
</el-table-column>
<el-table-column align="center" label="用户是否通过邮箱激活" prop="identity" width="180">
    <template v-slot="scope">
        <i :class="scope.row.activate_code?'el-icon-close':'el-icon-check'"></i>
    </template>
</el-table-column>
<el-table-column align="center" label="操作" width="240">
    <template v-slot="scope">
        <el-button type="primary" plain size="small" @click="activate_permission_user(scope.row)" style="margin-right: 10px;">激活账号</el-button>
        <el-button type="danger" size="small" @click="delete_user(scope.row)">删除注册记录</el-button>
    </template>
</el-table-column>
</el-table>

</div>
</template>

<script>
export default {
data () {
    return {
        users: [],
        filter_academy:'',
        academys: [],
        search_content: '',

        identity_map: {
            'teacher': { text: '教师',  tag_type:'success'},
            'student': { text: '学生',  tag_type:''},
            'admin'  : { text: '管理员',tag_type:'warning'},
        }
    };
},
components: {
},
mounted() {
    this.refresh_user()
},

methods: {
    refresh_user() {
        this.$api.admin.get_unactivated_user().then((response) => { 
            console.log(response)
            this.users = response
            var academys = []
            for (var i = 0; i < response.length; i++) {
                if (!academys.includes(response[i].academy)) {
                    academys.push(response[i].academy)
                    this.academys.push({ label: response[i].academy, value: response[i].academy })
                }
            }
            this.$forceUpdate()
        })
    },
    confirm(user) {
        const h = this.$createElement
        return new Promise((resolve, reject) => {
            this.$confirm('', {
            message:h('div',null, [
                h('i',{ class:'el-icon-question',style:'color:#f90;font-size:40px;' }),
                h('span', { style: 'margin-left:10px;font-size:16px;line-height:30px;font-weight:600;vertical-align:top;' }, '为防止误操作请确认用户信息'),
                h('p', { style: 'margin:10px 0 0 40px;' }, 'id : ' + user.id),
                h('p', { style: 'margin:10px 0 0 40px;' }, '名称 : ' + user.name),
                h('p', { style: 'margin:10px 0 0 40px;' }, '身份 : ' + this.identity_map[user.identity].text),
                h('p', { style: 'margin:10px 0 0 40px;' }, '学院 : ' + user.academy),
            ]),
            confirmButtonText: '确定',
            cancelButtonText: '取消',
        })
        .then(res => {
            resolve(res);
        })
        .catch(err => {
            this.$message.info('已取消');
            reject(err)
        })
    });
    },
    activate_permission_user(user) {
        this.$api.admin.activate_permission_user(user.activate_code).then(() => {
            this.$notify.success({ title: '激活成功', message: ''})
        }).catch(() => {
            this.$notify.error({ title: '激活用户失败', message:'' })
        })
    },
    delete_user(user) {
        this.confirm(user).then(() => {
            this.$api.admin.delete_user(user.activate_code).then(() => {
                this.$notify.success({ title: '删除成功', message: ''})
            }).catch(() => {
                this.$notify.error({ title: '删除失败', message:'' })
            })
        })
        
    },
    //搜索建议
    querySearch(queryString, cb) {
        var result=[]
        for(var i in this.show_user){
            result.push({ 'value' : this.show_users[i]['name'] })
        }
        cb(result);
    },

},
computed: {
    show_users: {
        get() {
            return (this.search_content == ''&&this.filter_academy=='') ? this.users : this.users.filter(
                (user) => {
                    if (this.filter_academy && user.academy != this.filter_academy)
                        return false
                    return user.name.match(this.search_content) || user.id.match(this.search_content)
                }
            )
        },
        set(users) {
            this.search_content = ''
            this.users = users
        }
        
    }
}
}

</script>

<style scoped>

</style>