<template>
<el-dialog title="新建班级" :visible.sync="newClassVisible" :destroy-on-close="true" :center="true" @close="$emit('close')">
<el-form ref="form" :rules="$formRules" :model="form" status-icon label-width="100px" size="mini">
    <el-form-item label="班级名称" prop="class_name">
        <el-input type="text"  v-model="form.class_name"></el-input>
    </el-form-item>
</el-form>
<div slot="footer" class="dialog-footer">
    <el-button @click="newClassVisible=false">取 消</el-button>
    <el-button type="primary" @click="$refs['form'].validate().then(submit)">确 定</el-button>
</div>
</el-dialog>
</template>

<script>
export default {
props: [
    'newClassVisible'
],
data () {
    return {
        form:{class_name:''}
    };
},
components: {
},
mounted() {

},

methods: {
    submit() {
        this.$api.teacher.create_class(this.form.class_name).then(() => {
            this.$message.success('新建班级成功')
            this.form.class_name=''
            this.$emit('newClass')
            this.$emit('close')
        }).catch(() => {
            this.$message.error('新建班级失败')
        }
        )
    }
}
}
</script>

<style scoped>
</style>