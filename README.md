
# D&D 5e — Ficha de Personagem API

API REST construída com **FastAPI** para geração de fichas de personagem D&D 5e.
Recebe os dados do personagem em JSON e devolve o PDF oficial preenchido (3 páginas).

---

## Estrutura do projeto

```
dnd_api/
├── main.py                              # App FastAPI — rotas e configuração
├── models.py                            # Modelos Pydantic (request/response)
├── pdf_service.py                       # Lógica de negócio: cálculos e preenchimento do PDF
├── ficha.html                           # Interface HTML servida em GET /html
├── requirements.txt
└── Ficha-Oficial-D-D-5E-Editavel.pdf   ← coloque aqui o template (3 páginas)
```

---

## Instalação

```bash
pip install -r requirements.txt
```

Dependências:

| Pacote | Versão mínima | Uso |
|---|---|---|
| `fastapi` | 0.111.0 | Framework web |
| `uvicorn[standard]` | 0.29.0 | Servidor ASGI |
| `pdfrw` | 0.4 | Leitura/escrita de campos PDF |
| `python-multipart` | 0.0.9 | Upload de arquivos via `multipart/form-data` |

---

## Execução

```bash
uvicorn main:app --reload
```

| Interface | URL |
|---|---|
| Interface HTML | http://localhost:8000/html |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## Endpoints

### `GET /html`
Serve o arquivo `ficha.html` diretamente no navegador. É a rota padrão (redirecionamento de `/`).

---

### `POST /ficha/gerar-pdf`
Recebe os dados do personagem como JSON e devolve o PDF oficial preenchido para download.

O template `Ficha-Oficial-D-D-5E-Editavel.pdf` deve estar na mesma pasta que `main.py`, ou pode ser enviado no campo `template` como `multipart/form-data`.

**Exemplo com curl (JSON puro):**
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

---

### `POST /ficha/gerar-pdf-upload`
Alternativa multipart: envie o template PDF e um arquivo JSON separadamente.

```bash
curl -X POST http://localhost:8000/ficha/gerar-pdf-upload \
  -F "template=@Ficha-Oficial-D-D-5E-Editavel.pdf" \
  -F "ficha_json=@personagem.json" \
  --output ficha.pdf
```

---

### `POST /ficha/calcular`
Calcula e devolve modificadores, salvaguardas e perícias **sem gerar o PDF**. Útil para exibir valores em tempo real em um front-end.

**Resposta (`FichaCalculada`):**
```json
{
  "iniciativa": "+2",
  "sabedoria_passiva": 11,
  "modificadores": { "forca": "+4", "destreza": "+2", ... },
  "salvaguardas":  { "forca": "+7", "destreza": "+2", ... },
  "pericias":      { "atletismo": "+7", "intimidacao": "+3", ... }
}
```

---

### `GET /ficha/campos`
Retorna o schema JSON completo do modelo `FichaPersonagem` com a descrição de cada campo. Útil para validação no front-end ou geração automática de formulários.

---

## Modelo de dados (`FichaPersonagem`)

Todos os campos são opcionais exceto `nome_personagem`. Os valores padrão reproduzem uma ficha em branco do jogo.

| Grupo | Campos principais |
|---|---|
| Cabeçalho | `nome_personagem`, `classe_nivel`, `antecedente`, `nome_jogador`, `raca`, `alinhamento`, `experiencia` |
| Atributos | `forca`, `destreza`, `constituicao`, `inteligencia`, `sabedoria`, `carisma` (1–30, padrão 10) |
| Combate | `inspiracao`, `bonus_proficiencia`, `classe_armadura`, `deslocamento`, `dado_vida` |
| Pontos de vida | `pv_maximo`, `pv_atuais`, `pv_temporarios` |
| Salvaguardas | `salv_<atributo>_prof` (bool) — proficiência em cada salvaguarda |
| Perícias | `<pericia>_prof` (bool) — 18 perícias disponíveis |
| Ataques | `ataque1/2/3_nome`, `ataque1/2/3_bonus`, `ataque1/2/3_dano` + `ataques_conjuracao_extra` |
| Personalidade | `tracos_personalidade`, `ideais`, `vinculos`, `fraquezas` |
| Textos (pág. 1) | `outras_proficiencias`, `equipamento`, `caracteristicas_talentos` |
| Aparência (pág. 2) | `idade`, `altura`, `peso`, `cor_olhos`, `cor_pele`, `cor_cabelo` |
| Histórico (pág. 2) | `aliados_nome`, `aliados_organizacoes`, `caract_talentos_adicionais`, `historia_personagem`, `tesouros` |
| Magias (pág. 3) | `classe_conjuradora`, `atributo_conjuracao`, `cd_magias`, `bonus_ataque_magico` |

---

## Cálculos automáticos

O serviço (`pdf_service.py`) calcula automaticamente ao gerar o PDF:

- **Modificadores de atributo** → `(atributo - 10) // 2`, exibidos com sinal (`+4`, `-1`).
- **Iniciativa** → modificador de Destreza.
- **Salvaguardas** → modificador do atributo + bônus de proficiência (se proficiente).
- **Perícias** → modificador do atributo vinculado + bônus de proficiência (se proficiente).
- **Percepção passiva** → `10 + modificador de Percepção`.

---

## Mapeamento de campos PDF

O arquivo `pdf_service.py` mantém o dicionário `MAPA_CAMPOS` com o ID real de cada campo do formulário PDF (`"Campo de Texto0"`, `"Caixa de Seleção0"`, etc.) mapeado para a chave interna do modelo. Isso cobre as 3 páginas da ficha oficial.

---

## Diferenças em relação ao app Streamlit original

| Streamlit (`dnd_ficha_v4.py`) | FastAPI (`dnd_api/`) |
|---|---|
| Interface gráfica no browser | API REST pura + HTML em `/html` |
| Upload do template pela barra lateral | Template no disco ou via `multipart/form-data` |
| Cálculos só no momento da geração | Endpoint `/ficha/calcular` para cálculos isolados |
| Arquivo único | Separação em `main`, `models`, `pdf_service` |
| `streamlit`, `pdfrw` | `fastapi`, `uvicorn`, `pdfrw`, `python-multipart` |

