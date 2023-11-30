<template>
<div @click="$router.push({name:'Student_upload', params:{'collection':collection}})" v-show="collection.collection_state=='收集中'||collection.collection_state=='即将截止'" >
    <el-card class="collection_card" :class="{red_card:!collection.finished&&collection.collection_state=='即将截止'}" shadow="never">
        <div slot="header" class="collection_card_header" justify="space-between">
            <el-row >
                <el-col :span="!collection.finished&&collection.collection_state=='即将截止'?18:24"><el-tag style="font-size: medium;">{{ collection.class_name }}</el-tag></el-col>
                <el-col :span="!collection.finished&&collection.collection_state=='即将截止'?6:0"><el-tag type="danger">即将截止</el-tag></el-col>
            </el-row>
            <el-row>
                <el-col>{{ collection.collection_name }}</el-col>
            </el-row>
        </div>
    
        <cover :cover="collection.cover" :width="250"></cover>
        <el-statistic ref="statistic" title="距离截止" time-indices
            :format="(collection.collection_state=='即将截止'?'':'D天 ')+'HH:mm:ss'"
            :value="new Date(collection.collection_end_time).getTime()"
            @finish="time_up()"></el-statistic>
    </el-card>
</div>
</template>

<script>

import cover from '../../components/cover.vue'
export default {
props: [
    'collection',
],
data () {
    return {
        flag:false
    };
},

components: {
    cover
},
mounted() {
    setTimeout("this.flag=true", 10)
},

methods: {
    time_up() {
        if (this.flag)
            this.$router.go(0)
    }
}
}
</script>

<style scoped>
.collection_card:hover{
    box-shadow: 4px 8px 24px 0 rgba(0,0,0,.25);
    transform: scale(1.1,1.1);
    transform-origin: center center;
    transition:all 0.3s linear;
}
.red_card,.red_card:hover{
    animation: breath 1.5s linear infinite alternate;
}

@keyframes breath {
    0%   { box-shadow: 2px 4px 8px 0 rgba(255, 0, 0,.2); }
    100% { box-shadow: 2px 4px 16px 1px rgba(255, 55, 0, 0.5); }
}

.collection_card{
    width: 290px;
    border-radius: 18px;
}
</style>