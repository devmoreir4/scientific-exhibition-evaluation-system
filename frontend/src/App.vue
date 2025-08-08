<script setup>
</script>

<template>
  <router-view />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  background: #f5f6fa;
  font-family: 'Segoe UI', Arial, sans-serif;
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

div, section, article, aside, header, footer, nav, main {
  box-sizing: border-box;
}

table {
  border-collapse: collapse;
  border-spacing: 0;
}

img {
  max-width: 100%;
  height: auto;
}

button, input, textarea, select {
  font-family: inherit;
  font-size: inherit;
}
</style>
