<template>
<div>
<el-radio-group v-model="cover_type">
    <el-radio-button label="使用模板封面"></el-radio-button>
    <el-radio-button label="上传自定义封面"></el-radio-button>
</el-radio-group>
<div class="cover_uploader">
    <div v-show="cover_type=='使用模板封面'">
        <el-row>
        <el-col :span="15">
            <cover class="cover_viewer" :width="240" :cover="cover_string" :key="cover_string"></cover>
        </el-col>
        <el-col :span="9">
            <el-select size="medimum" v-model="cover_template" placeholder="请选择模板">
                <el-option
                v-for="template in cover_templates"
                :key="template.value"
                :label="template.label"
                :value="template.value">
                <cover :cover="'template:' + template.value + '/' + primary_color + '/' + secondary_color" :key="cover_string"></cover>
                </el-option>
            </el-select>

            <el-select size="medimum" v-model="color_recomand" placeholder="推荐颜色组合" @change="color_recomand_choose">
                <el-option
                v-for="color in color_recomand_list"
                :key="color.value"
                :label="color.label"
                :value="color.value">
                </el-option>
            </el-select>
            <el-color-picker size="medimum" @change="color_recomand=''" v-model="primary_color"></el-color-picker>
            <el-color-picker size="medimum" @change="color_recomand=''" v-model="secondary_color"></el-color-picker>
        </el-col>
        </el-row>
        
    </div>
    
    <div v-show="cover_type=='上传自定义封面'">
        <el-row>
            <el-col :span="12">
                <el-tag>旧封面</el-tag>
                <br>
                <el-image v-if="src" class="cover_viewer" :src="src"></el-image>
                <!-- v-if不要动, 通过v-if刷新才行不然再打开会不显示 -->
            </el-col>
            <el-col :span="12">
                <el-tag>上传处(图片需小于4M)</el-tag>
                <el-upload
                    class="cover_viewer"
                    action="cover_upload"
                    :http-request="$api.teacher.cover_upload(class_id)"
                    :on-success="cover_update"
                    :show-file-list="false"
                    :limit=1
                    >
                    <i class="el-icon-plus"></i>
                </el-upload>
            </el-col>
        </el-row>
    </div>
    
</div>
</div>
</template>

<script>
import cover from '../../components/cover.vue'

export default {
props: [
'cover',
'class_id',

],
data () {
    return {
        cover_type: '',
        cover_template: '01',
        primary_color: '#FFF',
        secondary_color:'#48B',
        cover_templates: [],

        color_recomand:'',
        color_recomand_list: [
            { value: '#FFFFFF,#4488BB', label: '白蓝' },
            { value: '#4488BB,#FFFFFF', label: '蓝白' },
            { value: '#F0E68C,#F5F5DC', label: '黄黄' },
            { value: '#CD5C5C,#EEE8AA', label: '红黄' }
        ],
        src: null,
    };
},

components: {
    cover
},
mounted() {
    for (let i = 1; i <= 21; i++){
        this.cover_templates.push({value:(i<10?'0':'') + i.toString(),label:i.toString()+'号模板'})
    }
    this.cover_templates[0].label += ' - 编织';
    this.cover_templates[1].label += ' - 波浪';
    this.cover_templates[2].label += ' - 曲线';
    this.cover_templates[3].label += ' - 草地';
    this.cover_templates[4].label += ' - 彩带';
    
	//template:(1)/(2)/(3)
	//(1)模板号		(2)主色		(3)副色
	var template_re = /template:(.{2})\/(.+)?\/(.+)?/
    var split = this.cover.match(template_re)
    if (split) {
        this.cover_type = '使用模板封面'
        this.cover_template = split[1]
        this.primary_color = split[2]
        this.secondary_color = split[3]

        if (!this.primary_color) this.primary_color = 'white'
        if (!this.secondary_color) this.secondary_color = '#48B'
    }
    else {
        this.cover_type = '上传自定义封面'
    }
    this.src = this.$urls.api_url + this.$urls.auth.get_cover + this.class_id
},

methods: {
    cover_update() {
        this.$api.teacher.update_class(this.class_id, 'cover', this.cover_string).then(() => {
            this.$notify.success("上传封面成功")
            this.$emit('uploadSuccess')
        })
        .catch(() => {
            this.$notify.error("上传封面错误")
        });
        
    },
    color_recomand_choose() {
        var colors = this.color_recomand.match(/(.+),(.+)/)
        this.primary_color = colors[1]
        this.secondary_color = colors[2]
    },
},
computed:{
    cover_string() {
        let new_cover=this.cover_type=='使用模板封面'?'template:' + this.cover_template + '/' + this.primary_color + '/' + this.secondary_color:'image:'+this.class_id
        this.$emit('change',new_cover)
        return new_cover
    }
},
watch: {
}
}
</script>

<style scoped>
.cover_uploader{
    margin-top:10px;
}
.cover_viewer{
width: 240px;
height: 135px;
border: 2px dashed #d9d9d9;
border-radius: 6px;
cursor: pointer;
position: relative;
overflow: hidden;
}
.cover_viewer:hover {
border-color: #409EFF;
}
.cover_viewer i {
font-size: 28px;
color: #8c939d;
width: 240px;
height: 135px;
line-height: 135px;
text-align: center;
}
</style>