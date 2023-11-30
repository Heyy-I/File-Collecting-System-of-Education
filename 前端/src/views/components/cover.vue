<template>
<div class="cover" :style="cover_size_style">
	
    <el-image v-if="show=='image'" :src="src"></el-image>
	
    <div      v-else :class="'template '+cover_template" :style="{'--primary_color':primary_color,'--secondary_color':secondary_color}"></div>
</div>
    
</template>

<script>
export default {
props: [
    'cover',
    'width'
],
data () {
	return {
		show:'',
		cover_size_style: '',
		cover_template: '',
		primary_color: '',
		secondary_color: '',

		src:''
    };
},

components: {
    
},
mounted() {
	if (this.width) {
		this.cover_size_style = 'width:' + this.width + 'px;'
		this.cover_size_style += 'height:' + this.width / 16 * 9 + 'px;'
	}
	else {
		this.cover_size_style = 'width:160px;height:90px'
	}
	
	//template:(1)/(2)/(3)
	//(1)模板号		(2)主色		(3)副色
	var template_re = /template:(.{2})\/(.+)?\/(.+)?/
	var image_re = /image:([a-zA-Z0-9]{8})/
	if (this.cover.match(template_re)) {
		var split = this.cover.match(template_re)
		this.show = 'template'
		this.cover_template = 'cover_template_' + split[1]
		this.primary_color = split[2]
		this.secondary_color = split[3]
		
		if(!this.primary_color)this.primary_color = 'white'
		if(!this.secondary_color) this.secondary_color = '#48B'
	}
	else if (this.cover.match(image_re)) {
		this.show = 'image'
		var class_id=this.cover.match(image_re)[1]
		this.src = this.$urls.api_url + this.$urls.auth.get_cover + class_id
	}
	else {
		this.show='image'
	}
},

methods: {
    
},
}
</script>

<style scoped>
.cover{
    border-radius: 12px;
    overflow: hidden;
}
.cover img,.cover div{
    width: 100%;
    height: 100%;
}



.cover_template_01{
background: linear-gradient(45deg, #dca 12%, transparent 0, transparent 88%, #dca 0),
linear-gradient(135deg, transparent 37%, #a85 0, #a85 63%, transparent 0),
linear-gradient(45deg, transparent 37%, #dca 0, #dca 63%, transparent 0) #753;
background-size: 25px 25px;
}
.cover_template_02{
	background:
	radial-gradient(
			at bottom right,
			dodgerblue 0,
			dodgerblue 1em,
			lightskyblue 1em,
			lightskyblue 2em,
			deepskyblue 2em,
			deepskyblue 3em,
			gainsboro 3em,
			gainsboro 4em,
			lightsteelblue 4em,
			lightsteelblue 5em,
			deepskyblue 5em,
			deepskyblue 6em,
			lightskyblue 6em,
			lightskyblue 7em,
			transparent 7em,
			transparent 8em
		),
		radial-gradient(
			at top left,
			transparent 0,
			transparent 1em,
			lightskyblue 1em,
			lightskyblue 2em,
			deepskyblue 2em,
			deepskyblue 3em,
			lightsteelblue 3em,
			lightsteelblue 4em,
			gainsboro 4em,
			gainsboro 5em,
			deepskyblue 5em,
			deepskyblue 6em,
			skyblue 6em,
			skyblue 7em,
			dodgerblue 7em,
			dodgerblue 8em,
			transparent 8em,
			transparent 20em
		),
		radial-gradient(
			circle at center bottom,
			coral, darkslateblue
		);
	
	background-blend-mode: overlay;
	background-size:
		8em 8em, 8em 8em, cover;
}
.cover_template_03{
	background:
	radial-gradient(
		circle at bottom left,
		transparent 0,
		transparent 2em,
		beige 2em,
		beige 4em,
		transparent 4em,
		transparent 6em,
		khaki 6em,
		khaki 8em,
		transparent 8em,
		transparent 10em
	),
	radial-gradient(
		circle at top right,
		transparent 0,
		transparent 2em,
		beige 2em,
		beige 4em,
		transparent 4em,
		transparent 6em,
		khaki 6em,
		khaki 8em,
		transparent 8em,
		transparent 10em
	),
	radial-gradient(
		circle at top left,
		transparent 0,
		transparent 2em,
		navajowhite 2em,
		navajowhite 4em,
		transparent 4em,
		transparent 6em,
		peachpuff 6em,
		peachpuff 8em,
		transparent 8em,
		transparent 10em
	),
	radial-gradient(
		circle at bottom right,
		transparent 0,
		transparent 2em,
		palegoldenrod 2em,
		palegoldenrod 4em,
		transparent 4em,
		transparent 6em,
		peachpuff 6em,
		peachpuff 8em,
		transparent 8em,
		transparent 10em
	), blanchedalmond;
	
background-blend-mode: multiply;
background-size: 10em 10em;
background-position: 0 0, 0 0, 5em 5em, 5em 5em;
}
.cover_template_04{
	background:
	radial-gradient(
		circle at left,
		transparent,
		#99eb47,
		#99eb47 3.36927%,
		transparent 3.36927%,
		transparent 6.73854%,
		#b3e87d 6.73854%,
		#b3e87d 10.10782%,
		transparent 10.10782%,
		transparent 13.47709%,
		#ccebad 13.47709%,
		#ccebad 16.84636%,
		transparent 16.84636%,
		transparent 20.21563%,
		#a6ed5e 20.21563%,
		#a6ed5e 23.58491%,
		transparent 23.58491%,
		transparent 26.95418%,
		#ccebad 26.95418%,
		#ccebad 30.32345%,
		transparent 30.32345%,
		transparent 33.69272%,
		#b3e87d 33.69272%,
		#b3e87d 37.06199%,
		transparent 37.06199%,
		transparent 40.43127%,
		#99eb47 40.43127%,
		#99eb47 43.80054%,
		transparent 43.80054%,
		transparent 47.16981%
	),
	radial-gradient(
		circle at right,
		transparent,
		#99eb47 0%,
		#99eb47 3.36927%,
		transparent 3.36927%,
		transparent 6.73854%,
		#b3e87d 6.73854%,
		#b3e87d 10.10782%,
		transparent 10.10782%,
		transparent 13.47709%,
		#ccebad 13.47709%,
		#ccebad 16.84636%,
		transparent 16.84636%,
		transparent 20.21563%,
		#a6ed5e 20.21563%,
		#a6ed5e 23.58491%,
		transparent 23.58491%,
		transparent 26.95418%,
		#ccebad 26.95418%,
		#ccebad 30.32345%,
		transparent 30.32345%,
		transparent 33.69272%,
		#b3e87d 33.69272%,
		#b3e87d 37.06199%,
		transparent 37.06199%,
		transparent 40.43127%,
		#99eb47 40.43127%,
		#99eb47 43.80054%,
		transparent 43.80054%,
		transparent 47.16981%
	),
	radial-gradient(circle at left,
		transparent,
		#99eb47 0%,
		#99eb47 3.36927%,
		transparent 3.36927%,
		transparent 6.73854%,
		#b3e87d 6.73854%,
		#b3e87d 10.10782%,
		transparent 10.10782%,
		transparent 13.47709%,
		#ccebad 13.47709%,
		#ccebad 16.84636%,
		transparent 16.84636%,
		transparent 20.21563%,
		#a6ed5e 20.21563%,
		#a6ed5e 23.58491%,
		transparent 23.58491%,
		transparent 26.95418%,
		#ccebad 26.95418%,
		#ccebad 30.32345%,
		transparent 30.32345%,
		transparent 33.69272%,
		#b3e87d 33.69272%,
		#b3e87d 37.06199%,
		transparent 37.06199%,
		transparent 40.43127%,
		#99eb47 40.43127%,
		#99eb47 43.80054%,
		transparent 43.80054%,
		transparent 47.16981%
	),
	radial-gradient(circle at right,
		transparent,
		#99eb47 0%,
		#99eb47 3.36927%,
		transparent 3.36927%,
		transparent 6.73854%,
		#b3e87d 6.73854%,
		#b3e87d 10.10782%,
		transparent 10.10782%,
		transparent 13.47709%,
		#ccebad 13.47709%,
		#ccebad 16.84636%,
		transparent 16.84636%,
		transparent 20.21563%,
		#a6ed5e 20.21563%,
		#a6ed5e 23.58491%,
		transparent 23.58491%,
		transparent 26.95418%,
		#ccebad 26.95418%,
		#ccebad 30.32345%,
		transparent 30.32345%,
		transparent 33.69272%,
		#b3e87d 33.69272%,
		#b3e87d 37.06199%,
		transparent 37.06199%,
		transparent 40.43127%,
		#99eb47 40.43127%,
		#99eb47 43.80054%,
		transparent 43.80054%,
		transparent 47.16981%
	), #99e052;

background-size: 4em 4em;
background-position:
	0 0,
	0 2em,
	2em 0,
	2em 2em;
background-blend-mode:
	overlay,
	overlay,
	normal,
	normal;
}
.cover_template_05{
	background:
	repeating-linear-gradient(
		45deg,
		transparent,
		transparent 1em,
		moccasin 0,
		moccasin 2em,
		transparent 0,
		transparent 3em,
		powderblue 0,
		powderblue 4em,
		transparent 0,
		transparent 5em,
		lavender 0,
		lavender 6em,
		transparent 0,
		transparent 7em,
		beige 0,
		beige 8em
	),
	repeating-linear-gradient(
		-45deg,
		transparent,
		transparent 1em,
		khaki 0,
		khaki 2em,
		transparent 0,
		transparent 3em,
		beige 0,
		beige 4em,
		transparent 0,
		transparent 5em,
		peachpuff 0,
		peachpuff 6em
	), whitesmoke;

background-blend-mode: multiply;
}
.cover_template_06{
background:
linear-gradient(135deg, var(--primary_color) 10px, var(--secondary_color) 11px, var(--secondary_color) 12px, transparent 12px, transparent 33px, var(--secondary_color) 33px, var(--secondary_color) 34px, transparent 34px),
linear-gradient(225deg, var(--primary_color) 10px, var(--secondary_color) 11px, var(--secondary_color) 12px, transparent 12px, transparent 33px, var(--secondary_color) 33px, var(--secondary_color) 34px, transparent 34px)0 32px;
background-color:var(--primary_color);
background-size: 32px 64px;
}
.cover_template_07{
background-color: var(--primary_color);
background-image:
repeating-linear-gradient(120deg, hsla(0, 0%, 100%, 0.2), rgba(255,255,255,.2) 1px, transparent 1px, transparent 45px),
repeating-linear-gradient(60deg, rgba(255,255,255,.2), rgba(255,255,255,.2) 1px, transparent 1px, transparent 45px),
linear-gradient(60deg, rgba(0,0,0,.2) 25%, transparent 25%, transparent 75%, rgba(0,0,0,.2) 75%, rgba(0,0,0,.2)),
linear-gradient(120deg, rgba(0,0,0,.2) 25%, transparent 25%, transparent 75%, rgba(0,0,0,.2) 75%, rgba(0,0,0,.2));
background-size: 52px 90px;
}
.cover_template_08{
background-color: var(--secondary_color);
background-size: 58px 58px;
background-position: 0px 2px, 4px 35px, 29px 31px, 33px 6px,
0px 36px, 4px 2px, 29px 6px, 33px 30px;
background-image:
linear-gradient(335deg, var(--primary_color) 23px, transparent 23px),
linear-gradient(155deg, var(--primary_color) 23px, transparent 23px),
linear-gradient(335deg, var(--primary_color) 23px, transparent 23px),
linear-gradient(155deg, var(--primary_color) 23px, transparent 23px),

linear-gradient(335deg, var(--primary_color) 10px, transparent 10px),
linear-gradient(155deg, var(--primary_color) 10px, transparent 10px),
linear-gradient(335deg, var(--primary_color) 10px, transparent 10px),
linear-gradient(155deg, var(--primary_color) 10px, transparent 10px);
}
.cover_template_09{
background:
radial-gradient(circle at 100% 50%, transparent 20%, var(--secondary_color) 21%, var(--secondary_color) 34%, transparent 35%, transparent),
radial-gradient(circle at 0% 50%, transparent 20%, var(--secondary_color) 21%, var(--secondary_color) 34%, transparent 35%, transparent) 0 -25px;
background-color: var(--primary_color);
background-size:37px 50px;
}
.cover_template_10{
background-color: var(--primary_color);
background-image: radial-gradient(closest-side, transparent 98%, rgba(0,0,0,.3) 99%),
radial-gradient(closest-side, transparent 98%, rgba(0,0,0,.3) 99%);
background-size:60px 60px;
background-position:0 0, 30px 30px;
}
.cover_template_11{
background-color:var(--primary_color);
background-image:
radial-gradient(circle at 100% 150%, var(--primary_color) 24%, var(--secondary_color) 24%, var(--secondary_color) 28%, var(--primary_color) 28%, var(--primary_color) 36%, var(--secondary_color) 36%, var(--secondary_color) 40%, transparent 40%, transparent),
radial-gradient(circle at 0    150%, var(--primary_color) 24%, var(--secondary_color) 24%, var(--secondary_color) 28%, var(--primary_color) 28%, var(--primary_color) 36%, var(--secondary_color) 36%, var(--secondary_color) 40%, transparent 40%, transparent),
radial-gradient(circle at 50%  100%, var(--secondary_color) 10%, var(--primary_color) 10%, var(--primary_color) 23%, var(--secondary_color) 23%, var(--secondary_color) 30%, var(--primary_color) 30%, var(--primary_color) 43%, var(--secondary_color) 43%, var(--secondary_color) 50%, var(--primary_color) 50%, var(--primary_color) 63%, var(--secondary_color) 63%, var(--secondary_color) 71%, transparent 71%, transparent),
radial-gradient(circle at 100% 50%, var(--secondary_color) 5%, var(--primary_color) 5%, var(--primary_color) 15%, var(--secondary_color) 15%, var(--secondary_color) 20%, var(--primary_color) 20%, var(--primary_color) 29%, var(--secondary_color) 29%, var(--secondary_color) 34%, var(--primary_color) 34%, var(--primary_color) 44%, var(--secondary_color) 44%, var(--secondary_color) 49%, transparent 49%, transparent),
radial-gradient(circle at 0    50%, var(--secondary_color) 5%, var(--primary_color) 5%, var(--primary_color) 15%, var(--secondary_color) 15%, var(--secondary_color) 20%, var(--primary_color) 20%, var(--primary_color) 29%, var(--secondary_color) 29%, var(--secondary_color) 34%, var(--primary_color) 34%, var(--primary_color) 44%, var(--secondary_color) 44%, var(--secondary_color) 49%, transparent 49%, transparent);
background-size: 100px 50px;
}
.cover_template_12{
background-color: var(--primary_color);
background-image: linear-gradient(45deg, var(--secondary_color) 25%, transparent 25%, transparent 75%, var(--secondary_color) 75%, var(--secondary_color)),
linear-gradient(45deg, var(--secondary_color) 25%, transparent 25%, transparent 75%, var(--secondary_color) 75%, var(--secondary_color));
background-size: 61px 61px;
background-position: 0 0, 30px 30px;
}
.cover_template_13{
background-color: var(--primary_color);
background-image: linear-gradient(45deg, var(--secondary_color) 25%, transparent 25%, transparent 75%, var(--secondary_color) 75%, var(--secondary_color)),
linear-gradient(-45deg, var(--secondary_color) 25%, transparent 25%, transparent 75%, var(--secondary_color) 75%, var(--secondary_color));
background-size: 50px 50px;
}
.cover_template_14{
background-color: var(--primary_color);
background-image: repeating-linear-gradient(transparent, transparent 50px, rgba(0,0,0,.4) 50px, rgba(0,0,0,.4) 53px, transparent 53px, transparent 63px, rgba(0,0,0,.4) 63px, rgba(0,0,0,.4) 66px, transparent 66px, transparent 116px, rgba(0,0,0,.5) 116px, rgba(0,0,0,.5) 166px, rgba(255,255,255,.2) 166px, rgba(255,255,255,.2) 169px, rgba(0,0,0,.5) 169px, rgba(0,0,0,.5) 179px, rgba(255,255,255,.2) 179px, rgba(255,255,255,.2) 182px, rgba(0,0,0,.5) 182px, rgba(0,0,0,.5) 232px, transparent 232px),
repeating-linear-gradient(270deg, transparent, transparent 50px, rgba(0,0,0,.4) 50px, rgba(0,0,0,.4) 53px, transparent 53px, transparent 63px, rgba(0,0,0,.4) 63px, rgba(0,0,0,.4) 66px, transparent 66px, transparent 116px, rgba(0,0,0,.5) 116px, rgba(0,0,0,.5) 166px, rgba(255,255,255,.2) 166px, rgba(255,255,255,.2) 169px, rgba(0,0,0,.5) 169px, rgba(0,0,0,.5) 179px, rgba(255,255,255,.2) 179px, rgba(255,255,255,.2) 182px, rgba(0,0,0,.5) 182px, rgba(0,0,0,.5) 232px, transparent 232px),
repeating-linear-gradient(125deg, transparent, transparent 2px, rgba(0,0,0,.2) 2px, rgba(0,0,0,.2) 3px, transparent 3px, transparent 5px, rgba(0,0,0,.2) 5px);
}
.cover_template_15{
background:
radial-gradient(circle farthest-side at 0% 50%,var(--primary_color) 23.5%,rgba(240,166,17,0) 0)21px 30px,
radial-gradient(circle farthest-side at 0% 50%,var(--secondary_color) 24%,rgba(240,166,17,0) 0)19px 30px,
linear-gradient(var(--primary_color) 14%,rgba(240,166,17,0) 0, rgba(240,166,17,0) 85%,var(--primary_color) 0)0 0,
linear-gradient(150deg,var(--primary_color) 24%,var(--secondary_color) 0,var(--secondary_color) 26%,rgba(240,166,17,0) 0,rgba(240,166,17,0) 74%,var(--secondary_color) 0,var(--secondary_color) 76%,var(--primary_color) 0)0 0,
linear-gradient(30deg,var(--primary_color) 24%,var(--secondary_color) 0,var(--secondary_color) 26%,rgba(240,166,17,0) 0,rgba(240,166,17,0) 74%,var(--secondary_color) 0,var(--secondary_color) 76%,var(--primary_color) 0)0 0,
linear-gradient(90deg,var(--secondary_color) 2%,var(--primary_color) 0,var(--primary_color) 98%,var(--secondary_color) 0%)0 0 var(--primary_color);
background-size: 40px 60px;
}
.cover_template_16{
background: linear-gradient(var(--primary_color) 50%, rgba(255,255,255,0) 0) 0 0,
radial-gradient(circle closest-side, var(--primary_color) 53%, rgba(255,255,255,0) 0) 0 0,
radial-gradient(circle closest-side, var(--primary_color) 50%, rgba(255,255,255,0) 0) 23px 0 var(--secondary_color);
background-size: 45px 90px;
background-repeat: repeat-x;
}
.cover_template_17{
background:
radial-gradient(circle at 0% 50%, rgba(96, 16, 48, 0) 9px, var(--secondary_color) 10px, rgba(96, 16, 48, 0) 11px) 0px 10px,
radial-gradient(at 100% 100%,rgba(96, 16, 48, 0) 9px, var(--secondary_color) 10px, rgba(96, 16, 48, 0) 11px),var(--primary_color);
background-size: 20px 20px;
}
.cover_template_18{
background:
linear-gradient(63deg, var(--primary_color) 23%, transparent 23%) 7px 0,
linear-gradient(63deg, transparent 74%, var(--primary_color) 78%),
linear-gradient(63deg, transparent 34%, var(--primary_color) 38%, var(--primary_color) 58%, transparent 62%),
var(--secondary_color);
background-size: 16px 48px;
}
.cover_template_19{
background: var(--primary_color);
background:
linear-gradient(115deg, transparent 75%, var(--secondary_color) 75%) 0 0,
linear-gradient(245deg, transparent 75%, var(--secondary_color) 75%) 0 0,
linear-gradient(115deg, transparent 75%, var(--secondary_color) 75%) 7px -15px,
linear-gradient(245deg, transparent 75%, var(--secondary_color) 75%) 7px -15px,
var(--primary_color);
background-size: 15px 30px;
}
.cover_template_20{
background:
linear-gradient(45deg, var(--secondary_color) 23px, transparent 23px)32px 32px,
linear-gradient(45deg, var(--secondary_color) 22px, transparent 22px,transparent 45px, var(--primary_color) 45px, var(--primary_color) 67px, transparent 67px),
linear-gradient(-45deg, var(--secondary_color) 10px, transparent 11px, transparent 34px,var(--secondary_color) 34px,var(--secondary_color) 56px,transparent 56px,transparent 79px,var(--secondary_color) 79px);
background-color:var(--primary_color);
background-size: 64px 64px;
}
.cover_template_21{
background:
linear-gradient(135deg, var(--secondary_color) 25%, transparent 25%) -15px 0,
linear-gradient(225deg, var(--secondary_color) 25%, transparent 25%) -15px 0,
linear-gradient(315deg, var(--secondary_color) 25%, transparent 25%),
linear-gradient(45deg, var(--secondary_color) 25%, transparent 25%);
background-size: 30px 30px;
background-color: var(--primary_color);
}
</style>