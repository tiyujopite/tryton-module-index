<script setup>
</script>

<template>
  <header class="header pt-8 text-center font-bold text-white">
    <img src="../assets/logo.svg" alt="logo" class="w-full max-w-4xl mx-auto">
    <nav class="flex gap-4 justify-center py-4">
      <a @click="$router.push('/home')">HOME</a>
      <a @click="$router.push('/modules')">MODULES</a>
    </nav>
  </header>
</template>

<style scoped>
.header {
  background-color: var(--bg-color);
}
nav > a {
  text-decoration: none;
  color: white;
}
a:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
