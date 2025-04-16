from fastapi import FastAPI
import pyautogui as auto
import time
import os
import psutil

app = FastAPI()


def is_uvicorn_running():
    for proc in psutil.process_iter(['pid', 'name']):
        if "uvicorn" in proc.info['name']:
            return True
    return False

if not is_uvicorn_running():
    os.system("uvicorn Main:app --reload")

@app.get("/")
def main():
    return "Hello World"

@app.get("/navegarInternet/{site}")
def navegarInternet(site: str):
    auto.press('win')
    time.sleep(2)
    auto.write('opera')
    auto.press('enter')
    time.sleep(2)
    auto.write(site)
    auto.press('enter')

@app.get("/abrirAplicativo/{app}")
def abrirAplicativo(app: str):
    auto.press('win')
    time.sleep(2)
    auto.write(app)
    auto.press('enter')

@app.get("/desligarComputador")
def deligarComputador():
    os.system("shutdown /s /t 1")