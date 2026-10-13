from __future__ import annotations

import argparse
import logging
import random
import re
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

import openpyxl
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@dataclass
class Config:
    excel: Path; mensagem: Path; coluna: str; perfil: Path | None
    minimo: float; maximo: float; timeout: int; dry_run: bool; numero: str | None; headless: bool; perfil_chrome: str


def configurar_logs() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")


def limpar_numero(valor: object) -> str:
    numero = re.sub(r"\D", "", str(valor)).lstrip("0")
    if len(numero) in (10, 11):
        numero = "55" + numero
    if len(numero) < 12:
        raise ValueError(f"Número inválido: {valor}")
    return numero


def carregar_contatos(caminho: Path, coluna: str) -> list[str]:
    if not caminho.exists():
        raise FileNotFoundError(f"Excel não encontrado: {caminho}")
    planilha = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
    aba = planilha.active
    cabecalhos = {str(c.value).strip().lower(): c.column for c in aba[1] if c.value is not None}
    indice = cabecalhos.get(coluna.lower())
    if indice is None:
        raise ValueError(f"Coluna '{coluna}' não encontrada. Cabeçalhos: {', '.join(cabecalhos)}")
    contatos = []
    for linha in aba.iter_rows(min_row=2, min_col=indice, max_col=indice, values_only=True):
        if linha[0] is not None:
            try:
                contatos.append(limpar_numero(linha[0]))
            except ValueError as erro:
                logging.warning(str(erro))
    planilha.close()
    return list(dict.fromkeys(contatos))


def ler_mensagem(caminho: Path) -> str:
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de mensagem não encontrado: {caminho}")
    mensagem = caminho.read_text(encoding="utf-8-sig").strip()
    if not mensagem:
        raise ValueError("O arquivo de mensagem está vazio.")
    return mensagem


def enviar(driver, numero: str, mensagem: str, timeout: int) -> None:
    driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={quote(mensagem)}&app_absent=0")
    time.sleep(5)
    caixa = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@contenteditable="true" and @role="textbox"]')))
    time.sleep(2)
    caixa.send_keys(Keys.ENTER)


def executar(config: Config) -> None:
    contatos = carregar_contatos(config.excel, config.coluna)
    if config.numero:
        contatos = [limpar_numero(config.numero)]
    mensagem = ler_mensagem(config.mensagem)
    logging.info("%d contato(s) válido(s) carregado(s).", len(contatos))
    if config.dry_run:
        for contato in contatos:
            logging.info("[DRY-RUN] Enviaria para %s", contato)
        return
    opcoes = webdriver.ChromeOptions()
    if config.headless:
        opcoes.add_argument("--headless=new")
    if config.perfil:
        opcoes.add_argument(f"--user-data-dir={config.perfil.resolve()}")
    opcoes.add_argument(f"--profile-directory={config.perfil_chrome}")
    opcoes.add_argument("--start-maximized")
    opcoes.add_argument("--disable-extensions")
    opcoes.add_argument("--disable-gpu")
    opcoes.add_argument("--no-first-run")
    opcoes.add_argument("--no-default-browser-check")
    opcoes.add_argument("--remote-debugging-port=0")
    driver = webdriver.Chrome(options=opcoes)
    time.sleep(8)
    enviados = falhas = 0
    try:
        for posicao, numero in enumerate(contatos, 1):
            try:
                logging.info("Enviando %d/%d para %s", posicao, len(contatos), numero)
                enviar(driver, numero, mensagem, config.timeout)
                enviados += 1
                time.sleep(random.uniform(config.minimo, config.maximo))
            except (TimeoutException, WebDriverException, ValueError) as erro:
                falhas += 1
                logging.error("Falha para %s: %s", numero, erro)
    finally:
        driver.quit()
        logging.info("Finalizado: %d enviados; %d falhas.", enviados, falhas)


def parse_args() -> Config:
    parser = argparse.ArgumentParser(description="Envia msm.txt aos contatos do Excel.")
    parser.add_argument("--excel", default="zap cursistas.xlsx")
    parser.add_argument("--mensagem", default="msm2.txt")
    parser.add_argument("--coluna", default="zap")
    parser.add_argument("--perfil", default=".chrome_whatsapp", help="Perfil exclusivo do WhatsApp, separado do Chrome pessoal")
    parser.add_argument("--perfil-chrome", default="Default", help="Nome do perfil do Chrome")
    parser.add_argument("--minimo", type=float, default=5)
    parser.add_argument("--maximo", type=float, default=10)
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--numero", default=None, help="Envia somente para este número")
    parser.add_argument("--headless", action="store_true", help="Executa sem janela visível")
    args = parser.parse_args()
    return Config(Path(args.excel), Path(args.mensagem), args.coluna, Path(args.perfil) if args.perfil else None, args.minimo, args.maximo, args.timeout, args.dry_run, args.numero, args.headless, args.perfil_chrome)
