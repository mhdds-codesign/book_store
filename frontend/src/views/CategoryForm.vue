<template>
  <div>
    <div class="page-top-bar">
      <div class="page-title">
        <i :class="isEdit ? 'fas fa-pen-to-square' : 'fas fa-folder-plus'"></i>
        <span>{{ isEdit ? 'ویرایش دسته‌بندی' : 'افزودن دسته‌بندی جدید' }}</span>
      </div>
      <div class="page-actions">
        <router-link to="/categories" class="btn-orbit-secondary">
          <i class="fas fa-arrow-right"></i>
          <span>بازگشت به دسته‌بندی‌ها</span>
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
          <label>نام دسته‌بندی کتاب</label>
          <input
            v-model="form.name"
            required
            placeholder="مثال: رمان و ادبیات داستانی"
          />
        </div>

        <div class="form-group">
          <label>توضیحات دسته‌بندی</label>
          <input
            v-model="form.description"
            placeholder="مثال: شاهکارهای ادبیات جهان، رمان‌های کلاسیک و معاصر"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-orbit-primary" :disabled="saving">
            <i class="fas fa-floppy-disk"></i>
            <span>{{ saving ? 'در حال ذخیره‌سازی...' : (isEdit ? 'بروزرسانی دسته‌بندی' : 'ثبت دسته‌بندی') }}</span>
          </button>
          <router-link to="/categories" class="btn-orbit-secondary">
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
        description: ''
      }
    }
  },
  async created() {
    const id = this.$route.params.id
    this.isEdit = !!id

    if (id) {
      try {
        const res = await api.categories({ per_page: 100 })
        const c = (res.categories || []).find(x => x.id == id)
        if (c) {
          this.form = {
            name: c.name,
            description: c.description || ''
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
          await api.updateCategory(this.$route.params.id, this.form)
        } else {
          await api.createCategory(this.form)
        }
        this.$router.push('/categories')
      } catch (e) {
        this.error = 'خطا در ثبت: ' + e.message
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
