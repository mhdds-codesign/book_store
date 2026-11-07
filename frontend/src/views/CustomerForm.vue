<template>
  <div>
    <div class="page-top-bar">
      <div class="page-title">
        <i :class="isEdit ? 'fas fa-user-pen' : 'fas fa-user-plus'"></i>
        <span>{{ isEdit ? 'ویرایش اطلاعات مشتری' : 'افزودن مشتری جدید' }}</span>
      </div>
      <div class="page-actions">
        <router-link to="/customers" class="btn-orbit-secondary">
          <i class="fas fa-arrow-right"></i>
          <span>بازگشت به لیست مشتریان</span>
        </router-link>
      </div>
    </div>

    <div class="form-card">
      <div v-if="error" class="alert-error">
        <i class="fas fa-triangle-exclamation"></i>
        <span>{{ error }}</span>
      </div>

      <form @submit.prevent="doSave">
        <div class="form-group">
          <label>نام و نام خانوادگی (فارسی یا انگلیسی)</label>
          <input
            v-model="form.name"
            required
            placeholder="مثال: سارا احمدی یا آلیس جانسون"
          />
        </div>

        <div class="form-group">
          <label>آدرس ایمیل</label>
          <input
            v-model="form.email"
            type="email"
            required
            style="direction:ltr; text-align:right;"
            placeholder="example@mail.com"
          />
        </div>

        <div class="form-group">
          <label>شماره تماس</label>
          <input
            v-model="form.phone"
            style="direction:ltr; text-align:right;"
            placeholder="۰۹۱۲-۱۲۳۴۵۶۷"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-orbit-primary" :disabled="saving">
            <i class="fas fa-floppy-disk"></i>
            <span>{{ saving ? 'در حال ذخیره‌سازی...' : (isEdit ? 'بروزرسانی مشتری' : 'ثبت مشتری') }}</span>
          </button>
          <router-link to="/customers" class="btn-orbit-secondary">
            انصراف
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      isEdit: false,
      saving: false,
      error: null,
      form: {
        name: '',
        email: '',
        phone: ''
      }
    }
  },
  async created() {
    const id = this.$route.params.id
    this.isEdit = !!id

    if (id) {
      try {
        const res = await api.customers({ per_page: 100 })
        const c = (res.customers || []).find(x => x.id == id)
        if (c) {
          this.form = {
            name: c.name,
            email: c.email,
            phone: c.phone || ''
          }
        }
      } catch (e) {
        this.error = e.message
      }
    }
  },
  methods: {
    async doSave() {
      this.saving = true
      this.error = null
      try {
        if (this.isEdit) {
          await api.updateCustomer(this.$route.params.id, this.form)
        } else {
          await api.createCustomer(this.form)
        }
        this.$router.push('/customers')
      } catch (e) {
        this.error = 'خطا در ثبت: ' + e.message
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
