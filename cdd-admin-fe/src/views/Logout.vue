<template>
  <div></div>
</template>

<script>
import user from '../localStorage/user'

export default {
  name: 'Logout',
  created () {
    user.logout()
    this.$router.push({ name: 'Login' })
  }
}
</script>
