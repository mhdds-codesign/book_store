<template>
  <div>
    <!-- Top Header Bar -->
    <div class="page-top-bar">
      <div class="page-title">
        <i class="fas fa-tags"></i>
        <span>دسته‌بندی‌ها</span>
      </div>

      <div class="page-actions">
        <router-link to="/categories/new" class="btn-orbit-primary">
          <i class="fas fa-plus"></i>
          <span>افزودن دسته‌بندی</span>
        </router-link>
      </div>
    </div>

    <!-- Sorting Bar -->
    <div class="search-filter-card" style="padding: 1rem 1.25rem;">
      <div class="sort-pills-bar" style="margin-bottom:0;">
        <span class="sort-label">مرتب‌سازی بر اساس:</span>
        <button
          class="sort-pill"
          :class="{ active: sort === 'default' }"
          @click="setSort('default')"
        >
          پیش‌فرض
        </button>
        <button
          class="sort-pill"
          :class="{ active: sort === 'name' }"
          @click="setSort('name')"
        >
          نام (الفبای فارسی)
        </button>
      </div>
    </div>

    <!-- Categories Card with Left Illustration from Design -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-layer-group"></i>
          <span>تمامی دسته‌بندی‌های کتاب ({{ formatNumber(total) }})</span>
        </div>
      </div>

      <div v-if="loading" class="state-box">
        <i class="fas fa-spinner fa-spin"></i>
        <p>در حال بارگذاری دسته‌بندی‌ها...</p>
      </div>

      <div v-else class="category-card-layout">
        <!-- Table on Right (in RTL) -->
        <div class="table-responsive" style="flex:1;">
          <table class="orbit-table">
            <thead>
              <tr>
                <th style="width:45px;">#</th>
                <th>نام دسته‌بندی</th>
                <th>توضیحات</th>
                <th style="text-align:center;">محصولات</th>
                <th style="text-align:center;">عملیات</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in categories" :key="c.id">
                <td style="font-weight:700; color:#64748b;">#{{ formatNumber(c.id) }}</td>
                <td style="font-weight:700; color:#0c3b4a; font-size:1rem;">{{ c.name }}</td>
                <td style="color:#475569; max-width:320px;">{{ c.description || '—' }}</td>
                <td style="text-align:center; font-weight:700;">
                  <span class="status-pill status-completed" style="padding:0.2rem 0.8rem;">
                    {{ formatNumber(c.product_count) }}
                  </span>
                </td>
                <td style="text-align:center;">
                  <div class="action-buttons-group" style="justify-content:center;">
                    <router-link :to="'/categories/' + c.id + '/edit'" class="btn-action-edit" title="ویرایش">
                      <i class="fas fa-pen"></i>
                    </router-link>
                    <button class="btn-action-delete" @click="doDelete(c)" title="حذف">
                      <i class="fas fa-trash-can"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!categories.length">
                <td colspan="5" style="text-align:center; padding:3rem; color:#94a3b8;">
                  دسته‌بندی ثبت نشده است.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 3D Book Artwork on Left (as in screenshot) -->
        <div class="category-card-left-img">
          <img src="/assets/books_category.png" alt="دسته‌بندی کتاب‌ها" />
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="orbit-pagination">
        <button
          class="page-btn"
          :disabled="page <= 1"
          @click="goPage(page - 1)"
        >
          قبل
        </button>
        <button
          v-for="p in totalPages"
          :key="p"
          class="page-btn"
          :class="{ active: p === page }"
          @click="goPage(p)"
        >
          {{ formatNumber(p) }}
        </button>
        <button
          class="page-btn"
          :disabled="page >= totalPages"
          @click="goPage(page + 1)"
        >
          بعدی
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import { formatNumber } from '../utils.js'

export default {
  data() {
    return {
      categories: [],
      total: 0,
      page: 1,
      totalPages: 1,
      sort: 'default',
      loading: true
    }
  },
  async created() {
    await this.load()
  },
  methods: {
    formatNumber,
    setSort(val) {
      this.sort = val
      this.page = 1
      this.load()
    },
    async load() {
      this.loading = true
      try {
        const res = await api.categories({ sort: this.sort, page: this.page })
        this.categories = res.categories || []
        this.total = res.total || 0
        this.totalPages = res.total_pages || 1
      } catch (e) {
        alert('خطا در بارگذاری دسته‌بندی‌ها: ' + e.message)
      } finally {
        this.loading = false
      }
    },
    goPage(n) {
      if (n >= 1 && n <= this.totalPages) {
        this.page = n
        this.load()
      }
    },
    async doDelete(c) {
      if (!confirm(`آیا از حذف دسته‌بندی "${c.name}" اطمینان دارید؟`)) return
      try {
        await api.deleteCategory(c.id)
        this.load()
      } catch (e) {
        alert('خطا در حذف دسته‌بندی: ' + e.message)
      }
    }
  }
}
</script>
