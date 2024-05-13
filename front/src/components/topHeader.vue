<template>
    <div id="top-header">
      <dv-decoration-8 class="header-left-decoration" />
      <dv-decoration-5 :dur="10" class="header-center-decoration" />
      <dv-decoration-8 class="header-right-decoration" :reverse="true" />
      <div class="center-title">多变量招聘数据可视分析</div>
    </div>
</template>

<script>
export default {
    name: 'TopHeader'
}
</script>

<style lang="css">
#top-header {
    position: relative;
    width: 100%;
    height: 100px;
    display: flex;
    justify-content: space-between;
    flex-shrink: 0;
}

#top-header .header-center-decoration {
    width: 40%;
    height: 60px;
    margin-top: 30px;
}

#top-header .header-left-decoration,
#top-header .header-right-decoration {
    width: 25%;
    height: 60px;
}

#top-header .center-title {
    position: absolute;
    font-size: 30px;
    font-weight: bold;
    left: 50%;
    top: 15px;
    transform: translateX(-50%);
}
</style>