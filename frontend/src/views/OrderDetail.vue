<template>
  <div>
    <div v-if="loading" class="state-box">
      <i class="fas fa-spinner fa-spin"></i>
      <p>در حال بارگذاری فاکتور سفارش...</p>
    </div>

    <div v-else-if="order">
      <div class="page-top-bar">
        <div class="page-title">
          <i class="fas fa-receipt"></i>
          <span>جزئیات سفارش #{{ formatNumber(order.id) }}</span>
        </div>
        <div class="page-actions">
          <router-link to="/orders" class="btn-orbit-secondary">
            <i class="fas fa-arrow-right"></i>
            <span>بازگشت به سفارش‌ها</span>
          </router-link>
        </div>
      </div>

      <!-- Order Info Summary Card -->
      <div class="orbit-card">
        <div class="orbit-card-header">
          <div class="orbit-card-title">
            <i class="fas fa-circle-info"></i>
            <span>اطلاعات سفارش و خریدار</span>
          </div>
        </div>
        <div class="orbit-card-body">
          <div class="order-detail-meta-grid">
            <div>
              <span style="display:block; color:#64748b; font-size:0.9rem; margin-bottom:0.25rem;">نام خریدار:</span>
              <strong style="font-size:1.05rem; color:#0c3b4a;">{{ order.customer_name }}</strong>
            </div>
            <div>
              <span style="display:block; color:#64748b; font-size:0.9rem; margin-bottom:0.25rem;">تاریخ ثبت سفارش:</span>
              <strong style="color:#0c3b4a;">{{ formatPersianDate(order.order_date) }}</strong>
            </div>
            <div>
              <span style="display:block; color:#64748b; font-size:0.9rem; margin-bottom:0.25rem;">مبلغ کل فاکتور:</span>
              <strong style="color:#0d9488; font-size:1.2rem;">{{ formatToman(order.total_amount) }}</strong>
            </div>
            <div>
              <span style="display:block; color:#64748b; font-size:0.9rem; margin-bottom:0.4rem;">وضعیت فعلی:</span>
              <div class="status-updater-row">
                <span :class="['status-pill', getStatusClass(order.status)]">
                  {{ translateStatus(order.status) }}
                </span>
                <select v-model="newStatus" style="width:auto; padding:0.35rem 0.6rem; border-radius:8px; border:1px solid #cbd5e1; font-family:inherit; font-size:0.85rem;">
                  <option value="completed">تکمیل شده</option>
                  <option value="pending">در انتظار</option>
                  <option value="cancelled">لغو شده</option>
                </select>
                <button class="btn-orbit-primary" @click="updateStatus" style="padding:0.35rem 0.8rem; font-size:0.85rem;">
                  ثبت وضعیت
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Itemized Table Card -->
      <div class="orbit-card">
        <div class="orbit-card-header">
          <div class="orbit-card-title">
            <i class="fas fa-list-check"></i>
            <span>کتاب‌های سفارش داده شده</span>
          </div>
        </div>
        <div class="table-responsive">
          <table class="orbit-table">
            <thead>
              <tr>
                <th style="width:45px;">#</th>
                <th>عنوان کتاب</th>
                <th>قیمت واحد</th>
                <th style="text-align:center;">تعداد</th>
                <th>جمع کل</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in order.items" :key="item.id">
                <td style="font-weight:700; color:#64748b;">{{ formatNumber(index + 1) }}</td>
                <td style="font-weight:700; color:#0c3b4a;">
                  {{ item.product_name || ('کتاب #' + formatNumber(item.product_id)) }}
                </td>
                <td style="color:#475569;">{{ formatToman(item.unit_price) }}</td>
                <td style="text-align:center; font-weight:700;">{{ formatNumber(item.quantity) }}</td>
                <td style="font-weight:700; color:#0d9488;">
                  {{ formatToman(item.unit_price * item.quantity) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div style="padding:1.25rem 1.5rem; background:#f4fbfb; display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0;">
          <span style="font-weight:700; font-size:1.1rem; color:#0c3b4a;">مبلغ نهایی پرداختی:</span>
          <span style="font-weight:800; font-size:1.4rem; color:#0d9488;">{{ formatToman(order.total_amount) }}</span>
        </div>
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
      order: null,
      loading: true,
      newStatus: 'completed'
    }
  },
  async created() {
    try {
      this.order = await api.order(this.$route.params.id)
      this.newStatus = this.order.status || 'pending'
    } catch (e) {
      alert('خطا در بارگذاری سفارش: ' + e.message)
    } finally {
      this.loading = false
    }
  },
  methods: {
    formatToman,
    formatNumber,
    formatPersianDate,
    translateStatus,
    getStatusClass,
    async updateStatus() {
      try {
        this.order = await api.updateOrderStatus(this.$route.params.id, this.newStatus)
        this.newStatus = this.order.status
        alert('وضعیت سفارش با موفقیت به «' + translateStatus(this.order.status) + '» تغییر یافت.')
      } catch (e) {
        alert('خطا در بروزرسانی وضعیت: ' + e.message)
      }
    }
  }
}
</script>
