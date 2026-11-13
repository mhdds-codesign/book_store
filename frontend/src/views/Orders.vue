<template>
  <div>
    <!-- Top Header Bar -->
    <div class="page-top-bar">
      <div class="page-title">
        <i class="fas fa-cart-shopping"></i>
        <span>سفارش‌ها</span>
      </div>

      <div class="page-actions">
        <router-link to="/orders/new" class="btn-orbit-primary">
          <i class="fas fa-plus"></i>
          <span>سفارش جدید</span>
        </router-link>
      </div>
    </div>

    <!-- Search & Sort Controls Bar -->
    <div class="search-filter-card">
      <div class="orders-filter-row">
        <!-- Sort Pills -->
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
            :class="{ active: sort === 'price' }"
            @click="setSort('price')"
          >
            قیمتی
          </button>
          <button
            class="sort-pill"
            :class="{ active: sort === 'status' }"
            @click="setSort('status')"
          >
            وضعیت
          </button>
        </div>

        <!-- Search Input -->
        <div class="orders-search-box">
          <input
            v-model="searchQuery"
            @keyup.enter="load"
            placeholder="جستجو در سفارش‌ها..."
          />
          <button class="btn-search-trigger" @click="load" title="جستجو">
            <i class="fas fa-search"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Orders Table Card -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-file-invoice"></i>
          <span>همه سفارش‌ها ({{ formatNumber(total) }})</span>
        </div>
      </div>

      <div v-if="loading" class="state-box">
        <i class="fas fa-spinner fa-spin"></i>
        <p>در حال دریافت سفارش‌ها...</p>
      </div>

      <div v-else class="table-responsive">
        <table class="orbit-table">
          <thead>
            <tr>
              <th style="width:45px;">#</th>
              <th>مشتری</th>
              <th>تاریخ</th>
              <th style="text-align:center;">آیتم‌ها</th>
              <th>مبلغ کل</th>
              <th>وضعیت</th>
              <th style="text-align:center;">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="o in orders" :key="o.id">
              <td style="font-weight:700; color:#64748b;">#{{ formatNumber(o.id) }}</td>
              <td style="font-weight:600;">{{ o.customer_name }}</td>
              <td style="color:#64748b;">{{ formatPersianDate(o.order_date) }}</td>
              <td style="text-align:center; font-weight:700;">{{ formatNumber(o.items?.length || 0) }}</td>
              <td style="font-weight:700; color:#0d9488;">{{ formatToman(o.total_amount) }}</td>
              <td>
                <span :class="['status-pill', getStatusClass(o.status)]">
                  {{ translateStatus(o.status) }}
                </span>
              </td>
              <td style="text-align:center;">
                <router-link :to="'/orders/' + o.id" class="btn-action-view" title="مشاهده جزئیات سفارش">
                  <i class="fas fa-eye"></i>
                </router-link>
              </td>
            </tr>
            <tr v-if="!orders.length">
              <td colspan="7" style="text-align:center; padding:3rem; color:#94a3b8;">
                سفارشی با این مشخصات یافت نشد.
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
import { formatToman, formatNumber, formatPersianDate, translateStatus, getStatusClass } from '../utils.js'

export default {
  data() {
    return {
      orders: [],
      total: 0,
      page: 1,
      totalPages: 1,
      sort: 'default',
      searchQuery: '',
      loading: true
    }
  },
  async created() {
    await this.load()
  },
  methods: {
    formatToman,
    formatNumber,
    formatPersianDate,
    translateStatus,
    getStatusClass,
    setSort(val) {
      this.sort = val
      this.page = 1
      this.load()
    },
    async load() {
      this.loading = true
      try {
        const params = { page: this.page, sort: this.sort }
        if (this.searchQuery) params.q = this.searchQuery
        const res = await api.orders(params)
        this.orders = res.orders || []
        this.total = res.total || 0
        this.totalPages = res.total_pages || 1
      } catch (e) {
        alert('خطا در بارگذاری سفارش‌ها: ' + e.message)
      } finally {
        this.loading = false
      }
    },
    goPage(n) {
      if (n >= 1 && n <= this.totalPages) {
        this.page = n
        this.load()
      }
    }
  }
}
</script>
