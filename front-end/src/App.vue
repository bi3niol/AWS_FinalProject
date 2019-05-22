<template>
  <div id="app">
    <div class="file-upload-site">
      <file-picker :upload="classifyImage"></file-picker>
    </div>
    <div class="statistics-data">
      <div class="app-title">Most frequently returned results</div>
      <hr/>
      <bar-chart
        :chart-data="chartData">
      </bar-chart>
    </div>
    <div class="last-classified-images">
      <span class="app-title">Last classified images</span>
      <hr/>
      <image-gallery :images="images"></image-gallery>
    </div>
  </div>
</template>

<script>
import FilePicker from "./components/FilePicker";
import ImageGallery from "./components/ImageGallery";
import BarChart from "./components/BarChart";
import $ from "jquery";

export default {
  name: "app",
  components: { FilePicker, ImageGallery, BarChart },
  data() {
    return {
      chartData: null,
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
  mounted() {
    this.chartData = {
      labels: [
        "test1",
        "test2",
        "test3",
        "test4",
        "test5",
        "test6",
        "test7",
        "test8",
        "test9"
      ],
      datasets: [
        {
          label: "class count",
          backgroundColor: "rgb(52, 126, 245)",
          data: [12, 23, 4, 17, 15, 1, 9, 5, 20]
        }
      ]
    };
  },
  methods: {
    classifyImage(file) {
      console.log(file);
      if (!file) {
        return;
      }
      var reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        console.log("reader.result");
        $.ajax({
          type: "POST",
          url:
            "https://0oanfqjnbg.execute-api.us-east-1.amazonaws.com/chmury/classifyimage",
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          data: JSON.stringify({
            filename: file.name,
            contenttype: file.type,
            imagedata: reader.result.replace(/^data:(.*;base64,)?/, "")
          }),
          success: (data, status) => {
            console.log(data);
            console.log(status);
          }
        });
      };
      reader.onerror = error => {
        console.log("Error: ", error);
      };
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

.statistics-data {
  max-width: 700px;
  max-height: 600px;
  text-align: center;
  margin: 0 auto;
  padding-top: 20px;
  grid-area: statisticsData;
}

@media only screen and (min-width: 700px) {
  #app {
    padding-top: 50px;
    grid-template:
      "fileSite statisticsData statisticsData"
      "imageGalery imageGalery imageGalery";
  }
}
.statistics-data > span {
  font-size: 2rem;
}
.file-upload-site {
  grid-area: fileSite;
  min-width: 400px;
  padding: 0 20px;
}
.statistics-data,
.last-classified-images {
  transition: 0.5s;
  opacity: 0.7;
}
.statistics-data:hover,
.last-classified-images:hover {
  opacity: 1;
}
.last-classified-images {
  padding-top: 20px;
  text-align: center;
  grid-area: imageGalery;
}
.app-title {
  font-size: 2rem;
  letter-spacing: 5px;
  pointer-events: none;
}
</style>
