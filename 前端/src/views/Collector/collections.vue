<template>
<el-container>
        <el-header>
            <el-page-header @back="$router.go(-1)" content="'管理收集任务'"></el-page-header>
        </el-header>
        <el-main>
    <el-row style="margin-bottom: 10px;">
        <el-col :span="4"><el-tag type="info" effect="plain" style="font-size:medium;margin-top: 3px;">{{ class_name }}</el-tag></el-col>
        <el-col :span="12"><el-button  type="success" plain icon="el-icon-circle-plus" @click="newCollectionVisible=true">新增文件收集</el-button></el-col>
    </el-row>
    <el-table :data="class_collections" :border=true :fit=true>
        <el-table-column align="center" label="当前状态" width="130" prop="collection_name">
            <template v-slot="scope">
                <el-tag :type="scope.row.collection_state=='收集中'?'success':'warning'" style="font-size: medium;">{{ scope.row.collection_state }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column align="center" label="收集进度" width="160">
            <template v-slot="scope">
                <el-progress type="circle" :percentage=" Math.floor(scope.row.collection_progress*10)/10" :color="colors"></el-progress>
            </template>
        </el-table-column>
        <el-table-column align="center" label="收集名称" width="150" prop="collection_name">
            <template v-slot="scope">
                <el-input @change="update_collection(scope.row,'collection_name',scope.row.collection_name)"
                type="text" placeholder="请输入收集名称" v-model="scope.row.collection_name" :maxlength="255"></el-input>
            </template>
        </el-table-column>
        <el-table-column align="center" label="收集简介" width="250" prop="collection_info">
            <template v-slot="scope">
                <el-input @change="update_collection(scope.row,'collection_info',scope.row.collection_info)"
                type="textarea" placeholder="请介绍收集内容" v-model="scope.row.collection_info" :autosize="{ minRows: 1, maxRows: 6}" :maxlength="500"> </el-input>
            </template>
        </el-table-column>
        <el-table-column align="center" label="开始时间" width="220" prop="collection_start_time">
            <template v-slot="scope">
                <el-date-picker @change="update_collection(scope.row,'collection_start_time',scope.row.collection_start_time)" 
                v-model="scope.row.collection_start_time" type="datetime" placeholder="选择收集开始时间" :picker-options="pickerOptions" :clearable="false" style="width: 195px;"></el-date-picker>
            </template>
        </el-table-column>
        <el-table-column align="center" label="截止时间" width="220" prop="collection_end_time">
            <template v-slot="scope">
                <el-date-picker @change="update_collection(scope.row,'collection_end_time')" 
                v-model="scope.row.collection_end_time" type="datetime" placeholder="选择收集截止时间" :picker-options="pickerOptions" :clearable="false" style="width: 195px;"></el-date-picker>
            </template>
        </el-table-column>
        <el-table-column align="center" label="操作">
            <template v-slot="scope">
                <el-row :gutter="20">
                    <el-col :span="12"><el-button type="primary" plain size="small" @click="send_remind_email(scope.row.collection_id)">一键提醒</el-button></el-col>
                    <el-col :span="12"><el-button type="primary" plain size="small" @click="download_collection_zip(scope.row.collection_id)">下载文件</el-button></el-col>
                </el-row><el-row :gutter="20" style="margin-top: 10px;">
                    
                    <el-col :span="12"><el-button type="primary" plain size="small" @click="email_collection_zip(scope.row.collection_id)">发送到邮箱</el-button></el-col>
                    <el-col :span="12"><el-button type="danger"  plain size="small" icon="el-icon-delete" @click="delete_collection(scope.row.collection_id)">删除</el-button></el-col>
                </el-row>
            </template>
        </el-table-column>
    </el-table>
    <newCollectionDialog :class_id="class_id" :class_name="class_name" :newCollectionVisible="newCollectionVisible" @close="newCollectionVisible=false" @newCollection="refresh_collections"></newCollectionDialog>

</el-main>
</el-container>
</template>

<script>
let formatDateTime = function (date) {
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h=h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    minute = minute < 10 ? ('0' + minute) : minute;
    var second=date.getSeconds();
    second=second < 10 ? ('0' + second) : second;
    return y + '-' + m + '-' + d+' '+h+':'+minute+':'+second;
};
let collection_state = function (collection) {
    let collection_state = ''
    if (new Date(collection.collection_start_time) < new Date() && new Date(collection.collection_end_time) > new Date()) {
        collection_state = '收集中'
    }
    else if (new Date(collection.collection_end_time) < new Date()) {
        collection_state = '收集已截止'
    }
    else if (new Date(collection.collection_start_time) > new Date()) {
        collection_state = '收集未开始'
    }
    else {
        collection_state = '状态出错'
    }
    return collection_state
};
// 保存到本地
function saveAs(blob) {
        if ('download' in document.createElement('a')) {
            const eleA = document.createElement('a');
            eleA.download = blob.file_name
            eleA.style.display = 'none';
            eleA.href = URL.createObjectURL(blob);
            document.body.appendChild(eleA);
            eleA.click();
            URL.revokeObjectURL(eleA.href); //释放URL对象
            document.body.removeChild(eleA);
        } else {
            // IE下载
            navigator.msSaveOrOpenBlob(blob, blob.file_name)
        }
    }
import newCollectionDialog from './collections/newCollectionDialog.vue'
export default {
props: [
    'class_id',
    'class_name'
],
data() {
    return {
        class_collections: null,
        newCollectionVisible: false,
        colors: [
            {color: '#f56c6c', percentage: 20},
            {color: '#e6a23c', percentage: 40},
            {color: '#5cb87a', percentage: 60},
            {color: '#1989fa', percentage: 80},
            {color: '#6f7ad3', percentage: 100}
        ],
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
    };
},

components: {
    newCollectionDialog
},
mounted() {
    this.refresh_collections()
},

methods: {
    refresh_collections() {
        if (this.class_id) {
            this.$api.collector.get_collections_by_class_id(this.class_id).then((response) => {
                response.forEach(collection => {
                    collection.collection_start_time = formatDateTime(new Date(collection.collection_start_time))
                    collection.collection_end_time = formatDateTime(new Date(collection.collection_end_time))
                    collection['collection_state'] = collection_state(collection)
                });
                this.class_collections = response
            })
        }
        else {
            this.$router.go(-1)
        }
    },
    delete_collection(collection_id) {
        this.$confirm('删除收集任务是不可挽回的, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
        }).then(() => {
            this.$api.collector.delete_collection(collection_id).then(()=>{
                this.$message.success('删除成功!')
                this.refresh_collections()
            }).catch(() => {
                this.$notify.message.error({ title: '删除收集任务失败', message:'请联系管理员解决' })
            })
        }).catch(() => {
            this.$message.info('已取消删除');
        })
    },
    download_collection_zip(collection_id) {
        this.$api.collector.download_collection_zip(collection_id).then(res => {
            saveAs(res)
        })
    },
    email_collection_zip(collection_id) {
        this.$api.collector.email_collection_zip(collection_id).then(() => {
            this.$notify.success('请前往邮箱查看!')
        })
    },
    update_collection(collection, field) {
        var data = collection[field]
        if (field == 'collection_start_time' || field == 'collection_end_time') {
            collection.collection_start_time = Number(new Date(collection.collection_start_time))
            collection.collection_end_time = Number(new Date(collection.collection_end_time))
            data=Number(new Date(data))
        }
        if (collection.collection_start_time > collection.collection_end_time) 
            this.$message.error('开始时间应该早于截止时间')
        else
            this.$api.collector.update_collection(collection.collection_id, field, data).then(() => {
                this.$message.success('修改成功!')
            })
    },
    send_remind_email(collection_id){
        this.$api.collector.send_remind_email(collection_id).then(() => {
            this.$message.success('提醒成功!')
        })
    }
}
}
</script>

<style scoped>

</style>