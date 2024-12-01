<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Username:</label>
        <input v-model="username" id="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p>
      No account?
      <router-link to="/register">Register</router-link>
    </p>
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
    handleLogin() {
      // 检查用户是否存在
      const registeredUser = JSON.parse(localStorage.getItem("user"));
      if (
        registeredUser &&
        registeredUser.username === this.username &&
        registeredUser.password === this.password
      ) {
        alert("Login successful!");
      } else {
        alert("Invalid username or password");
      }
    },
  },
};
</script>

<style scoped>
/* 样式设置略 */
</style>
