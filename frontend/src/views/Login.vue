<template>
  <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #092834 0%, #051b23 100%); padding: 1.5rem;">
    <div style="background: #ffffff; border-radius: 24px; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35); max-width: 420px; width: 100%; padding: 2.5rem 2rem; text-align: center; position: relative;">
      
      <!-- Brand Logo -->
      <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #06b6d4 0%, #10b981 100%); border-radius: 18px; margin: 0 auto 1rem auto; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.8rem; box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);">
        <i class="fas fa-book-open"></i>
      </div>
      <h2 style="font-size: 1.6rem; font-weight: 800; color: #0c3b4a; margin-bottom: 0.25rem;">OrbitBook</h2>
      <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.75rem;">سامانه مدیریت هوشمند کتابفروشی</p>

      <div v-if="error" class="alert-error" style="text-align: right;">
        <i class="fas fa-circle-exclamation"></i>
        <span>{{ error }}</span>
      </div>

      <form @submit.prevent="doLogin" style="text-align: right;">
        <div class="form-group">
          <label><i class="fas fa-user" style="color:#0d9488; margin-left:0.3rem;"></i> نام کاربری مدیر</label>
          <input
            v-model="username"
            type="text"
            required
            autofocus
            placeholder="admin"
          />
        </div>

        <div class="form-group">
          <label><i class="fas fa-key" style="color:#0d9488; margin-left:0.3rem;"></i> رمز عبور</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="*********"
          />
        </div>

        <button
          type="submit"
          class="btn-orbit-primary"
          style="width: 100%; justify-content: center; padding: 0.8rem; margin-top: 1rem; border-radius: 14px;"
          :disabled="loading"
        >
          <i class="fas fa-right-to-bracket" v-if="!loading"></i>
          <i class="fas fa-spinner fa-spin" v-else></i>
          <span>{{ loading ? 'در حال ورود...' : 'ورود به سامانه' }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
      loading: false
    }
  },
  methods: {
    async doLogin() {
      this.loading = true
      this.error = null
      try {
        await api.login(this.username, this.password)
        this.$router.push('/')
      } catch (e) {
        this.error = 'نام کاربری یا رمز عبور اشتباه است.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
