<template>
  <div>
    <!-- Top Header Bar -->
    <div class="page-top-bar">
      <div class="page-title">
        <i class="fas fa-boxes-stacked"></i>
        <span>محصولات و کتاب‌ها</span>
      </div>

      <div class="page-actions">
        <router-link to="/products/new" class="btn-orbit-primary">
          <i class="fas fa-plus"></i>
          <span>افزودن محصول</span>
        </router-link>
      </div>
    </div>

    <!-- Search & Filter Card from Design -->
    <div class="search-filter-card">
      <div class="filter-bar-header">
        <div class="filter-title">
          <i class="fas fa-filter" style="color:var(--teal-primary);"></i>
          <span>جستجو و فیلتر</span>
        </div>
      </div>

      <div class="filter-inputs-row">
        <!-- Search Keyword -->
        <div class="filter-input-wrap filter-input-search">
          <input
            v-model="filters.q"
            @keyup.enter="applyFilters"
            placeholder="نام محصول یا توضیحات..."
          />
        </div>

        <!-- Min Price -->
        <div class="filter-input-wrap">
          <input
            v-model.number="filters.min_price"
            type="number"
            placeholder="حداقل قیمت (تومان)"
          />
        </div>

        <!-- Max Price -->
        <div class="filter-input-wrap">
          <input
            v-model.number="filters.max_price"
            type="number"
            placeholder="حداکثر قیمت (تومان)"
          />
        </div>

        <!-- Category Dropdown -->
        <div class="filter-input-wrap">
          <select v-model.number="filters.category_id">
            <option :value="0">همه دسته‌بندی‌ها</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>

        <!-- Search & Reset Buttons -->
        <div class="filter-buttons-group">
          <button class="btn-search-trigger" @click="applyFilters">
            <i class="fas fa-search"></i>
            <span>جستجو</span>
          </button>
          <button class="btn-orbit-secondary btn-reset-filters" @click="resetFilters" title="پاکسازی فیلترها">
            <i class="fas fa-rotate-right"></i>
          </button>
        </div>
      </div>

      <!-- Sort Pills Bar -->
      <div class="sort-pills-bar" style="margin-top:1.2rem; margin-bottom:0;">
        <span class="sort-label">مرتب‌سازی بر اساس:</span>
        <button
          class="sort-pill"
          :class="{ active: filters.sort === 'default' }"
          @click="setSort('default')"
        >
          پیش‌فرض
        </button>
        <button
          class="sort-pill"
          :class="{ active: filters.sort === 'name' }"
          @click="setSort('name')"
        >
          نام کتاب (الفبای فارسی)
        </button>
        <button
          class="sort-pill"
          :class="{ active: filters.sort === 'price' }"
          @click="setSort('price')"
        >
          قیمت
        </button>
        <button
          class="sort-pill"
          :class="{ active: filters.sort === 'stock' }"
          @click="setSort('stock')"
        >
          موجودی
        </button>
      </div>
    </div>

    <!-- Products Table Card -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-book"></i>
          <span>لیست کتاب‌ها ({{ formatNumber(total) }})</span>
        </div>
      </div>

      <div v-if="loading" class="state-box">
        <i class="fas fa-spinner fa-spin"></i>
        <p>در حال بارگذاری اطلاعات محصولات...</p>
      </div>

      <div v-else class="table-responsive">
        <table class="orbit-table">
          <thead>
            <tr>
              <th style="width:45px;">#</th>
              <th style="text-align:center; width:60px;">تصویر</th>
              <th>نام محصول</th>
              <th>دسته‌بندی</th>
              <th>قیمت</th>
              <th style="text-align:center;">موجودی</th>
              <th style="text-align:center;">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in products" :key="p.id">
              <td style="font-weight:700; color:#64748b;">#{{ formatNumber(p.id) }}</td>
              <td style="text-align:center;">
                <img src="/assets/book_thumb.png" alt="کتاب" class="product-book-thumb" />
              </td>
              <td>
                <div style="font-weight:700; color:#0c3b4a; font-size:1rem;">{{ p.name }}</div>
                <div style="font-size:0.82rem; color:#64748b; max-width:320px;" v-if="p.description">
                  {{ p.description }}
                </div>
              </td>
              <td>
                <span class="status-pill status-pending" style="font-size:0.82rem; padding:0.25rem 0.75rem;">
                  {{ p.category_name || 'بدون دسته‌بندی' }}
                </span>
              </td>
              <td style="font-weight:700; color:#0d9488; font-size:1rem;">
                {{ formatToman(p.price) }}
              </td>
              <td style="text-align:center;">
                <span
                  style="font-weight:700; padding:0.2rem 0.7rem; border-radius:8px;"
                  :style="{
                    color: p.stock < 10 ? '#dc2626' : '#1e293b',
                    background: p.stock < 10 ? '#fee2e2' : '#f1f5f9'
                  }"
                >
                  {{ formatNumber(p.stock) }}
                </span>
              </td>
              <td style="text-align:center;">
                <div class="action-buttons-group" style="justify-content:center;">
                  <router-link :to="'/products/' + p.id + '/edit'" class="btn-action-edit" title="ویرایش">
                    <i class="fas fa-pen"></i>
                  </router-link>
                  <button class="btn-action-delete" @click="doDelete(p)" title="حذف">
                    <i class="fas fa-trash-can"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!products.length">
              <td colspan="7" style="text-align:center; padding:3rem; color:#94a3b8;">
                محصولی با این مشخصات یافت نشد.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div v-if="totalPages > 1" class="orbit-pagination">
        <button
          class="page-btn"
          :disabled="page <= 1"
          @click="goPage(page - 1)"
        >
          قبل
        </button>
        <button
          v-for="n in totalPages"
          :key="n"
          class="page-btn"
          :class="{ active: n === page }"
          @click="goPage(n)"
        >
          {{ formatNumber(n) }}
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
import { formatToman, formatNumber } from '../utils.js'

export default {
  data() {
    return {
      products: [],
      categories: [],
      total: 0,
      page: 1,
      totalPages: 1,
      loading: true,
      filters: {
        sort: 'default',
        q: '',
        min_price: null,
        max_price: null,
        category_id: 0
      }
    }
  },
  async created() {
    await this.load()
  },
  methods: {
    formatToman,
    formatNumber,
    setSort(val) {
      this.filters.sort = val
      this.page = 1
      this.load()
    },
    applyFilters() {
      this.page = 1
      this.load()
    },
    resetFilters() {
      this.filters = {
        sort: 'default',
        q: '',
        min_price: null,
        max_price: null,
        category_id: 0
      }
      this.page = 1
      this.load()
    },
    async load() {
      this.loading = true
      try {
        const params = {
          sort: this.filters.sort,
          page: this.page,
          per_page: 10
        }
        if (this.filters.q) params.q = this.filters.q
        if (this.filters.min_price != null && this.filters.min_price !== '') params.min_price = this.filters.min_price
        if (this.filters.max_price != null && this.filters.max_price !== '') params.max_price = this.filters.max_price
        if (this.filters.category_id) params.category_id = this.filters.category_id

        const res = await api.products(params)
        this.products = res.products || []
        this.total = res.total || 0
        this.totalPages = res.total_pages || 1
        this.categories = res.categories || []
      } catch (e) {
        alert('خطا در دریافت لیست محصولات: ' + e.message)
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
    async doDelete(p) {
      if (!confirm(`آیا از حذف کتاب "${p.name}" اطمینان دارید؟`)) return
      try {
        await api.deleteProduct(p.id)
        this.load()
      } catch (e) {
        alert('خطا در حذف محصول: ' + e.message)
      }
    }
  }
}
</script>
