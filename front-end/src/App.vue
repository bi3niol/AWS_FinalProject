<template>
  <div id="app">
    <div class="file-upload-site">sd</div>
    <div class="statistics-data">d</div>
    <div class="last-classified-images">s</div>
  </div>
</template>

<script>
export default {
  name: "app",
  components: {}
};
</script>

<style>
#app {
  position: sticky;
  background: white;
  top: 0;
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: grid;
  min-height: 100vh;
  height: 200vh;
  margin-bottom: -60px;
  grid-template:
    "fileSite statisticsData statisticsData"
    "imageGalery imageGalery imageGalery";
  grid-gap: 10px;
}
@media only screen and (max-width: 700px) {
  #app {
    grid-template:
      "fileSite"
      "statisticsData"
      "imageGalery";
  }
}
.file-upload-site,
.statistics-data,
.last-classified-images {
}
.file-upload-site {
  background-color: aqua;
  grid-area: fileSite;
}
.statistics-data {
  background-color: brown;
  grid-area: statisticsData;
}
.last-classified-images {
  background-color: blue;
  grid-area: imageGalery;
}
</style>
