<template>
  <div>
    <GroupNavbar v-if="$q.platform.is.mobile && showGroupNavbar" />
    <router-view/>
  </div>
</template>

<script>
import GroupNavbar from '@/components/Group/Navbar'
export default {
  components: { GroupNavbar },
  computed: {
    showGroupNavbar () {
      // quick hack to discover all routes where group navbar should be shown
      return this.$route.name.startsWith('group')
    },
  },
}
</script>

<style scoped lang="stylus">
</style>
