<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="username">Username:</label>
        <input v-model="username" id="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleRegister() {
      // 模拟用户数据保存
      const user = { username: this.username, password: this.password };
      localStorage.setItem("user", JSON.stringify(user));
      console.log("Registered User:", user);

      // 跳转到登录页面
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
/* 样式设置略 */
</style>
