#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelos Pydantic para a Ficha de Personagem D&D 5e.
"""

from typing import Optional
from pydantic import BaseModel, Field


class FichaPersonagem(BaseModel):
    """Dados completos do personagem D&D 5e."""

    # ── Cabeçalho ────────────────────────────────────────────────────
    nome_personagem: str = Field(..., description="Nome do personagem")
    classe_nivel: Optional[str] = Field(None, description="Classe e nível (ex.: Guerreiro 5)")
    antecedente: Optional[str] = Field(None, description="Antecedente (ex.: Soldado)")
    nome_jogador: Optional[str] = Field(None, description="Nome do jogador")
    raca: Optional[str] = Field(None, description="Raça (ex.: Humano)")
    alinhamento: Optional[str] = Field(None, description="Alinhamento (ex.: Leal e Bom)")
    experiencia: Optional[int] = Field(0, ge=0, description="Pontos de experiência")

    # ── Atributos ────────────────────────────────────────────────────
    forca: int = Field(10, ge=1, le=30, description="Força")
    destreza: int = Field(10, ge=1, le=30, description="Destreza")
    constituicao: int = Field(10, ge=1, le=30, description="Constituição")
    inteligencia: int = Field(10, ge=1, le=30, description="Inteligência")
    sabedoria: int = Field(10, ge=1, le=30, description="Sabedoria")
    carisma: int = Field(10, ge=1, le=30, description="Carisma")

    # ── Stats de combate ─────────────────────────────────────────────
    inspiracao: bool = Field(False, description="Inspiração ativa")
    bonus_proficiencia: int = Field(2, ge=2, le=6, description="Bônus de proficiência (+2 a +6)")
    classe_armadura: int = Field(10, ge=0, description="Classe de armadura (CA)")
    deslocamento: int = Field(9, ge=0, description="Deslocamento em metros")
    dado_vida: Optional[str] = Field(None, description="Dado de vida (ex.: 1d10)")

    # ── Pontos de vida ───────────────────────────────────────────────
    pv_maximo: int = Field(10, ge=0, description="Pontos de vida máximos")
    pv_atuais: int = Field(10, ge=0, description="Pontos de vida atuais")
    pv_temporarios: int = Field(0, ge=0, description="Pontos de vida temporários")

    # ── Salvaguardas — proficiência ──────────────────────────────────
    salv_forca_prof: bool = Field(False)
    salv_destreza_prof: bool = Field(False)
    salv_constituicao_prof: bool = Field(False)
    salv_inteligencia_prof: bool = Field(False)
    salv_sabedoria_prof: bool = Field(False)
    salv_carisma_prof: bool = Field(False)

    # ── Perícias — proficiência ──────────────────────────────────────
    acrobacia_prof: bool = Field(False)
    arcanismo_prof: bool = Field(False)
    atletismo_prof: bool = Field(False)
    atuacao_prof: bool = Field(False)
    enganacao_prof: bool = Field(False)
    furtividade_prof: bool = Field(False)
    historia_prof: bool = Field(False)
    intimidacao_prof: bool = Field(False)
    intuicao_prof: bool = Field(False)
    investigacao_prof: bool = Field(False)
    lidar_animais_prof: bool = Field(False)
    medicina_prof: bool = Field(False)
    natureza_prof: bool = Field(False)
    percepcao_prof: bool = Field(False)
    persuasao_prof: bool = Field(False)
    prestidigitacao_prof: bool = Field(False)
    religiao_prof: bool = Field(False)
    sobrevivencia_prof: bool = Field(False)

    # ── Ataques ──────────────────────────────────────────────────────
    ataque1_nome: Optional[str] = Field(None, description="Nome do 1º ataque")
    ataque1_bonus: Optional[str] = Field(None, description="Bônus de ataque do 1º ataque (ex.: +5)")
    ataque1_dano: Optional[str] = Field(None, description="Dano/tipo do 1º ataque (ex.: 1d8+3 cortante)")
    ataque2_nome: Optional[str] = Field(None)
    ataque2_bonus: Optional[str] = Field(None)
    ataque2_dano: Optional[str] = Field(None)
    ataque3_nome: Optional[str] = Field(None)
    ataque3_bonus: Optional[str] = Field(None)
    ataque3_dano: Optional[str] = Field(None)
    ataques_conjuracao_extra: Optional[str] = Field(None, description="Notas adicionais de ataques & conjuração")

    # ── Traços de personalidade ──────────────────────────────────────
    tracos_personalidade: Optional[str] = Field(None)
    ideais: Optional[str] = Field(None)
    vinculos: Optional[str] = Field(None)
    fraquezas: Optional[str] = Field(None)

    # ── Áreas de texto (página 1) ────────────────────────────────────
    outras_proficiencias: Optional[str] = Field(None, description="Proficiências com armas, armaduras, ferramentas e idiomas")
    equipamento: Optional[str] = Field(None, description="Itens, armas, armaduras, dinheiro…")
    caracteristicas_talentos: Optional[str] = Field(None, description="Características de classe, raciais e talentos")

    # ── Aparência física (página 2) ──────────────────────────────────
    idade: Optional[str] = Field(None)
    altura: Optional[str] = Field(None)
    peso: Optional[str] = Field(None)
    cor_olhos: Optional[str] = Field(None)
    cor_pele: Optional[str] = Field(None)
    cor_cabelo: Optional[str] = Field(None)

    # ── Histórico & organização (página 2) ──────────────────────────
    aliados_nome: Optional[str] = Field(None)
    aliados_organizacoes: Optional[str] = Field(None)
    caract_talentos_adicionais: Optional[str] = Field(None)
    historia_personagem: Optional[str] = Field(None)
    tesouros: Optional[str] = Field(None)

    # ── Magias (página 3) ────────────────────────────────────────────
    classe_conjuradora: Optional[str] = Field(None)
    atributo_conjuracao: Optional[str] = Field(None)
    cd_magias: Optional[str] = Field(None)
    bonus_ataque_magico: Optional[str] = Field(None)

    model_config = {"json_schema_extra": {
        "example": {
            "nome_personagem": "Aldric Pedraforte",
            "classe_nivel": "Guerreiro 5",
            "antecedente": "Soldado",
            "nome_jogador": "Rafael",
            "raca": "Humano",
            "alinhamento": "Leal e Bom",
            "experiencia": 6500,
            "forca": 18,
            "destreza": 14,
            "constituicao": 16,
            "inteligencia": 10,
            "sabedoria": 12,
            "carisma": 8,
            "bonus_proficiencia": 3,
            "classe_armadura": 18,
            "deslocamento": 9,
            "dado_vida": "1d10",
            "pv_maximo": 52,
            "pv_atuais": 52,
            "pv_temporarios": 0,
            "salv_forca_prof": True,
            "salv_constituicao_prof": True,
            "atletismo_prof": True,
            "intimidacao_prof": True,
            "ataque1_nome": "Espada Longa",
            "ataque1_bonus": "+7",
            "ataque1_dano": "1d8+4 cortante",
        }
    }}


class ModificadoresAtributo(BaseModel):
    forca: str
    destreza: str
    constituicao: str
    inteligencia: str
    sabedoria: str
    carisma: str


class ValoresSalvaguarda(BaseModel):
    forca: str
    destreza: str
    constituicao: str
    inteligencia: str
    sabedoria: str
    carisma: str


class ValoresPericia(BaseModel):
    acrobacia: str
    arcanismo: str
    atletismo: str
    atuacao: str
    enganacao: str
    furtividade: str
    historia: str
    intimidacao: str
    intuicao: str
    investigacao: str
    lidar_animais: str
    medicina: str
    natureza: str
    percepcao: str
    persuasao: str
    prestidigitacao: str
    religiao: str
    sobrevivencia: str


class FichaCalculada(BaseModel):
    """Resultado dos cálculos automáticos da ficha."""
    iniciativa: str = Field(..., description="Modificador de iniciativa (= mod. Destreza)")
    sabedoria_passiva: int = Field(..., description="Percepção passiva (10 + mod. Percepção)")
    modificadores: ModificadoresAtributo
    salvaguardas: ValoresSalvaguarda
    pericias: ValoresPericia
