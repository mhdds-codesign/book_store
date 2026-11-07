# تابع مرتبسازی فارسی برای نام
def persian_sort_key(customer):
    """مرتبسازی بر اساس نام فارسی"""
    persian_alphabet = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    name = getattr(customer, 'name', '') or ''

    result = []
    for char in name:
        if char in persian_alphabet:
            result.append(persian_alphabet.index(char))
        else:
            result.append(ord(char))
    return result
