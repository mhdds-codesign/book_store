<template>
  <div>
    <div class="page-top-bar">
      <div class="page-title">
        <i :class="isEdit ? 'fas fa-pen-to-square' : 'fas fa-book-medical'"></i>
        <span>{{ isEdit ? 'ویرایش کتاب' : 'افزودن کتاب جدید' }}</span>
      </div>
      <div class="page-actions">
        <router-link to="/products" class="btn-orbit-secondary">
          <i class="fas fa-arrow-right"></i>
          <span>بازگشت به لیست کتاب‌ها</span>
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
          <label>نام کتاب / عنوان اثر</label>
          <input
            v-model="form.name"
            required
            placeholder="مثال: شازده کوچولو یا Python for Data Science"
          />
        </div>

        <div class="form-group">
          <label>توضیحات (نویسنده، مترجم یا خلاصه اثر)</label>
          <input
            v-model="form.description"
            placeholder="مثال: اثر آنتوان دو سنت اگزوپری ترجمه احمد شاملو"
          />
        </div>

        <div class="form-group">
          <label>قیمت به تومان</label>
          <input
            v-model.number="form.price"
            type="number"
            min="0"
            step="1000"
            required
            placeholder="مثال: ۱۲۰۰۰۰"
          />
          <small style="color:#0d9488; font-weight:600; display:block; margin-top:0.3rem;">
            معادل: {{ formatToman(form.price) }}
          </small>
        </div>

        <div class="form-group">
          <label>تعداد موجودی در انبار</label>
          <input
            v-model.number="form.stock"
            type="number"
            min="0"
            required
            placeholder="مثال: ۵۰"
          />
        </div>

        <div class="form-group">
          <label>دسته‌بندی موضوعی کتاب</label>
          <select v-model.number="form.category_id">
            <option :value="null">— انتخاب دسته‌بندی —</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-orbit-primary" :disabled="saving">
            <i class="fas fa-floppy-disk"></i>
            <span>{{ saving ? 'در حال ذخیره‌سازی...' : (isEdit ? 'بروزرسانی کتاب' : 'ثبت کتاب') }}</span>
          </button>
          <router-link to="/products" class="btn-orbit-secondary">
            انصراف
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import { formatToman } from '../utils.js'

export default {
  data() {
    return {
      isEdit: false,
      saving: false,
      error: null,
      form: {
        name: '',
        description: '',
        price: 0,
        stock: 0,
        category_id: null
      },
      categories: []
    }
  },
  async created() {
    const id = this.$route.params.id
    this.isEdit = !!id

    try {
      const catRes = await api.categories({ per_page: 100 })
      this.categories = catRes.categories || []

      if (id) {
        const p = await api.product(id)
        this.form = {
          name: p.name,
          description: p.description || '',
          price: p.price,
          stock: p.stock,
          category_id: p.category_id
        }
      }
    } catch (e) {
      this.error = e.message
    }
  },
  methods: {
    formatToman,
    async doSave() {
      this.saving = true
      this.error = null
      try {
        if (this.isEdit) {
          await api.updateProduct(this.$route.params.id, this.form)
        } else {
          await api.createProduct(this.form)
        }
        this.$router.push('/products')
      } catch (e) {
        this.error = 'خطا در ثبت: ' + e.message
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
