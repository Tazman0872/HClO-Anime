<template>
  <div class="about-container">
    <h1 class="main-title">关于</h1>
    <p class="description">
      这是一个由
      <a
        href="mailto:Tazman_0872@hypochlorous.top"
        class="email-link"
        title="点击发送邮件"
      >
        Tazman_0872@hypochlorous.top
      </a>
      制作的自动追番工具，旨在打通自动追番最后一公里。
    </p>
  </div>
</template>

<script setup>
// 无逻辑，纯展示组件
</script>

<style scoped>
.about-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1.5rem;
  text-align: center;
  font-family: system-ui, sans-serif;
  background-color: var(--sidebar-bg);
  color: var(--text);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: background-color 0.3s, color 0.3s;
}

.main-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  color: var(--text);
}

.description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--text);
}

.email-link {
  color: var(--hover);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease, text-decoration 0.2s ease;
}

.email-link:hover {
  text-decoration: underline;
}

@media (max-width: 600px) {
  .about-container {
    padding: 1.25rem;
    margin: 1rem;
  }

  .main-title {
    font-size: 1.75rem;
  }

  .description {
    font-size: 1rem;
  }
}
</style>