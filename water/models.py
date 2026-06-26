from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (so'm)")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi qoldiq (dona)")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Rasm")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} – {self.price:,.0f} so'm"


class Customer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Mijoz/Kompaniya nomi")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    address = models.TextField(verbose_name="Manzil")

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name="invoices", verbose_name="Mijoz"
    )
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0.00, editable=False,
        verbose_name="Umumiy summa (so'm)"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Faktura"
        verbose_name_plural = "Fakturalar"
        ordering = ['-created_at']

    def update_total_price(self):
        total = sum(item.item_total_price for item in self.items.all())
        self.total_price = total
        # Faqat total_price maydonini o'zini saqlaymiz (rekursiya bo'lmasligi uchun)
        Invoice.objects.filter(pk=self.pk).update(total_price=total)

    def __str__(self):
        return f"#{self.pk} – {self.customer.name} ({self.created_at.strftime('%d.%m.%Y')})"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE,
        related_name="items", verbose_name="Faktura"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        verbose_name="Mahsulot"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdor (dona)")
    item_total_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, editable=False,
        verbose_name="Satr summasi (so'm)"
    )

    class Meta:
        verbose_name = "Faktura mahsuloti"
        verbose_name_plural = "Faktura mahsulotlari"

    def save(self, *args, **kwargs):
        self.item_total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)
        self.invoice.update_total_price()

    def delete(self, *args, **kwargs):
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.update_total_price()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"