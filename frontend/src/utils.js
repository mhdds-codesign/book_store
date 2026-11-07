/**
 * Persian formatting utilities for OrbitBook
 */

export function formatToman(amount) {
  if (amount == null || isNaN(amount)) return '۰ تومان'
  const val = Math.round(Number(amount))
  return val.toLocaleString('fa-IR') + ' تومان'
}

export function formatNumber(num) {
  if (num == null || isNaN(num)) return '۰'
  return Number(num).toLocaleString('fa-IR')
}

export function formatPersianDate(dateStr) {
  if (!dateStr) return '—'
  try {
    const d = new Date(dateStr)
    if (isNaN(d.getTime())) return dateStr
    return new Intl.DateTimeFormat('fa-IR-u-ca-persian', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).format(d)
  } catch {
    return dateStr
  }
}

export function translateStatus(status) {
  if (!status) return '—'
  const s = status.toLowerCase()
  if (s === 'completed' || s === 'تکمیل شده') return 'تکمیل شده'
  if (s === 'cancelled' || s === 'لغو شده') return 'لغو شده'
  if (s === 'pending' || s === 'در انتظار') return 'در انتظار'
  return status
}

export function getStatusClass(status) {
  const s = translateStatus(status)
  if (s === 'تکمیل شده') return 'status-completed'
  if (s === 'لغو شده') return 'status-cancelled'
  return 'status-pending'
}
