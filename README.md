💍 Wedding Manager

Sistema de gerenciamento de casamento desenvolvido com Django para ajudar os noivos a organizarem convidados, confirmações de presença (RSVP) e controle financeiro do evento.

O sistema possui um painel administrativo elegante, confirmação de presença online e envio de convites diretamente pelo WhatsApp.

✨ Funcionalidades
👰 Dashboard dos Noivos

Painel privado para gerenciamento completo do casamento.

Inclui:

Contagem regressiva para o casamento

Data oficial do evento

Estatísticas de convidados

Taxa de confirmação

Gráfico de confirmações

Gráfico de gastos por categoria

Controle de despesas

📋 Gerenciamento de Convidados

Permite organizar todos os convidados do casamento.

Funcionalidades:

Cadastro manual de convidados

Classificação por tipo:

Amigo

Família

Identificação de quem convidou:

Noivo

Noiva

Cadastro de acompanhantes

Status de confirmação

Edição de convidados

Visualização de acompanhantes

📩 RSVP (Confirmação de Presença)

Cada convidado recebe um link exclusivo para confirmação de presença.

O formulário permite:

confirmar presença

adicionar acompanhantes

atualizar dados

registrar confirmação no banco

Após confirmar presença o convidado recebe um email automático de agradecimento.

📱 Envio de Convites via WhatsApp

No painel dos noivos é possível enviar o convite diretamente pelo WhatsApp.

O sistema gera automaticamente uma mensagem contendo:

nome do convidado

mensagem personalizada

link de confirmação RSVP

💰 Controle Financeiro

O sistema possui controle de despesas do casamento.

Cada despesa pode conter:

nome da despesa

categoria

valor

status (pago ou pendente)

O dashboard mostra:

total gasto

despesas pendentes

gráfico de gastos por categoria

🖥️ Tecnologias Utilizadas

Python

Django

SQLite

HTML

CSS

JavaScript

Chart.js

Google Fonts

⚙️ Instalação

Clone o repositório:

git clone https://github.com/lucascarrari/wedding-manager.git

Entre na pasta do projeto:

cd wedding-manager
🐍 Criar ambiente virtual
python -m venv venv

Ativar ambiente virtual.

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
📦 Instalar dependências
pip install django python-dotenv
🔐 Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto:

SECRET_KEY=sua_secret_key
DEBUG=True

EMAIL_HOST_USER=seu_email
EMAIL_HOST_PASSWORD=sua_senha_de_app

⚠️ O arquivo .env não é enviado ao GitHub por segurança.

🗄️ Aplicar migrações
python manage.py migrate
👤 Criar super usuário
python manage.py createsuperuser
🚀 Rodar o servidor
python manage.py runserver

Abra no navegador:

http://127.0.0.1:8000
🔑 Acesso ao painel

Admin do Django:

http://127.0.0.1:8000/admin

Dashboard dos noivos:

http://127.0.0.1:8000/dashboard
📂 Estrutura do Projeto
wedding_manager/
│
├── wedding/
│ ├── models.py
│ ├── views.py
│ ├── forms.py
│ ├── urls.py
│
├── templates/
│
├── static/
│ ├── css
│ ├── js
│
├── manage.py
└── db.sqlite3
🔒 Segurança

Arquivos sensíveis não são enviados ao repositório:

.env

venv

db.sqlite3

Esses arquivos são protegidos pelo .gitignore.

📈 Melhorias Futuras

Lista de presença exportável

Organização de mesas

QR Code para confirmação

Área pública do evento

Upload de fotos

Lista de presentes

👨‍💻 Autor

Lucas Carrari

Projeto desenvolvido para gerenciamento do próprio casamento.

❤️ Licença

Este projeto foi desenvolvido para fins pessoais e educacionais.
