<template>
<div>
    <el-row style="margin-bottom: 14px;">
    <el-col :span="4">
        <el-input placeholder="输入班级号（区分大小写）" v-model="class_id" clearable style="width:100%" maxlength="8" show-word-limit></el-input>
    </el-col>
    <el-col :span="2" :offset="1">
        <el-button type="success" plain icon="el-icon-circle-plus" @click="join_class()">加入班级</el-button>
    </el-col>
    <el-col :span="8" :offset="3">
    <el-autocomplete placeholder="搜索班级名称或班级号（支持正则）" v-model="search_content" clearable :fetch-suggestions="querySearch" style="width:100%"></el-autocomplete>
    </el-col>
</el-row>

<el-table :data="show_classes" :border=true :fit=true>
<el-table-column align="center" label="封面" width="180">
    <template v-slot="scope">
        <cover :cover="scope.row.cover" :key="scope.row.id+scope.row.cover"></cover>
    </template>
</el-table-column>
<el-table-column align="center" label="班级号" width="100" prop="id"></el-table-column>
<el-table-column align="center" label="班级名称" width="300" prop="name"></el-table-column>
<el-table-column align="center" label="教师姓名" width="100" prop="teacher_name"></el-table-column>
<el-table-column align="center" label="学院" width="300" prop="academy"></el-table-column>
<el-table-column align="center" label="操作">
    <template v-slot="scope">
        <el-button type="danger" size="small" @click="quit_class(scope.row.id)">退出班级</el-button>
    </template>
</el-table-column>
</el-table>
</div>
</template>

<script>
import cover from '../components/cover.vue'

export default {
data () {
    return {
        classes: [],
        class_id:'',
        search_content: '',
    };
},
components: {
    cover,
},
mounted() {
    this.refresh_classes()
},

methods: {
    refresh_classes() {
        this.$api.student.get_class_list().then((response) => { 
            this.classes = response
        })
    },
    join_class() {
        if (this.class_id.length == 8) {
            this.$api.student.student_join_class(this.class_id).then(() => {
                this.$message.success('加入班级成功!')
                this.refresh_classes()
                this.class_id=''
            }
            ).catch(() => {
                this.$message.error('此班级也许不存在,请确认班级号')
            })
        }
        else
            this.$message.error('班级号长度不足')
    },
    quit_class(class_id) {
        this.$api.student.student_quit_class(class_id).then(() => {
            this.$message.success('成功退出班级!')
            this.refresh_classes()
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