<template>
<div>
<el-row style="margin-bottom: 14px;">
    <el-col :span="8">
    <el-autocomplete placeholder="搜索班级名称或班级号（支持正则）" v-model="search_content" clearable :fetch-suggestions="querySearch" style="width:100%"></el-autocomplete>
    </el-col>
    <el-col :span="2" :offset="1">
        <el-button type="success" plain icon="el-icon-circle-plus" @click="newClassVisible=true">新增班级</el-button>
    </el-col>
</el-row>

<el-table :data="show_classes" :border=true :fit=true>
<el-table-column align="center" label="封面" width="180">
    <template v-slot="scope">
        <cover :cover="scope.row.cover" :key="scope.row.id+scope.row.cover" @click.native="cover_modify_open(scope.row.id)"></cover>
    </template>
</el-table-column>
<el-table-column align="center" label="班级名称" width="260" prop="class_name">
    <template v-slot="scope">
        <el-input v-model="scope.row.name" @change="update_class(scope.row.id,'name',scope.row.name)" :minlength="2" :maxlength="30" :show-word-limit="true"></el-input>
    </template>
</el-table-column>
<el-table-column align="center" label="班级号" width="100" prop="id"></el-table-column>
<el-table-column align="center" label="授权收集学生" width="235">
    <template v-slot="scope">
        <el-select style="width:100%"
        v-model="scope.row.permission_students_id" multiple filterable placeholder="请选择授权学生(可搜索)"
        @change="permission_students_change(scope.row.id, scope.row.permission_students_id)">
            <el-option 
            v-for="stu in scope.row.all_students" 
            :key="stu.id" :label="stu.name" :value="stu.id">
                <span style="float: left">{{ stu.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ stu.id }}</span>
            </el-option>
        </el-select>
    </template>
</el-table-column>

<el-table-column align="center" label="组成班">
    <template slot="header">
        组成班 <el-button size="small" round type="info" @click="component_classes_edit_switch = !component_classes_edit_switch;$message.info('编辑模式切换成功')">(编辑模式切换按钮)</el-button>
    </template>
    <template slot-scope="scope">
        <el-select style="width:100%"
        :disabled="component_classes_edit_switch"
        v-model="scope.row.component_classes" multiple filterable placeholder="请选择组成班(可搜索)" 
        @change="component_classes_change(scope.row.id, scope.row.component_classes)">
            <el-option
                v-for="class_ in classes.filter((cla)=>cla.id!=scope.row.id&&!cla.component_classes.includes(scope.row.id))"
                :key="class_.id" :label="class_.name" :value="class_.id">
                <span style="float: left">{{ class_.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ class_.id }}</span>
            </el-option>
        </el-select>
    </template>
</el-table-column>
<el-table-column align="center" label="操作" width="210">
    <template v-slot="scope">
        <el-button type="primary" plain size="small" @click="member_adjust(scope.row.id)" style="margin-right: 10px;">成员调整</el-button>
        <el-button type="danger" size="small" @click="delete_class(scope.row.id,scope.row.name)">解散班级</el-button>
    </template>
</el-table-column>
</el-table>

<newClassDialog :newClassVisible="newClassVisible" @close="newClassVisible=false" @newClass="refresh_classes"></newClassDialog>

<studentAdjust :studentAdjustVisible="studentAdjustVisible" @close="adjusted()" :current_class="current_class"></studentAdjust>

<el-dialog :title="'修改封面 - '+current_class.name" :visible.sync="coverModifyVisible" :center="true" width="40%">
<coverUploader v-if="coverModifyVisible" :cover="current_class.cover" :class_id="current_class.id" @change="cover_change" @close="coverModifyVisible=false" @uploadSuccess="uploadSuccess"></coverUploader>
<div slot="footer" class="dialog-footer">
    <el-button @click="coverModifyVisible=false">取 消</el-button>
    <el-button type="primary" @click="cover_modify_submit">确 定</el-button>
</div>
</el-dialog>


</div>
</template>

<script>
import newClassDialog from './myclass/newClassDialog.vue'
import cover from '../components/cover.vue'
import coverUploader from './myclass/coverUploader.vue'
import studentAdjust from './myclass/studentAdjust.vue'

export default {
data () {
    return {
        classes: [],
        search_content: '',
        current_class: {},

        newClassVisible: false,
        coverModifyVisible: false,
        studentAdjustVisible: false,
        component_classes_edit_switch:true,
    };
},
components: {
    newClassDialog,
    cover,
    coverUploader,
    studentAdjust
},
mounted() {
    this.refresh_classes()
},

methods: {
    refresh_classes() {
        this.$api.teacher.get_class_list().then((response) => { 
            this.classes = response
        })
    },
    set_current_class(class_id) {
        this.current_class=this.classes.find(class_ => {
            return class_.id==class_id;
        })
    },
    
    //更新字段内容
    update_class(class_id, field, data) {
        this.$api.teacher.update_class(class_id, field, data).then(() => {
                this.$message.success('修改成功')
            }
        ).catch(() => {
                this.$message.error('修改失败,请排查原因后重试')
            }
        )
    },
    //封面相关
    cover_modify_open(class_id) {
        this.set_current_class(class_id)
        this.coverModifyVisible = true
    },
    cover_change(new_cover) {
        this.current_class.cover = new_cover
    },
    cover_modify_submit() {
        this.$api.teacher.update_class(this.current_class.id, 'cover', this.current_class.cover).then(() => {
            this.$message.success('修改封面成功')
            }
        ).catch(() => {
                this.$message.error('修改封面失败,请排查原因后重试')
            }
        )
        this.coverModifyVisible = false
        },
    uploadSuccess() {
        this.cover_modify_submit()
        this.$router.go(0)
    },
    //修改授权学生
    permission_students_change(class_id,permission_students_id) {
        this.update_class(class_id,'permission_students_id',permission_students_id.join())
    },
    //修改组成班
    component_classes_change(class_id, component_classes_id) {
        this.update_class(class_id,'component_classes_id',component_classes_id.join())
    },
    //成员调整
    member_adjust(class_id) {
        this.set_current_class(class_id)
        this.studentAdjustVisible = true
    },
    adjusted() {
        this.studentAdjustVisible = false
    },
    //删除班级
    delete_class(class_id,class_name) {
        this.set_current_class(class_id)
        this.$confirm('解散班级是不可挽回的, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            this.$api.teacher.delete_class(class_id).then(() => {
                this.$notify.success({ title: '解散班级成功', message: class_name + '已被成功解散' })
                this.refresh_classes()
            }).catch(() => {
                this.$notify.message.error({ title: '解散班级失败', message:'请联系管理员解决' })
            })
        }).catch(() => {
            this.$message.info('已取消删除');
        })
    },
    //搜索建议
    querySearch(queryString, cb) {
        var result=[]
        for(var i in this.show_classes){
            result.push({ 'value' : this.show_classes[i]['name'] })
        }
        cb(result);
    },

},
computed: {
    show_classes: {
        get() {
            return this.search_content == '' ? this.classes : this.classes.filter(
                (class_) => class_.name.match(this.search_content) || class_.id.match(this.search_content)
            )
        },
        set(classes) {
            this.search_content = ''
            this.classes = classes
        }
        
    }
}
}

</script>

<style scoped>

</style>