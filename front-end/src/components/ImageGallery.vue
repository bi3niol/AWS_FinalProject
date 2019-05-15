<template>
<div>
    <div class="images">
        <div class="image" v-for="(src,id) in images" :key="id" @click="()=>show(id)">
            <div>
                <img :src="src"/>
            </div>
        </div>
    </div>
    <vue-easy-lightbox
        :visible="visible"
        :imgs="images"
        :index="index"
        @hide="handleHide"
      ></vue-easy-lightbox>
</div>
</template>

<script>
export default {
  name: "image-gallery",
  props: ["images"],
  data() {
    return {
      index: 0,
      visible: false
    };
  },
  methods: {
    handleHide() {
      this.visible = false;
    },
    show(index) {
      this.index = index;
      this.visible = true;
    }
  }
};
</script>
<style>
.images {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: top;
}
.image div {
  margin: 10px;
}
.image img {
  cursor: pointer;
  display: block;
  transition: 0.25s;
  box-shadow: 0 0 5px 0px black;
  max-width: 200px;
  max-height: 200px;
  opacity: 0.7;
}
.image img:hover {
  /* transform: rotateZ(10deg); */
  margin: -5px;
  opacity: 1;
  box-shadow: 0 0 10px 0px black;
}
</style>
