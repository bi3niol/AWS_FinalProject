<template>
    <div class="presenter">
        <div class="item" :class="indx%2==0?'blue-bc-theme-inverse':'blue-bc-theme'" v-for="(label, indx) in result.labels" :key="label.Name">
            <span>{{label.Name}}</span>
            <span>{{Number(label.Confidence).toFixed(2)}}</span>
        </div>
    </div>
</template>

<script>
export default { name: "result-presenter", props: ["result"] };
</script>

<style>
.presenter {
  width: 100%;
}
.item {
  display: flex;
  justify-content: space-around;
  margin: 10px 0;
  padding: 15px;
}
/* .item span {
  display: block;
} */
</style>

 