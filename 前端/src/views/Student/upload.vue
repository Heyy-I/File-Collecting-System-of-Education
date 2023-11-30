<template>
    <el-container>
        <el-header>
            <el-page-header @back="$router.go(-1)" content="提交收集任务"></el-page-header>
        </el-header>
        <el-main>
            <el-card>
                <h2 style="margin-bottom: 14px;text-align: center;">{{ collection.class_name }}</h2>
                <h2 style="margin-bottom: 14px;text-align: center;">{{ collection.collection_name }}</h2>
                <el-statistic ref="statistic" time-indices
                :format="'距离截止还有 : '+(collection.collection_state=='即将截止'?'':'D天 ')+'HH:mm:ss'"
                :value="new Date(collection.collection_end_time).getTime()"
                @finish="$router.go(-1)"></el-statistic>
                <el-divider></el-divider>
                {{collection.collection_info}}
            </el-card>
            <div v-for="(item,index) in collection.items" :key="index">
                <el-divider content-position="left" style="font-size: larger;"></el-divider>
                <el-row>
                    <el-col :span="item.exist?0:10" v-show="!item.exist">
                        <el-upload drag action="collection_upload"
                            :http-request="$api.student.collection_upload(item,upload_success(index))"
                            :show-file-list="false" :limit=1>
                            <div class="main_upload">
                                <i class="el-icon-plus"></i>
                                <div class="el-upload__text"><em>将文件拖到此处，或点击上传</em></div>
                                <div class="el-upload__tip" slot="tip">文件不得大于100MB</div>
                                <div class="el-upload__tip" slot="tip" v-show="item.type!='0[*]'">限制文件格式 : {{item.type.match(/0\[(.+)\]/)[1]}}</div>
                            </div>
                        </el-upload>
                    </el-col>
                    <el-col :span="item.exist?6:0" style="text-align: right;">
                        <i class="el-icon-circle-check" style="color:limegreen;font-size: 168px;"></i>
                    </el-col>
                    <el-col :span="item.exist?4:0" style="padding: 70px 0 0 0">
                        <el-button type="warning" @click="roll_back(index)">撤回<i class="el-icon-refresh-left"></i></el-button>
                    </el-col>
                    <el-col :span="14">
                        <el-card style="min-height: 180px;">
                            {{item.info}}
                        </el-card>
                    </el-col>
                </el-row>
            </div>
        </el-main>
    </el-container>
</template>



<script>
export default {
data(){
    return {
    }
},
props: [
'collection',
],

methods:{
    upload_success(index) {
        return () => {
            this.$message.success('上传文件成功')
            this.collection.items[index].exist = true
            this.$forceUpdate()
        }
    },
    roll_back(index) {
        this.$api.student.roll_back(this.collection.collection_id, index).then(() => {
            this.$message.success('撤销文件成功')
            this.collection.items[index].exist = false
            this.$forceUpdate()
        })
    }
},

computed:{},

watch : {},

created(){},

mounted() {
    console.log(this.collection)
    if (this.collection == null) {
        this.$router.push('/Student_collections')
    }
},

components:{
}
}

</script>

<style scoped>
.el-col{
    text-align: center;
}
.main_upload{
    padding-top: 50px;
}
.main_upload>i{
    font-size: xx-large;
    color: #409EFF;
}
</style>