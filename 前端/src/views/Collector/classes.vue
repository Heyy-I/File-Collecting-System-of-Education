<template>
<div>
    <el-row style="margin-bottom: 14px;">
        <el-col :span="8">
        <el-autocomplete placeholder="搜索班级名称或班级号（支持正则）" v-model="search_content" clearable :fetch-suggestions="querySearch" style="width:100%"></el-autocomplete>
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
            {{ scope.row.name }}
        </template>
    </el-table-column>
    <el-table-column align="center" label="班级号" width="100" prop="id"></el-table-column>
    <el-table-column align="center" label="教师" width="100" prop="teacher_name"></el-table-column>
    <el-table-column align="center" label="操作">
        <template v-slot="scope">
            <el-button type="primary" plain size="large" @click="$router.push({name:'Collector_collections', params:{'class_id':scope.row.id,'class_name':scope.row.name}})">查看收集详情</el-button>
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
            search_content: '',
        };
    },
    components: {
        cover,
    },
    mounted() {
        this.$api.collector.get_class_list().then((response) => { 
            this.classes = response
        })
    },
    
    methods: {
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