<template>
  <div>
    <!-- Top Header Bar -->
    <div class="page-top-bar">
      <div class="page-title">
        <i class="fas fa-users"></i>
        <span>مشتریان</span>
      </div>

      <div class="page-actions">
        <router-link to="/customers/new" class="btn-orbit-primary">
          <i class="fas fa-plus"></i>
          <span>افزودن مشتری</span>
        </router-link>
      </div>
    </div>

    <!-- Sorting Controls Bar -->
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
        <button
          class="sort-pill"
          :class="{ active: sort === 'email' }"
          @click="setSort('email')"
        >
          ایمیل
        </button>
      </div>
    </div>

    <!-- Customers Table Card -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-address-book"></i>
          <span>لیست مشتریان ({{ formatNumber(total) }})</span>
        </div>
      </div>

      <div v-if="loading" class="state-box">
        <i class="fas fa-spinner fa-spin"></i>
        <p>در حال بارگذاری مشتریان...</p>
      </div>

      <div v-else class="table-responsive">
        <table class="orbit-table">
          <thead>
            <tr>
              <th style="width:45px;">#</th>
              <th>نام</th>
              <th>ویرایش / حذف</th>
              <th>تلفن</th>
              <th>ایمیل</th>
              <th style="text-align:center;">سفارش‌ها</th>
              <th style="text-align:center;">عملیات</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in customers" :key="c.id">
              <td style="font-weight:700; color:#64748b;">#{{ formatNumber(c.id) }}</td>
              <td style="font-weight:700; font-size:1rem; color:#0c3b4a;">{{ c.name }}</td>
              <td>
                <div class="action-buttons-group">
                  <router-link :to="'/customers/' + c.id + '/edit'" class="btn-action-edit" title="ویرایش">
                    <i class="fas fa-pen"></i>
                  </router-link>
                  <button class="btn-action-delete" @click="doDelete(c)" title="حذف">
                    <i class="fas fa-trash-can"></i>
                  </button>
                </div>
              </td>
              <td style="direction:ltr; text-align:right; color:#475569;">{{ c.phone || '—' }}</td>
              <td style="color:#0284c7; direction:ltr; text-align:right;">{{ c.email }}</td>
              <td style="text-align:center; font-weight:700;">
                <span class="status-pill status-completed" style="padding:0.2rem 0.75rem;">
                  {{ formatNumber(c.order_count) }}
                </span>
              </td>
              <td style="text-align:center;">
                <router-link :to="'/orders?customer_id=' + c.id" class="btn-action-view" title="مشاهده سفارش‌های این مشتری">
                  <i class="fas fa-eye"></i>
                </router-link>
              </td>
            </tr>
            <tr v-if="!customers.length">
              <td colspan="7" style="text-align:center; padding:3rem; color:#94a3b8;">
                مشتری یافت نشد.
              </td>
            </tr>
          </tbody>
        </table>
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
      customers: [],
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
        const res = await api.customers({ sort: this.sort, page: this.page })
        this.customers = res.customers || []
        this.total = res.total || 0
        this.totalPages = res.total_pages || 1
      } catch (e) {
        alert('خطا در بارگذاری مشتریان: ' + e.message)
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
      if (!confirm(`آیا از حذف مشتری "${c.name}" اطمینان دارید؟ تمامی سفارش‌های این مشتری نیز حذف خواهند شد.`)) return
      try {
        await api.deleteCustomer(c.id)
        this.load()
      } catch (e) {
        alert('خطا در حذف مشتری: ' + e.message)
      }
    }
  }
}
</script>
