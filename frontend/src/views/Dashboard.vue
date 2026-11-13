<template>
  <div>
    <!-- Welcome Greeting Banner from Design -->
    <div class="welcome-banner">
      <div class="welcome-text">
        <h1>
          <span>به اوربیت بوک خوش آمدید!</span>
          <i class="fas fa-sparkles" style="color:#0d9488; font-size:1.2rem;"></i>
        </h1>
        <p>امیدواریم روز کاری پربرکت و خوبی را در کتابفروشی سپری کنید</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="state-box">
      <i class="fas fa-spinner fa-spin"></i>
      <p>در حال بارگذاری اطلاعات داشبورد...</p>
    </div>

    <template v-else-if="data">
      <!-- 5 Stat Cards in Row -->
      <div class="stats-grid">
        <!-- Products -->
        <div class="stat-card">
          <div class="stat-card-header">
            <div class="stat-icon stat-icon-green">
              <i class="fas fa-box"></i>
            </div>
            <div class="stat-title">محصولات</div>
          </div>
          <div class="stat-card-body">
            <div class="stat-value">{{ formatNumber(data.total_products) }}</div>
            <div class="stat-badge">
              <i class="fas fa-arrow-up"></i>
              <span>+۱۷%</span>
            </div>
          </div>
        </div>

        <!-- Categories -->
        <div class="stat-card">
          <div class="stat-card-header">
            <div class="stat-icon stat-icon-blue">
              <i class="fas fa-shapes"></i>
            </div>
            <div class="stat-title">دسته‌بندی‌ها</div>
          </div>
          <div class="stat-card-body">
            <div class="stat-value">{{ formatNumber(data.total_categories) }}</div>
            <div class="stat-badge">
              <i class="fas fa-arrow-up"></i>
              <span>+۰%</span>
            </div>
          </div>
        </div>

        <!-- Customers -->
        <div class="stat-card">
          <div class="stat-card-header">
            <div class="stat-icon stat-icon-purple">
              <i class="fas fa-users"></i>
            </div>
            <div class="stat-title">مشتریان</div>
          </div>
          <div class="stat-card-body">
            <div class="stat-value">{{ formatNumber(data.total_customers) }}</div>
            <div class="stat-badge">
              <i class="fas fa-arrow-up"></i>
              <span>+۰%</span>
            </div>
          </div>
        </div>

        <!-- Orders -->
        <div class="stat-card">
          <div class="stat-card-header">
            <div class="stat-icon stat-icon-teal">
              <i class="fas fa-cart-shopping"></i>
            </div>
            <div class="stat-title">سفارش‌ها</div>
          </div>
          <div class="stat-card-body">
            <div class="stat-value">{{ formatNumber(data.total_orders) }}</div>
            <div class="stat-badge">
              <i class="fas fa-arrow-up"></i>
              <span>+۲۹%</span>
            </div>
          </div>
        </div>

        <!-- Revenue (in Toman) -->
        <div class="stat-card">
          <div class="stat-card-header">
            <div class="stat-icon stat-icon-emerald">
              <i class="fas fa-coins"></i>
            </div>
            <div class="stat-title">درآمد کل</div>
          </div>
          <div class="stat-card-body">
            <div class="stat-value" style="font-size:1.15rem; color:#059669;">{{ formatToman(data.total_revenue) }}</div>
            <div class="stat-badge">
              <i class="fas fa-arrow-up"></i>
              <span>+۴۵%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Two-Column Grid: Recent Orders (Right) & Sales Overview (Left) -->
      <div class="dashboard-grid">
        <!-- Right Column: Recent Orders -->
        <div class="orbit-card">
          <div class="orbit-card-header">
            <div class="orbit-card-title">
              <i class="fas fa-clock-rotate-left"></i>
              <span>آخرین سفارش‌ها</span>
            </div>
            <router-link to="/orders" class="btn-orbit-secondary" style="font-size:0.85rem; padding:0.35rem 0.9rem;">
              <span>مشاهده همه</span>
              <i class="fas fa-chevron-left" style="font-size:0.75rem;"></i>
            </router-link>
          </div>
          <div class="table-responsive">
            <table class="orbit-table">
              <thead>
                <tr>
                  <th style="width:40px;">#</th>
                  <th>مشتری</th>
                  <th>تاریخ</th>
                  <th>وضعیت</th>
                  <th style="text-align:center;">عملیات</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="o in data.recent_orders" :key="o.id">
                  <td style="font-weight:700; color:#64748b;">#{{ formatNumber(o.id) }}</td>
                  <td style="font-weight:600;">{{ o.customer_name }}</td>
                  <td style="color:#64748b;">{{ formatPersianDate(o.order_date) }}</td>
                  <td>
                    <span :class="['status-pill', getStatusClass(o.status)]">
                      {{ translateStatus(o.status) }}
                    </span>
                  </td>
                  <td style="text-align:center;">
                    <router-link :to="'/orders/' + o.id" class="btn-action-view" title="مشاهده جزئیات">
                      <i class="fas fa-eye"></i>
                    </router-link>
                  </td>
                </tr>
                <tr v-if="!data.recent_orders || !data.recent_orders.length">
                  <td colspan="5" style="text-align:center; padding:2rem; color:#94a3b8;">
                    سفارشی ثبت نشده است.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Left Column: Sales Overview Chart -->
        <div class="orbit-card">
          <div class="orbit-card-header chart-header-row">
            <div class="orbit-card-title">
              <i class="fas fa-chart-line"></i>
              <span>نمای کلی فروش</span>
            </div>
            <div class="chart-header-actions">
              <span class="status-pill status-completed" style="font-size:0.82rem; padding:0.25rem 0.75rem;">
                {{ formatToman(data.total_revenue) }}
              </span>
              <select style="border-radius:20px; border:1px solid #cbd5e1; padding:0.25rem 0.7rem; font-size:0.82rem; background:#fff; font-family:inherit;">
                <option>این ماه</option>
                <option>ماه گذشته</option>
                <option>امسال</option>
              </select>
            </div>
          </div>
          <div class="orbit-card-body" style="padding:1rem;">
            <!-- Beautiful Glowing Vector SVG Line Chart -->
            <div style="width:100%; height:220px; position:relative; overflow:hidden;">
              <svg viewBox="0 0 500 200" style="width:100%; height:100%; overflow:visible;">
                <defs>
                  <linearGradient id="chartGlowGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.0" />
                  </linearGradient>
                </defs>

                <!-- Grid horizontal lines -->
                <line x1="40" y1="30" x2="480" y2="30" stroke="#e2e8f0" stroke-dasharray="4 4" />
                <line x1="40" y1="80" x2="480" y2="80" stroke="#e2e8f0" stroke-dasharray="4 4" />
                <line x1="40" y1="130" x2="480" y2="130" stroke="#e2e8f0" stroke-dasharray="4 4" />
                <line x1="40" y1="180" x2="480" y2="180" stroke="#e2e8f0" />

                <!-- Y-axis labels -->
                <text x="25" y="35" font-size="10" fill="#94a3b8" text-anchor="middle">1.5M</text>
                <text x="25" y="85" font-size="10" fill="#94a3b8" text-anchor="middle">1M</text>
                <text x="25" y="135" font-size="10" fill="#94a3b8" text-anchor="middle">500k</text>
                <text x="25" y="184" font-size="10" fill="#94a3b8" text-anchor="middle">0</text>

                <!-- Area fill -->
                <path
                  d="M 60 160 C 120 170, 160 85, 210 100 C 260 115, 300 40, 360 45 C 420 50, 440 90, 470 65 L 470 180 L 60 180 Z"
                  fill="url(#chartGlowGradient)"
                />

                <!-- Stroke Line -->
                <path
                  d="M 60 160 C 120 170, 160 85, 210 100 C 260 115, 300 40, 360 45 C 420 50, 440 90, 470 65"
                  fill="none"
                  stroke="#0891b2"
                  stroke-width="3.5"
                  stroke-linecap="round"
                />

                <!-- Data Points -->
                <circle cx="60" cy="160" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="130" cy="150" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="210" cy="100" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="280" cy="105" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="360" cy="45" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="420" cy="70" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />
                <circle cx="470" cy="65" r="5" fill="#ffffff" stroke="#0891b2" stroke-width="2.5" />

                <!-- X-axis Persian Weekdays -->
                <text x="60" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">شنبه</text>
                <text x="130" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">یکشنبه</text>
                <text x="210" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">دوشنبه</text>
                <text x="280" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">سه‌شنبه</text>
                <text x="360" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">چهارشنبه</text>
                <text x="420" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">پنجشنبه</text>
                <text x="470" y="196" font-size="11" fill="#64748b" text-anchor="middle" font-family="Vazirmatn">جمعه</text>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import api from '../api.js'
import { formatToman, formatNumber, formatPersianDate, translateStatus, getStatusClass } from '../utils.js'

export default {
  data() {
    return {
      data: null,
      loading: true
    }
  },
  async created() {
    await this.fetchDashboard()
  },
  methods: {
    formatToman,
    formatNumber,
    formatPersianDate,
    translateStatus,
    getStatusClass,
    async fetchDashboard() {
      this.loading = true
      try {
        this.data = await api.dashboard()
      } catch (err) {
        alert('خطا در بارگذاری اطلاعات داشبورد: ' + err.message)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
