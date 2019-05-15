<template>
  <div id="app">
    <div class="file-upload-site">
      <file-picker :upload="checkImage"></file-picker>
    </div>
    <div class="statistics-data">d</div>
    <div class="last-classified-images">
      <hr/>
      <span class="app-title">Last classified images</span>
      <hr/>
      <image-gallery :images="images"></image-gallery>
    </div>
  </div>
</template>

<script>
import FilePicker from "./components/FilePicker";
import ImageGallery from "./components/ImageGallery";
export default {
  name: "app",
  components: { FilePicker, ImageGallery },
  data() {
    return {
      images: [
        "https://via.placeholder.com/450.png/",
        "https://via.placeholder.com/250x400.png/",
        "https://via.placeholder.com/300.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/250x400.png/",
        "https://via.placeholder.com/450.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/450.png/",
        "https://via.placeholder.com/300.png/",
        "https://via.placeholder.com/300.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/450.png/",
        "https://via.placeholder.com/150.png/",
        "https://via.placeholder.com/300.png/",
        "https://via.placeholder.com/250x400.png/",
        "https://via.placeholder.com/250x400.png/",
        "https://via.placeholder.com/150.png/"
      ]
    };
  },
  methods: {
    checkImage(file) {
      console.log(file);
    }
  }
};
</script>

<style>
#app {
  position: relative;
  background: white;
  top: 0;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: grid;
  min-height: 100vh;
  /* margin-bottom: -60px; */
  padding-top: 20px;
  grid-template:
    "fileSite"
    "statisticsData"
    "imageGalery";
}
@media only screen and (min-width: 700px) {
  #app {
    padding-top: 50px;
    grid-template:
      "fileSite statisticsData statisticsData"
      "imageGalery imageGalery imageGalery";
  }
}

.file-upload-site {
  grid-area: fileSite;
  padding: 0 20px;
}
.statistics-data {
  background-color: brown;
  grid-area: statisticsData;
}
.last-classified-images {
  padding-top: 20px;
  text-align: center;
  grid-area: imageGalery;
}
.app-title {
  font-size: 2rem;
  letter-spacing: 5px;
  display: block;
  background-color: rgb(177, 177, 177);
}
</style>
