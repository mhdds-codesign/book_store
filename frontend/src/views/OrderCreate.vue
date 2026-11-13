<template>
  <div>
    <div class="page-top-bar">
      <div class="page-title">
        <i class="fas fa-cart-plus"></i>
        <span>ثبت سفارش جدید کتاب</span>
      </div>
      <div class="page-actions">
        <router-link to="/orders" class="btn-orbit-secondary">
          <i class="fas fa-arrow-right"></i>
          <span>بازگشت به سفارش‌ها</span>
        </router-link>
      </div>
    </div>

    <div v-if="error" class="alert-error">
      <i class="fas fa-triangle-exclamation"></i>
      <span>{{ error }}</span>
    </div>

    <div v-if="success" class="alert-success">
      <i class="fas fa-check-circle"></i>
      <span>سفارش با شماره #{{ formatNumber(createdOrderId) }} با موفقیت ثبت شد!</span>
    </div>

    <!-- Customer Selection -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-user"></i>
          <span>انتخاب مشتری</span>
        </div>
      </div>
      <div class="orbit-card-body">
        <div class="form-group" style="margin-bottom:0; max-width:480px;">
          <select v-model="customerId" :disabled="loadingCustomers">
            <option :value="null">— لطفا مشتری مورد نظر را انتخاب کنید —</option>
            <option v-for="c in customers" :key="c.id" :value="c.id">
              {{ c.name }} ({{ c.email }})
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Order Items Selection -->
    <div class="orbit-card">
      <div class="orbit-card-header">
        <div class="orbit-card-title">
          <i class="fas fa-books"></i>
          <span>اقلام سفارش (کتاب‌های انتخابی)</span>
        </div>
      </div>
      <div class="orbit-card-body">
        <div
          v-for="(item, idx) in items"
          :key="idx"
          class="order-item-card"
        >
          <!-- Product Dropdown -->
          <div class="order-item-product">
            <label>کتاب</label>
            <select v-model="item.product_id">
              <option :value="null">— انتخاب کتاب —</option>
              <option v-for="p in products" :key="p.id" :value="p.id">
                {{ p.name }} ({{ formatToman(p.price) }} — موجودی: {{ formatNumber(p.stock) }})
              </option>
            </select>
          </div>

          <!-- Quantity -->
          <div class="order-item-qty">
            <label>تعداد</label>
            <input v-model.number="item.quantity" type="number" min="1" />
          </div>

          <!-- Subtotal -->
          <div class="order-item-subtotal">
            <label>جمع جزء</label>
            <div class="subtotal-display">
              {{ formatToman(calcSubtotal(idx)) }}
            </div>
          </div>

          <!-- Remove Item Button -->
          <div class="order-item-remove" v-if="items.length > 1">
            <button
              class="btn-action-delete"
              @click="removeItem(idx)"
              title="حذف سطر"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>

        <button class="btn-orbit-secondary" @click="addItem" style="font-size:0.88rem;">
          <i class="fas fa-plus"></i>
          <span>افزودن کتاب دیگر</span>
        </button>

        <div class="order-total-summary">
          <span>مبلغ کل فاکتور:</span>
          <span class="total-price-value">{{ formatToman(total) }}</span>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="order-actions-row">
      <button class="btn-orbit-primary" @click="doCreate" :disabled="saving">
        <i class="fas fa-check"></i>
        <span>{{ saving ? 'در حال ثبت سفارش...' : 'تایید و ثبت نهایی سفارش' }}</span>
      </button>
      <router-link to="/orders" class="btn-orbit-secondary">انصراف</router-link>
    </div>
  </div>
</template>

<script>
import api from '../api.js'
import { formatToman, formatNumber } from '../utils.js'

export default {
  data() {
    return {
      customers: [],
      products: [],
      productMap: {},
      customerId: null,
      items: [{ product_id: null, quantity: 1 }],
      error: null,
      success: false,
      createdOrderId: null,
      saving: false,
      loadingCustomers: true
    }
  },
  computed: {
    total() {
      return this.items.reduce((sum, it) => {
        const p = this.productMap[it.product_id]
        return sum + (p ? p.price * (it.quantity || 0) : 0)
      }, 0)
    }
  },
  async created() {
    try {
      const [custRes, prodRes] = await Promise.all([
        api.customers({ per_page: 100 }),
        api.products({ per_page: 100 })
      ])
      this.customers = custRes.customers || []
      this.products = prodRes.products || []
      this.products.forEach(p => {
        this.productMap[p.id] = p
      })
    } catch (e) {
      this.error = e.message
    } finally {
      this.loadingCustomers = false
    }
  },
  methods: {
    formatToman,
    formatNumber,
    addItem() {
      this.items.push({ product_id: null, quantity: 1 })
    },
    removeItem(idx) {
      this.items.splice(idx, 1)
    },
    calcSubtotal(idx) {
      const p = this.productMap[this.items[idx].product_id]
      return p ? p.price * (this.items[idx].quantity || 0) : 0
    },
    async doCreate() {
      this.error = null
      this.success = false
      if (!this.customerId) {
        this.error = 'لطفا ابتدا مشتری را انتخاب نمایید.'
        return
      }
      const orderItems = this.items
        .filter(it => it.product_id && it.quantity > 0)
        .map(it => ({ product_id: it.product_id, quantity: it.quantity }))

      if (!orderItems.length) {
        this.error = 'حداقل یک کتاب باید به سفارش اضافه شود.'
        return
      }

      this.saving = true
      try {
        const res = await api.createOrder({
          customer_id: this.customerId,
          items: orderItems
        })
        this.createdOrderId = res.id
        this.success = true
        setTimeout(() => {
          this.$router.push('/orders/' + res.id)
        }, 1200)
      } catch (e) {
        this.error = 'خطا در ثبت سفارش: ' + e.message
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
