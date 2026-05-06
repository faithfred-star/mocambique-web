from django.db import models

class Order(models.Model):
    # Atualizado para refletir apenas a Movitel conforme solicitado nos templates
    PAYMENT_METHODS = [
        ('movitel', 'Movitel (e-Mola)'),
    ]
    
    DELIVERY_METHODS = [
        ('town', 'Recolha na Cidade'),
        ('door', 'Entrega ao Domicílio'),
    ]

    # Campos de Identidade e Contacto
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=100) # BI / Passaporte
    email = models.EmailField()
    phone = models.CharField(max_length=20) # Número Principal (+258)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    alt_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Campos de Endereço
    city = models.CharField(max_length=100)
    address = models.TextField()
    
    # Métodos e Valores
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHODS, default='town')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='movitel')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status e Segurança
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    # Lógica de Verificação (OTP)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    otp_resend_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"