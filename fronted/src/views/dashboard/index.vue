<template>
  <div class="dashboard-container" style="height: 800px">
    <div class="dashboard-text">欢迎: {{ name }} ~</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
.dashboard-text {
    margin: 0;
    margin: 0;
    font-family: 'Times New Roman', Times, serif;
    color: #070707;
    text-align: center;
}
</style>
