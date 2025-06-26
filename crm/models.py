from django.db import models

class User(models.Model):
    first_name = models.CharField("Nombre", max_length=50)
    last_name = models.CharField("Apellidos", max_length=50)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Teléfono", max_length=20, blank=True, null=True)
    address = models.TextField("Dirección", blank=True, null=True)
    registration_date = models.DateTimeField("Fecha de registro", auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagada'),
        ('cancelled', 'Cancelada'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices', verbose_name="Usuario")
    amount = models.DecimalField("Importe", max_digits=10, decimal_places=2)
    description = models.TextField("Descripción", blank=True, null=True)
    date = models.DateTimeField("Fecha", auto_now_add=True)
    status = models.CharField("Estado", max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Factura #{self.id} para {self.user}"


