from fastapi import FastAPI
import pyautogui as auto
import time
import os

app = FastAPI()

@app.get("/navegarInternet/{site}")
def navegarInternet(site :str):
    auto.press('win')
    time.sleep(2)
    auto.write('opera')
    auto.press('enter')
    time.sleep(2)
    auto.write(site)
    auto.press('enter')

@app.get("/abrirAplicativo/{app}")
def abrirAplicativo(app :str):
    auto.press('win')
    time.sleep(2)
    auto.write(app)
    auto.press('enter')

@app.get("/desligarComputador")
def deligarComputador():
    os.system("shutdown /s /t 1")