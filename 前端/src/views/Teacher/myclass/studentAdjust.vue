<template>
<el-dialog  :title = current_class.name :visible.sync="studentAdjustVisible" :before-close="handleClose">
    <!-- <el-row style="margin-bottom: 30px;">
        <el-col :span="6">
        <el-input placeholder="输入学号" v-model="adding_student_id">
        </el-input>
        </el-col>
        <el-col :span="4" :offset="1">
            <el-button type="success" plain icon="el-icon-circle-plus" @click="all_students.push()">添加学生</el-button>
        </el-col>
    </el-row> -->
    <el-transfer
        filterable :props="{key: 'id',label: 'name'}"
        :data="all_students" v-model="except_students"
        :titles="['当前班级中学生', '被排除的学生']"
        filter-placeholder="可根据学号或姓名搜索"
        :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
        }"
        >
    </el-transfer>
</el-dialog>
</template>

<script>
export default {
props: [
        'current_class',
        'studentAdjustVisible'
],
data () {
    return {
        all_students: [],
        except_students: []
        
    };
},

components: {
    
},
mounted() {
    
},

methods: {
    handleClose() {
        this.$emit('close')
        var old_except_student = this.current_class.except_students.map(stu => stu.id)
        var add_student_list = old_except_student.filter(stu => !this.except_students.includes(stu))
        var remove_student_list = this.except_students.filter(stu => !old_except_student.includes(stu))

        if (add_student_list.length) {
            this.$api.teacher.student_adjust(this.current_class.id, add_student_list, true)
            this.current_class.except_students = this.current_class.except_students.filter(
                stu => !add_student_list.includes(stu.id)
            )
        }
        if (remove_student_list.length) {
            this.$api.teacher.student_adjust(this.current_class.id, remove_student_list, false)
            this.current_class.except_students = this.current_class.except_students.concat(
                this.current_class.all_students.filter(stu => remove_student_list.includes(stu.id)&& !old_except_student.includes(stu.id))
            )
        }
        this.current_class.all_students=this.current_class.all_students.filter(stu => !this.current_class.except_students.includes(stu.id))
        this.current_class.permission_students_id=this.current_class.permission_students_id.filter(stu => !this.current_class.except_students.includes(stu.id))
    },
},
watch: {
    current_class() {
        this.all_students = this.current_class.all_students.concat(this.current_class.except_students)
        this.except_students = this.current_class.except_students.map(stu => stu.id)
    }
}
}
</script>

<style scoped>

</style>