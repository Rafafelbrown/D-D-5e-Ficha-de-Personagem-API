# D&D 5e — API REST construída com **FastAPI** para geração de fichas de personagem D&D 5e.
Recebe os dados do personagem em JSON e devolve o PDF oficial preenchido.
API REST construída com **FastAPI** para geração de fichas de personagem D&D 5e.
Recebe os dados do personagem em JSON e devolve o PDF oficial preenchido.

Conversão do app Streamlit original (`dnd_ficha_v4.py`).

---

## Estrutura do projeto

```
dnd_api/
├── main.py           # App FastAPI — rotas e configuração
├── models.py         # Modelos Pydantic (request/response)
├── pdf_service.py    # Lógica de negócio: cálculos e preenchimento do PDF
├── requirements.txt
└── Ficha-Oficial-D-D-5E-Editavel.pdf   ← coloque aqui o template
```

---

## Instalação

```bash
pip install -r requirements.txt
```

---

## Execução

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em:
- Swagger UI → http://localhost:8000/docs
- ReDoc      → http://localhost:8000/redoc

---

## Endpoints

### `POST /ficha/gerar-pdf`
Recebe os dados do personagem em JSON e devolve o PDF preenchido para download.
O template PDF deve estar na pasta do projeto como `Ficha-Oficial-D-D-5E-Editavel.pdf`,
ou pode ser enviado no campo `template` como `multipart/form-data`.

**Exemplo com curl:**
```bash
curl -X POST http://localhost:8000/ficha/gerar-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "nome_personagem": "Aldric Pedraforte",
    "classe_nivel": "Guerreiro 5",
    "raca": "Humano",
    "forca": 18,
    "destreza": 14,
    "constituicao": 16,
    "inteligencia": 10,
    "sabedoria": 12,
    "carisma": 8,
    "bonus_proficiencia": 3,
    "classe_armadura": 18,
    "pv_maximo": 52,
    "pv_atuais": 52,
    "salv_forca_prof": true,
    "salv_constituicao_prof": true,
    "atletismo_prof": true,
    "ataque1_nome": "Espada Longa",
    "ataque1_bonus": "+7",
    "ataque1_dano": "1d8+4 cortante"
  }' \
  --output ficha_aldric.pdf
```

### `POST /ficha/gerar-pdf-upload`
Alternativa multipart: envie o template PDF e um arquivo JSON separadamente.

### `POST /ficha/calcular`
Calcula e devolve modificadores, salvaguardas e perícias sem gerar o PDF.
Útil para exibir valores em tempo real em um front-end.

### `GET /ficha/campos`
Retorna o schema JSON completo do modelo com a descrição de cada campo.

---

## Diferenças em relação ao app Streamlit original

| Streamlit (`dnd_ficha_v4.py`) | FastAPI (`dnd_api/`) |
|-------------------------------|----------------------|
| Interface gráfica no browser  | API REST pura        |
| Upload do template pela barra lateral | Template no disco ou enviado via `multipart/form-data` |
| Cálculos só no momento da geração | Endpoint `/calcular` para cálculos isolados |
| Arquivo único                 | Separação em `main`, `models`, `pdf_service` |
| `streamlit`, `pdfrw`          | `fastapi`, `uvicorn`, `pdfrw`, `python-multipart` |
