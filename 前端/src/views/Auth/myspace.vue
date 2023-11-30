<template>
<div>
<!-- <el-collapse v-model="activeNames" accordion> -->
    <!-- <el-collapse-item title="账号信息" name="1"> -->
        <el-table :data="user" :border=true :fit=true>
        
        <el-table-column align="center" label="学号" width="150" prop="id"></el-table-column>
        <el-table-column align="center" label="姓名" width="260" prop="name">
            <template v-slot="scope">
                <el-input v-model="scope.row.name" @change="change_name" :minlength="2" :maxlength="30" :show-word-limit="true"></el-input>
            </template>
        </el-table-column>
        <el-table-column align="center" label="密码" width="180" prop="password">
                <el-button type="primary" @click="dialogFormVisible=true">修改</el-button>
        </el-table-column>
        <el-table-column align="center" label="邮箱" width="340" prop="email">
            <template v-slot="scope">
                <el-row>
                    <el-col :span="18">
                        <el-input v-model="scope.row.email"  :minlength="2" :maxlength="30"></el-input>
                    </el-col>
                    <el-col :span="2">
                        <el-button type="primary" @click="change_email">修改</el-button>
                    </el-col>
                </el-row>
                
            </template>
        </el-table-column>
        
        <el-table-column align="center" label="学院" width="280" prop="academy"></el-table-column>
        <el-table-column align="center" label="身份" prop="identity">
            <template v-slot="scope">
                <el-tag style="font-size: medium;" :type="identity_map[scope.row.identity].tag_type">{{ identity_map[scope.row.identity].text }}</el-tag>
            </template>
        </el-table-column>
        </el-table>

    <!-- </el-collapse-item>
    <el-collapse-item title="账号安全" name="2">

    </el-collapse-item>
    <el-collapse-item title="使用设置" name="3">
        
    </el-collapse-item>
</el-collapse> -->

<el-dialog title="修改密码" :visible.sync="dialogFormVisible">
    <el-form :model="form" :rules="$formRules" ref="form">
        <el-form-item label="旧密码" prop="old_password">
            <el-input v-model="form.old_password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
            <el-input v-model="form.new_password" autocomplete="off"></el-input>
        </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="change_password">确 定</el-button>
    </div>
</el-dialog>
</div>
</template>

<script>
export default {
data () {
    return {
        // activeNames:'1',
        form:{old_password:'',new_password:''},
        user: [],
        dialogFormVisible:false,
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
    this.get_my_info()
},

methods: {
    logout() {
        localStorage.removeItem('token')
        localStorage.removeItem('AES-key')
        localStorage.removeItem('AES-iv')
        this.$router.push('/')
    },
    get_my_info() {
        this.$api.auth.get_my_info().then((response) => {
            this.user=[]
            this.user.push(response)
            this.user[0].old_password = ''
            this.user[0].new_password = ''
        })
    },
    change_name() {
        this.$api.auth.change_name(this.user[0].name).then(() => {
            this.$message.success('修改成功!')
        }).catch(() => {
            this.$message.error('修改失败')
        })
    },
    change_password() {
        this.dialogFormVisible = false
        this.$api.auth.change_password(this.form).then(() => {
            this.$notify.success({ title: '修改密码成功!', message: '请前往邮箱进行确认', duration: 0})
            this.logout()
        })
    },
    change_email() {
        if (this.user[0].email.match(/^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/)) {
            this.$api.auth.change_email(this.user[0].email).then(() => {
                this.$notify.success({ title: '修改邮箱成功!', message: '请前往旧邮箱进行确认', duration: 0})
                this.logout()
            }).catch(() => {
                this.$message.error('邮箱已被占用')
            })
        }
        else {
            this.$message.error('邮箱格式不正确')
        }
    }
}
}
</script>

<style scoped>
</style>