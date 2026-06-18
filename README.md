# Integração de Mensagens WhatsApp com Python

Script Python que lê contatos do **Supabase** e envia mensagens personalizadas via **WhatsApp (Z-API)**.

---

## Setup da tabela no Supabase

Crie um projeto gratuito em [supabase.com](https://supabase.com), vá em **Table Editor → New Table** e crie a tabela `contatos` com as colunas:

| Coluna    | Tipo   | Descrição                                      |
|-----------|--------|------------------------------------------------|
| `id`      | `int8` | PK, auto increment                             |
| `nome`    | `text` | Nome do contato (ex.: `João`)                  |
| `contato` | `text` | Número com DDI, sem `+` (ex.: `5511999998888`) |

Insira até 3 contatos de teste pelo próprio Table Editor.

---

## Variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

| Variável             | Onde encontrar                                              |
|----------------------|-------------------------------------------------------------|
| `SUPABASE_URL`       | Dashboard → seu projeto → Settings → API → Project URL     |
| `SUPABASE_KEY`       | Dashboard → seu projeto → Settings → API → `anon` key      |
| `ZAPI_INSTANCE_ID`   | [app.z-api.io](https://app.z-api.io) → sua instância       |
| `ZAPI_TOKEN`         | app.z-api.io → sua instância → Token                       |
| `ZAPI_CLIENT_TOKEN`  | app.z-api.io → sua conta → Security → Client Token         |

---

## Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/whatsapp-notifier.git
cd whatsapp-notifier

# 2. Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com suas credenciais

# 5. Execute
python main.py
```

### Saída esperada

```
2026-06-18 10:00:00 [INFO] Buscando contatos no Supabase...
2026-06-18 10:00:01 [INFO] 3 contato(s) encontrado(s).
2026-06-18 10:00:01 [INFO] Enviando mensagem para João (5511999998888)...
2026-06-18 10:00:02 [INFO] Mensagem enviada para 5511999998888.
2026-06-18 10:00:02 [INFO] Concluído - 3/3 mensagem(ns) enviada(s) com sucesso.
```