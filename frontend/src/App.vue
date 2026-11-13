<template>
  <div id="app-shell" :class="{ 'no-sidebar': !loggedIn }">
    <!-- Mobile Navigation Bar (Visible on mobile/tablet) -->
    <header class="mobile-navbar" v-if="loggedIn">
      <button class="mobile-menu-toggle" @click="sidebarOpen = !sidebarOpen" aria-label="باز کردن منو">
        <i class="fas fa-bars"></i>
      </button>

      <router-link to="/" class="mobile-brand">
        <div class="mobile-brand-icon">
          <i class="fas fa-book-open"></i>
        </div>
        <div class="mobile-brand-text">
          <span class="mobile-brand-title">OrbitBook</span>
          <span class="mobile-brand-subtitle">Shop Manager</span>
        </div>
      </router-link>

      <button class="mobile-settings-btn" @click="showSettings = true" aria-label="تنظیمات">
        <i class="fas fa-sliders"></i>
      </button>
    </header>

    <!-- Mobile Drawer Backdrop Overlay -->
    <div
      class="sidebar-backdrop"
      v-if="loggedIn && sidebarOpen"
      @click="sidebarOpen = false"
    ></div>

    <!-- Sidebar Navigation -->
    <aside
      class="app-sidebar"
      :class="{ 'sidebar-open': sidebarOpen }"
      v-if="loggedIn"
    >
      <div>
        <div class="sidebar-header-row">
          <router-link to="/" class="sidebar-brand" @click="sidebarOpen = false">
            <div class="sidebar-brand-icon">
              <i class="fas fa-book-open"></i>
            </div>
            <div class="sidebar-brand-title">OrbitBook</div>
            <div class="sidebar-brand-subtitle">Shop Manager</div>
          </router-link>

          <!-- Mobile Close Button -->
          <button class="sidebar-mobile-close" @click="sidebarOpen = false" aria-label="بستن منو">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <ul class="sidebar-menu">
          <li class="sidebar-menu-item">
            <router-link to="/" @click="sidebarOpen = false">
              <i class="fas fa-house"></i>
              <span>داشبورد</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/products" @click="sidebarOpen = false">
              <i class="fas fa-box"></i>
              <span>محصولات</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/categories" @click="sidebarOpen = false">
              <i class="fas fa-shapes"></i>
              <span>دسته‌بندی‌ها</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/customers" @click="sidebarOpen = false">
              <i class="fas fa-users"></i>
              <span>مشتریان</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/orders" @click="sidebarOpen = false">
              <i class="fas fa-cart-shopping"></i>
              <span>سفارش‌ها</span>
            </router-link>
          </li>
          <!-- Note: Income/Revenue (درآمد) excluded per user explicit request -->
          <li class="sidebar-menu-item">
            <button type="button" @click="showSettings = true; sidebarOpen = false">
              <i class="fas fa-sliders"></i>
              <span>تنظیمات</span>
            </button>
          </li>
          <li class="sidebar-menu-item">
            <button type="button" @click="doLogout(); sidebarOpen = false" style="color: #fda4af;">
              <i class="fas fa-power-off"></i>
              <span>خروج از حساب</span>
            </button>
          </li>
        </ul>
      </div>

      <!-- Bottom Book Stack Artwork from Design -->
      <div class="sidebar-footer">
        <img src="/assets/books_sidebar.png" alt="OrbitBook 3D Books" class="sidebar-books-img" />
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="app-main">
      <router-view />
    </main>

    <!-- Settings Modal -->
    <div class="modal-overlay" v-if="showSettings" @click.self="showSettings = false">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3><i class="fas fa-sliders" style="color:#0d9488; margin-left:0.5rem;"></i> تنظیمات سامانه کتابفروشی</h3>
          <button class="modal-close" @click="showSettings = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>نام فروشگاه</label>
            <input type="text" value="فروشگاه آنلاین کتاب OrbitBook" readonly />
          </div>
          <div class="form-group">
            <label>واحد پولی سامانه</label>
            <input type="text" value="تومان (IRR / Toman)" readonly style="font-weight:700; color:#0d9488;" />
          </div>
          <div class="form-group">
            <label>کاربر جاری</label>
            <input type="text" value="مدیر سیستم (admin)" readonly />
          </div>
          <div class="form-group">
            <label>مرتب‌سازی نام</label>
            <input type="text" value="الفبای فارسی استاندارد (آ تا ی)" readonly />
          </div>
          <div style="text-align:left; margin-top:1.5rem;">
            <button class="btn-orbit-primary" @click="showSettings = false">بستن</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from './api.js'

export default {
  data() {
    return {
      loggedIn: false,
      showSettings: false,
      sidebarOpen: false
    }
  },
  async created() {
    await this.checkAuth()
  },
  watch: {
    $route() {
      this.sidebarOpen = false
      this.checkAuth()
    }
  },
  methods: {
    async checkAuth() {
      try {
        await api.me()
        this.loggedIn = true
      } catch {
        this.loggedIn = false
      }
    },
    async doLogout() {
      try {
        await api.logout()
      } catch (e) {
        console.error(e)
      }
      this.loggedIn = false
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.no-sidebar .app-main {
  padding: 0;
}
</style>
