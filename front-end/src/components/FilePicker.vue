<template>
  <form class="file-picker" ref="form">
    <div ref="fileDropArea" class="drop-area has-not-image" v-on:drop="fileDropped">
      <label for="filePickerInput">
          <span v-if="!hasFile">
            Click or drop a file...
          </span>
          <span v-else>
            {{fileInfo}}
          </span>
      </label>
      <input type="file" id="filePickerInput" name="file" v-on:change="fileDropped" ref="filePickerInput">
    </div>
    <v-btn color="primary" v-on:click="submit" flat>Classify</v-btn>
    <slot></slot>
  </form>

</template>

<script>
import $ from "jquery";
export default {
  name: "file-picker",
  props: ["onFileChanged", "upload"],
  data: () => {
    isAdvancedPicker;
    let div = document.createElement("div");
    const isAdvancedPicker =
      ("draggable" in div || ("ondragstart" in div && "ondrop" in div)) &&
      "FormData" in window &&
      "FileReader" in window;

    return {
      file: null,
      isAdvancedPicker: isAdvancedPicker
    };
  },
  methods: {
    submit() {
      if (this.upload) {
        this.upload(this.file);
      }
    },

    fileDropped(e) {
      let files = e.target.files || e.dataTransfer.files;
      this.$refs.filePickerInput.files = files;
      if (files && files.length) {
        this.file = files[0];
        $(this.$refs.fileDropArea).css(
          "background-image",
          "url('" + URL.createObjectURL(this.file) + "')"
        );
        $(this.$refs.fileDropArea).removeClass("has-not-image");
      } else {
        this.file = null;
        $(this.$refs.fileDropArea).css("background-image", "");
        $(this.$refs.fileDropArea).addClass("has-not-image");
      }
      if (this.onFileChanged) {
        this.onFileChanged(this.file);
      }
    }
  },
  computed: {
    hasFile() {
      return this.file != null;
    },
    fileInfo() {
      return this.file ? this.file.name : null;
    }
  },
  mounted() {
    $(this.$refs.form).on("submit", e => {
      e.preventDefault();
      e.stopPropagation();
    });
    $(this.$refs.fileDropArea)
      .on("dragenter dragover dragleave drop", e => {
        e.preventDefault();
        e.stopPropagation();
      })
      .on("dragenter", () => {
        $(this.$refs.fileDropArea).addClass("drag-entered");
      })
      .on("dragleave", () => {
        $(this.$refs.fileDropArea).removeClass("drag-entered");
      })
      .on("drop", () => {
        $(this.$refs.fileDropArea).removeClass("drag-entered");
      })
      .on("click", () => {
        this.$refs.filePickerInput.click();
      });
  }
};
</script>

<style>
input[type="file"] {
  display: none;
}
.file-picker {
  border: 2px rgb(0, 0, 0, 0.6) dashed;
  border-radius: 10px;
  opacity: 0.7;
  text-align: center;
  max-height: 30vh;
  min-height: 150px;
  background-color: rgb(52, 126, 245);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: 0.5s;
  overflow: hidden;
  /* animation: opacityAnim 1s infinite alternate-reverse; */
}
.file-picker:hover {
  opacity: 1;
}
@keyframes opacityAnim {
  from {
    opacity: 0.7;
  }
  to {
    opacity: 0.9;
  }
}
.has-not-image.drop-area:hover,
.drag-entered {
  transition: 0.5s;
  background: repeating-linear-gradient(
    45deg,
    rgb(175, 219, 255),
    rgb(175, 219, 255) 30px,
    rgb(52, 126, 245) 30px,
    rgba(52, 126, 245) 60px
  );
  /* animation: moveBackground 3s infinite; */
  opacity: 1;
}

.drop-area {
  flex-grow: 1;
  transition: 0.5s;
  padding: 30px;
  cursor: pointer;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center center;
}

.drop-area label {
  font-size: 2em;
  pointer-events: none;
}

@keyframes moveBackground {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>
