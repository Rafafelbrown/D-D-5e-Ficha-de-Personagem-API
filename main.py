#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ficha de Personagem D&D 5e — FastAPI
=====================================
Converte a lógica de negócio do app Streamlit original para uma API REST.

Endpoints principais:
  GET  /html              → Serve a interface HTML da ficha.
  POST /ficha/gerar-pdf   → Recebe JSON com dados do personagem, retorna PDF preenchido.
  GET  /ficha/campos      → Lista todos os campos disponíveis com descrição.
  POST /ficha/calcular    → Calcula modificadores, salvaguardas e perícias a partir dos atributos.

Execução:
    uvicorn main:app --reload

Dependências:
    pip install fastapi uvicorn pdfrw python-multipart
"""

import io
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.responses import RedirectResponse

from models import FichaPersonagem, FichaCalculada
from pdf_service import construir_dados_pdf, preencher_pdf, calcular_ficha

PDF_TEMPLATE_DEFAULT = "Ficha-Oficial-D-D-5E-Editavel.pdf"
HTML_FILE_DEFAULT    = "ficha.html"

app = FastAPI(
    title="D&D 5e — Ficha de Personagem API",
    description=(
        "API para geração de fichas de personagem de D&D 5e. "
        "Recebe os dados do personagem em JSON e devolve o PDF oficial preenchido."
    ),
    version="4.0.0",
)


def _carregar_template() -> bytes:
    """Tenta carregar o template PDF do disco. Lança HTTPException se não encontrado."""
    if not os.path.exists(PDF_TEMPLATE_DEFAULT):
        raise HTTPException(
            status_code=503,
            detail=(
                f"Template '{PDF_TEMPLATE_DEFAULT}' não encontrado no servidor. "
                "Use o endpoint /ficha/gerar-pdf com upload do template, ou "
                "coloque o PDF na mesma pasta que main.py."
            ),
        )
    with open(PDF_TEMPLATE_DEFAULT, "rb") as f:
        return f.read()


# ─────────────────────────────────────────────────────────────────
# Rotas
# ─────────────────────────────────────────────────────────────────

@app.get("/", tags=["Status"], include_in_schema=False)
def raiz():
    return RedirectResponse(url="/html")


@app.get(
    "/html",
    tags=["Interface"],
    summary="Abre a interface HTML da ficha",
    response_class=HTMLResponse,
)
def servir_html():
    """
    Serve o arquivo `ficha.html` diretamente pelo navegador.
    Basta acessar http://localhost:8000/html para abrir a interface.
    """
    if not os.path.exists(HTML_FILE_DEFAULT):
        raise HTTPException(
            status_code=404,
            detail=(
                f"Arquivo '{HTML_FILE_DEFAULT}' não encontrado. "
                "Coloque o ficha.html na mesma pasta que main.py."
            ),
        )
    with open(HTML_FILE_DEFAULT, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post(
    "/ficha/gerar-pdf",
    tags=["Ficha"],
    summary="Gera o PDF preenchido com os dados do personagem",
    response_description="Arquivo PDF preenchido para download",
)
def gerar_pdf(
    ficha: FichaPersonagem,
    template: UploadFile = File(default=None, description="PDF template (opcional se estiver no servidor)"),
):
    """
    Recebe os dados do personagem em JSON e devolve o PDF oficial da D&D 5e preenchido.

    O template pode ser enviado como `multipart/form-data` no campo `template`.
    Se omitido, o servidor busca o arquivo `Ficha-Oficial-D-D-5E-Editavel.pdf`
    na pasta de trabalho.

    **Atenção:** para enviar JSON + arquivo simultaneamente use `multipart/form-data`
    e passe os dados da ficha como string JSON no campo `ficha`.
    """
    if not ficha.nome_personagem or not ficha.nome_personagem.strip():
        raise HTTPException(status_code=422, detail="O campo 'nome_personagem' é obrigatório.")

    # Carrega o template
    if template is not None:
        template_bytes = template.file.read()
    else:
        template_bytes = _carregar_template()

    dados_pdf = construir_dados_pdf(ficha.model_dump())
    pdf_bytes = preencher_pdf(dados_pdf, template_bytes)

    nome_arquivo = ficha.nome_personagem.strip().replace(" ", "_").lower()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="ficha_{nome_arquivo}.pdf"',
        },
    )


@app.post(
    "/ficha/gerar-pdf-upload",
    tags=["Ficha"],
    summary="Gera o PDF enviando template e dados separadamente via multipart",
)
async def gerar_pdf_com_upload(
    template: UploadFile = File(..., description="PDF template oficial D&D 5e"),
    ficha_json: UploadFile = File(..., description="JSON com os dados do personagem"),
):
    """
    Alternativa multipart: envie o template PDF e um arquivo JSON com os dados
    do personagem. Útil para clientes que preferem não serializar JSON em campos
    de formulário.
    """
    import json

    template_bytes = await template.read()
    ficha_raw = await ficha_json.read()

    try:
        ficha_dict = json.loads(ficha_raw)
        ficha = FichaPersonagem(**ficha_dict)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"JSON inválido: {exc}")

    if not ficha.nome_personagem or not ficha.nome_personagem.strip():
        raise HTTPException(status_code=422, detail="O campo 'nome_personagem' é obrigatório.")

    dados_pdf = construir_dados_pdf(ficha.model_dump())
    pdf_bytes = preencher_pdf(dados_pdf, template_bytes)
    nome_arquivo = ficha.nome_personagem.strip().replace(" ", "_").lower()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="ficha_{nome_arquivo}.pdf"'},
    )


@app.post(
    "/ficha/calcular",
    tags=["Ficha"],
    summary="Calcula modificadores, salvaguardas e perícias",
    response_model=FichaCalculada,
)
def calcular(ficha: FichaPersonagem):
    """
    Devolve todos os valores calculados (modificadores de atributo,
    salvaguardas e perícias) sem gerar o PDF. Útil para front-ends
    que precisam exibir os totais em tempo real.
    """
    return calcular_ficha(ficha.model_dump())


@app.get(
    "/ficha/campos",
    tags=["Ficha"],
    summary="Lista todos os campos disponíveis no modelo",
)
def listar_campos():
    """Retorna o schema JSON do modelo FichaPersonagem com descrições de cada campo."""
    return FichaPersonagem.model_json_schema()
