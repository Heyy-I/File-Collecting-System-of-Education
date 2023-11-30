<template>
    <el-card shadow="hover" class="row-bg course" type="flex" justify="space-between" @click.native="$emit('upload', collection)">
        <el-badge value="即将截止">
            <img :src=collection.img_url>
        </el-badge>
        <h3>{{collection.course_name}}</h3>
        <h4>{{collection.collection_name}}</h4>
        <h5>截止时间 : {{collection.deadline}}</h5>
    </el-card>
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

    methods:{},

    computed:{},

    created(){},

    components:{}
}

</script>



<style scoped>
h1,h2,h3,h4,h5,h6 {
    margin: 0;
    padding: 0;
}
.course{
    min-height: 234px;
    max-height: 234px;
    min-width: 276px;
    max-width: 276px;
    margin: 20px;
    border-radius: 8px;
    color: #444444;
    overflow:visible;
}
.course img{
    border-radius: 8px;
    height: 130px;
    aspect-ratio: 24/13;
}
</style>