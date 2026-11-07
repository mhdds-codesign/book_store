<template>
  <div id="app-shell" :class="{ 'no-sidebar': !loggedIn }">
    <!-- Sidebar (Only shown when logged in) -->
    <aside class="app-sidebar" v-if="loggedIn">
      <div>
        <router-link to="/" class="sidebar-brand">
          <div class="sidebar-brand-icon">
            <i class="fas fa-book-open"></i>
          </div>
          <div class="sidebar-brand-title">OrbitBook</div>
          <div class="sidebar-brand-subtitle">Shop Manager</div>
        </router-link>

        <ul class="sidebar-menu">
          <li class="sidebar-menu-item">
            <router-link to="/">
              <i class="fas fa-house"></i>
              <span>داشبورد</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/products">
              <i class="fas fa-box"></i>
              <span>محصولات</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/categories">
              <i class="fas fa-shapes"></i>
              <span>دسته‌بندی‌ها</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/customers">
              <i class="fas fa-users"></i>
              <span>مشتریان</span>
            </router-link>
          </li>
          <li class="sidebar-menu-item">
            <router-link to="/orders">
              <i class="fas fa-cart-shopping"></i>
              <span>سفارش‌ها</span>
            </router-link>
          </li>
          <!-- Note: Income/Revenue (درآمد) excluded per user explicit request -->
          <li class="sidebar-menu-item">
            <button type="button" @click="showSettings = true">
              <i class="fas fa-sliders"></i>
              <span>تنظیمات</span>
            </button>
          </li>
          <li class="sidebar-menu-item">
            <button type="button" @click="doLogout" style="color: #fda4af;">
              <i class="fas fa-power-off"></i>
              <span>خروج از حساب</span>
            </button>
          </li>
        </ul>
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
      showSettings: false
    }
  },
  async created() {
    await this.checkAuth()
  },
  watch: {
    $route() {
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
