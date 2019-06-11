<template>
  <div id="app">
    <div class="file-upload-site">
      <file-picker :upload="classifyImage">
        <div class="loader-container">
          <div class="loader"></div>
        </div>
      </file-picker>
      <result-presenter :result="resultOfClassification"></result-presenter>
    </div>
    <div class="statistics-data">
      <div class="app-title">Most frequently returned results</div>
      <hr/>
      <apexchart type=bar :options="chartOptions" :series="chartSeries" />
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
import ResultPresenter from "./components/ResultPresenter";
import $ from "jquery";
import config from "./config.js";
import Vue from "vue";
import apexchart from "vue-apexcharts";

export default {
  name: "app",
  components: {
    FilePicker,
    ImageGallery,
    ResultPresenter,
    apexchart
  },
  data() {
    return {
      toastedOptions: {
        position: "top-center",
        containerClass: "text-center",
        duration: 3000
      },
      chartSeries: [
        {
          name: "Number of classifications",
          data: []
        }
      ],
      chartOptions: {
        plotOptions: {
          bar: { horizontal: true }
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          categories: []
        }
      },
      resultOfClassification: {
        labels: []
      },
      images: []
    };
  },
  mounted() {
    $(".to-content-arrow").on("click", function(e) {
      $("html, body").animate(
        {
          scrollTop: parseInt($("#app").offset().top)
        },
        1000
      );
    });

    $.ajax({
      url: config.GET_PAGE_DATA_URL,
      type: "GET",
      data: {
        topLabelsCount: 10,
        imageCount: 20
      }
    })
      .done((data, status) => {
        var lables = [];
        var values = [];
        if (data && data.labels && data.labels.length) {
          for (let i = 0; i < data.labels.length; i++) {
            const element = data.labels[i];
            values.push(element.count);
            lables.push(element.label);
          }
          this.chartOptions = {
            plotOptions: {
              bar: { horizontal: true }
            },
            dataLabels: {
              enabled: false
            },
            xaxis: {
              categories: lables
            }
          };
          this.chartSeries = [{ data: values }];
        }
        var images = [];
        if (data && data.images && data.images.length) {
          for (let index = 0; index < data.images.length; index++) {
            const element = data.images[index];
            images.push({
              src:
                config.S3_URL + element.bucketName + "/" + element.imgLocation,
              labels: element.labels
            });
          }
        }
        this.images = images;
      })
      .fail(this.onRequestFail)
      .always(this.always);
  },
  methods: {
    setLoader(isLoading) {
      if (isLoading) {
        $(".loader-container").addClass("request-inprogress");
      } else {
        $(".loader-container").removeClass("request-inprogress");
      }
    },
    onRequestFail(error) {
      console.error(error);
      Vue.toasted.error("Error : " + error.message, this.toastedOptions);
    },
    always() {
      this.setLoader(false);
    },
    classifyImage(file) {
      console.log(file);
      if (!file) {
        return;
      }
      this.resultOfClassification = { labels: [] };
      this.setLoader(true);
      var reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        console.log("reader.result");
        $.ajax({
          type: "POST",
          url: config.CLASSIFY_IMG_URL,
          contentType: "application/json; charset=utf-8",
          dataType: "json",
          data: JSON.stringify({
            filename: file.name,
            contenttype: file.type,
            imagedata: reader.result.replace(/^data:(.*;base64,)?/, "")
          })
        })
          .done((data, status) => {
            this.resultOfClassification.labels = data;
            Vue.toasted.success(
              "Success : found " +
                this.resultOfClassification.labels.length +
                " labels",
              this.toastedOptions
            );
          })
          .fail(this.onRequestFail)
          .always(this.always);
      };
      reader.onerror = error => {
        console.log("Error: ", error);
      };
    }
  }
};
</script>

<style>
.text-center {
  padding: 20px;
}
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
  position: relative;
  grid-area: fileSite;
  padding: 0 20px;
}
.file-picker {
  min-width: 400px;
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

.request-inprogress {
  display: block !important;
}

.loader-container {
  display: none;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  padding-top: 10px;
}

.loader {
  border: 16px solid #f3f3f3;
  border-radius: 50%;
  border-top: 16px solid blue;
  border-bottom: 16px solid blue;
  width: 60px;
  height: 60px;
  -webkit-animation: spin 2s linear infinite;
  animation: spin 2s linear infinite;
}

@-webkit-keyframes spin {
  0% {
    -webkit-transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
