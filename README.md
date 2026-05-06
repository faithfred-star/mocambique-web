# Starlink Moçambique - Django Full Stack

Este é um clone do site de pedidos da Starlink, adaptado para o mercado de Moçambique, com suporte para pagamentos locais e notificações via Telegram.

## Funcionalidades
- **Idioma:** Português (Moçambique).
- **Moeda:** Metical (MT).
- **Métodos de Pagamento:** M-Pesa, Airtel Money e e-Mola (Movitel).
- **Notificações:** Integração com Bot do Telegram para alertar sobre novos pedidos e o método de pagamento utilizado.
- **Painel Administrativo:** Gerenciamento completo de pedidos via Django Admin.

## Requisitos
- Python 3.10+
- Django 5.x
- Requests (para notificações do Telegram)

## Configuração do Telegram
No arquivo `core/settings.py`, configure as seguintes variáveis:
- `TELEGRAM_BOT_TOKEN`: O token do seu bot criado via @BotFather.
- `TELEGRAM_CHAT_ID`: O ID do chat ou grupo onde as notificações serão enviadas.

## Como Executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute as migrações:
   ```bash
   python manage.py migrate
   ```
3. Crie um superusuário para acessar o admin:
   ```bash
   python manage.py createsuperuser
   ```
4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## Estrutura do Projeto
- `core/`: Configurações principais do Django.
- `orders/`: Aplicativo que gerencia os pedidos, modelos e lógica de notificação.
- `templates/`: Arquivos HTML (Base, Index, Checkout, Instruções de Pagamento).
- `static/`: Arquivos CSS e imagens.
