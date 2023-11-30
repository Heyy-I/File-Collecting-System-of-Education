<template>
    <div>
        <el-tag type="warning" style="font-size: medium;margin: 0 0 10px 10px;">未完成</el-tag>
        <div style="display: flex;flex-wrap:wrap;justify-content: space-around;gap: 24px;">
            <collectionCard v-for="(collection,index) in collections.filter((coll)=>!coll.finished)"
                :key="index" :collection="collection"></collectionCard>
        </div>
        <el-divider content-position="left" style="padding: 20px;"></el-divider>
        <el-tag type="success" style="font-size: medium;margin: 0 0 10px 10px;">已完成</el-tag>
        <div style="display: flex;flex-wrap:wrap;justify-content: space-around;gap: 24px;">
            <collectionCard v-for="(collection,index) in collections.filter((coll)=>coll.finished)" 
                :key="index" :collection="collection"></collectionCard>
        </div>
    </div>
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
        if ((new Date(collection.collection_end_time) - new Date()) < 1000 * 60 * 60 * 24) {
            collection_state = '即将截止'
        }
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
import collectionCard from './collections/collectionCard.vue'
export default {
data () {
    return {
        collections: [],
    };
},

components: {
    collectionCard
},
mounted() {
    this.$api.student.get_collection_list().then((response) => {
        response.forEach(collection => {
            collection.collection_start_time = formatDateTime(new Date(collection.collection_start_time))
            collection.collection_end_time = formatDateTime(new Date(collection.collection_end_time))
            collection['collection_state'] = collection_state(collection)
        });
        this.collections = response
    })
},

methods: {
}
}
</script>

<style scoped>

</style>