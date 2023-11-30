<template>
<el-dialog title="新建文件收集任务" :visible.sync="newCollectionVisible" :destroy-on-close="true" :center="true" @close="$emit('close')">
<el-form ref="form" :rules="$formRules" :model="form" status-icon label-width="100px">
    <el-form-item label="收集名称" prop="collection_name">
        <el-input type="text" placeholder="请输入收集名称" v-model="form.collection_name" :maxlength="255"></el-input>
    </el-form-item>
    <el-form-item label="收集内容" prop="collection_info">
        <el-input type="textarea" placeholder="请介绍收集内容" v-model="form.collection_info" :autosize="{ minRows: 1, maxRows: 6}" :maxlength="500"> </el-input>
    </el-form-item>
    <el-row>
        <el-col :span="12"><el-form-item label="开始时间" prop="collection_start_time">
            <el-date-picker v-model="form.collection_start_time" type="datetime" placeholder="选择收集开始时间" :picker-options="pickerOptions" :clearable="false"></el-date-picker>
        </el-form-item></el-col>
        <el-col :span="12"><el-form-item label="截止时间" prop="collection_end_time">
            <el-date-picker v-model="form.collection_end_time" type="datetime" placeholder="选择收集截止时间" :picker-options="pickerOptions" :clearable="false"></el-date-picker>
        </el-form-item></el-col>
    </el-row>
    <el-form-item
        v-for="(item, index) in form.collection_items" :label="'收集项' + (index+1)" :key="index"
        :rules="{required: true, message: '收集项不能为空', trigger: 'blur'}">
        <el-input v-model="item.info" :maxlength="255"></el-input>
        <el-row>
            <!-- <el-col :span="4">
                <el-select v-model="item.type" placeholder="请选择收集类型">
                    <el-option v-for="item_type in collection_item_types" :key="item_type.value" :label="item_type.label" :value="item_type.value"></el-option>
                </el-select>
            </el-col> -->
            <el-col :span="16" v-show="item.item_type==0">
                <el-select v-model="item.file_type_confine" allow-create placeholder="文件类型">
                    <el-option v-for="file_type in file_type_confines" :key="file_type.value" :label="file_type.label" :value="file_type.value"></el-option>
                </el-select>
            </el-col>
            <!-- <el-col :span="2" :offset="1"><el-checkbox v-model="item.necessary" :disabled="index==0">必填</el-checkbox></el-col> -->
            <el-col :span="4" :offset="1" v-show="index>0"><el-button @click.prevent="form.collection_items.splice(index, 1)">删除</el-button></el-col>
        </el-row>
    </el-form-item>
</el-form>
<div slot="footer" collection="dialog-footer">
    <el-button @click="newCollectionVisible=false">取 消</el-button>
    <el-button type="primary" @click="$refs['form'].validate().then(submit)">确 定</el-button>
    <el-button @click="new_collection_items()">新增收集项</el-button>
</div>
</el-dialog>
</template>

<script>
export default {
props: [
    'newCollectionVisible',
    'class_id',
    'class_name'
],
data () {
    return {
        form: { class_id:this.class_id, class_name:this.class_name, collection_start_time: new Date(),
            collection_name: '', collection_info: '', collection_items: []},
        pickerOptions: {
            shortcuts: [{
                text: '现在',
                onClick(picker) {
                    picker.$emit('pick', new Date());
                }
            }, {
                text: '明天',
                onClick(picker) {
                    const date = new Date();
                    date.setTime(date.getTime() + 3600 * 1000 * 24);
                    picker.$emit('pick', date);
                }
            }, {
                text: '一周后',
                onClick(picker) {
                    const date = new Date();
                    date.setTime(date.getTime() + 3600 * 1000 * 24 * 7);
                    picker.$emit('pick', date);
                }
            }]
        },
        // collection_item_types: [
        //     { value: '0', label: '文件' },
        //     { value: '1', label: '仅文字' },
        // ],
        file_type_confines: [
            { value: '*', label: '不限制' },
            { value: 'jpg,png,gif', label: '图片' },
            { value: 'zip,7z,rar', label: '压缩包' },
            { value: 'doc,docx', label: 'word文档' },
        ]
    }
},
components: {
},
mounted() {
    this.new_collection_items()
},

methods: {
    new_collection_items() {
        if (this.form.collection_items.length < 10) {
            this.form.collection_items.push({ value: '',item_type:'0',key: Date.now(),necessary:true,file_type_confine:'*'})
        }
        else {
            this.$message.warning('文件数量上限为10个')
        }
    },
    submit() {
        let valide=true
        for (let i = 0; i < this.form.collection_items.length; i++) {
            if (!this.form.collection_items[i].info) {
                this.$message.error('收集项' + (i+1) + '还未填写')
                valide=false
                break
            }
        }
        if (valide) {
            let data_form = JSON.parse(JSON.stringify(this.form))
            console.log(data_form)
            for (let i = 0; i < data_form.collection_items.length; i++) {
                // if (data_form.collection_items[i].type == 0)
                data_form.collection_items[i].type = '0[' + data_form.collection_items[i].file_type_confine + ']'
            }
            data_form.collection_items = JSON.stringify(data_form.collection_items)
            data_form.collection_start_time = Number(new Date(data_form.collection_start_time))
            data_form.collection_end_time = Number(new Date(data_form.collection_end_time))
            if (data_form.collection_start_time > data_form.collection_end_time) 
                this.$message.error('开始时间应该早于截止时间')
            else
                this.$api.collector.new_collection(data_form).then(()=>{
                    this.$message.success(this.form.collection_name + '创建成功!')
                    this.newCollectionVisible = false
                    this.$refs['form'].resetFields()
                    this.$emit('newCollection')
                })
        }
    }
}
}
</script>

<style scoped>
</style>