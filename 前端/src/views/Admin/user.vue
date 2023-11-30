<template>
<div>
<el-row style="margin-bottom: 14px;">
    <el-col :span="8">
    <el-autocomplete placeholder="搜索用户名称或用户id（支持正则）" v-model="search_content" clearable :fetch-suggestions="querySearch" style="width:100%"></el-autocomplete>
    </el-col>
    <el-col :span="6" :offset="3">
        <el-select v-model="filter_academy" placeholder="学院筛选" clearable>
            <el-option v-for="academy in academys" :key="academy.value" :label="academy.label" :value="academy.value"></el-option>
        </el-select>
    </el-col>
    <el-col :span="3">
        <el-select v-model="filter_identity" placeholder="身份筛选" clearable>
            <el-option v-for="identity in identities" :key="identity.value" :label="identity.label" :value="identity.value"></el-option>
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
<el-table-column align="center" label="操作" width="240">
    <template v-slot="scope">
        <el-button type="primary" plain size="small" @click="reset_user_password(scope.row)" style="margin-right: 10px;">重置密码</el-button>
        <el-button type="danger" size="small" @click="delete_user(scope.row)">删除用户</el-button>
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
        filter_identity:'',
        identities:[],
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
        this.$api.admin.admin_get_user_list().then((response) => { 
            this.users = response
            var academys = []
            var identities = []
            for (var i = 0; i < response.length; i++) {
                if (!academys.includes(response[i].academy)) {
                    academys.push(response[i].academy)
                    this.academys.push({ label: response[i].academy, value: response[i].academy })
                }
                if (!identities.includes(response[i].identity)) {
                    identities.push(response[i].identity)
                    this.identities.push({ label: this.identity_map[response[i].identity].text, value: response[i].identity })
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
    reset_user_password(user) {
        this.confirm(user).then(() => {
            this.$api.admin.reset_user_password(user.id).then((new_password) => {
                this.$notify.success({ title: '重置密码成功', message: '新密码:【'+new_password+'】 请转告用户', duration: 0})
            }).catch(() => {
                this.$notify.error({ title: '重置密码失败', message:'' })
            })
        })
    },
    delete_user(user) {
        this.confirm(user).then(() => {
            this.$api.admin.delete_user(user.id).then(() => {
                this.$notify.success({ title: '成功删除用户', message: ''})
                this.refresh_user()
            }).catch(() => {
                this.$notify.error({ title: '删除用户失败失败', message:'' })
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
            return (this.search_content == ''&&this.filter_academy==''&&this.filter_identity=='') ? this.users : this.users.filter(
                (user) => {
                    if (this.filter_academy && user.academy != this.filter_academy)
                        return false
                    if (this.filter_identity && user.identity != this.filter_identity)
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