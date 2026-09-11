price = float(input("Цена: "))
discount = float(input("Скидка: "))
vat = float(input("НДС: "))

base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount

print(f"{'База после скидки:':<20} {base:>12.2f} ₽")
print(f"{'НДС:':<20} {vat_amount:>12.2f} ₽")
print(f"{'Итого к оплате:':<20} {total:>12.2f} ₽")