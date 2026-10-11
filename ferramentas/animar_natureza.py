#!/usr/bin/env python3
"""Anima uma arte parada com movimento sutil de natureza (folhas e grama balancando)
e gera um loop perfeito de poucos segundos em 2560x1440, para usar de fundo no video.

So a vegetacao se mexe: o script acha folhagem e grama pela cor e pela textura, deixa
ceu, montanhas lisas e as areas protegidas paradas, e desloca os pixels com ondas
senoidais cujo periodo e exatamente a duracao do loop (o ultimo quadro emenda no primeiro).

Uso:
  python3 animar_natureza.py <arte> <saida.mp4> [--segundos 4] [--forca 1.0]
      [--proteger x0,y0,x1,y1 ...] [--previa previa.mp4]

--proteger recebe fracoes da imagem (0 a 1) de uma caixa que nao pode mexer
(personagem, texto, logo). Pode repetir.
"""
import argparse
import subprocess
import sys

import cv2
import numpy as np

W, H, FPS = 2560, 1440, 24


def carregar(caminho: str) -> np.ndarray:
    img = cv2.imread(caminho, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"nao consegui abrir {caminho}")
    h, w = img.shape[:2]
    esc = max(W / w, H / h)
    img = cv2.resize(img, (round(w * esc), round(h * esc)), interpolation=cv2.INTER_LANCZOS4)
    h, w = img.shape[:2]
    x0, y0 = (w - W) // 2, (h - H) // 2
    return img[y0:y0 + H, x0:x0 + W].copy()


def ruido_suave(seed: int, escala: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    peq = rng.random((H // escala + 2, W // escala + 2)).astype(np.float32)
    return cv2.resize(peq, (W, H), interpolation=cv2.INTER_CUBIC)


def mascara_vegetacao(img: np.ndarray, proteger: list) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    cor = ((h >= 22) & (h <= 95) & (s > 50) & (v > 25)).astype(np.float32)
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    media = cv2.blur(cinza, (9, 9))
    textura = np.sqrt(np.maximum(cv2.blur(cinza * cinza, (9, 9)) - media * media, 0))
    textura = np.clip((textura - 4) / 10, 0, 1)
    m = cor * textura
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    m = cv2.GaussianBlur(m, (0, 0), 12)
    m = np.clip(m * 1.6, 0, 1)
    for (x0, y0, x1, y1) in proteger:
        caixa = np.zeros((H, W), np.float32)
        caixa[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 1
        caixa = cv2.GaussianBlur(cv2.dilate(caixa, np.ones((41, 41), np.uint8)), (0, 0), 18)
        m *= 1 - np.clip(caixa * 1.5, 0, 1)
    return m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("arte")
    ap.add_argument("saida")
    ap.add_argument("--segundos", type=float, default=4.0)
    ap.add_argument("--forca", type=float, default=1.0)
    ap.add_argument("--proteger", action="append", default=[])
    ap.add_argument("--previa")
    a = ap.parse_args()

    img = carregar(a.arte)
    proteger = [tuple(float(v) for v in p.split(",")) for p in a.proteger]
    m = mascara_vegetacao(img, proteger)

    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    fy = ys / H
    # folhas penduradas no alto balancam mais na ponta; grama embaixo balanca menos
    perfil = np.where(fy < 0.5, 0.6 + 0.8 * fy / 0.5, 0.08 + 0.5 * np.clip((fy - 0.62) / 0.38, 0, 1))
    amp = 3.2 * a.forca * m * perfil * (0.6 + 0.8 * ruido_suave(1, 160))
    fase = 2 * np.pi * ruido_suave(2, 220) + xs / 380.0  # rajada que atravessa a cena
    fase2 = 2 * np.pi * ruido_suave(3, 90)

    n = round(a.segundos * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
           "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.saida]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        t = 2 * np.pi * i / n
        dx = amp * (np.sin(t + fase) + 0.35 * np.sin(2 * t + fase2))
        dy = 0.35 * amp * np.sin(t + fase + 1.3)
        quadro = cv2.remap(img, xs + dx, ys + dy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        ff.stdin.write(quadro.tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        return 1
    if a.previa:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "2", "-i", a.saida,
                        "-vf", "scale=1280:-2", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                        a.previa], check=True)
    cv2.imwrite(a.saida.rsplit(".", 1)[0] + "_mascara.jpg", (m * 255).astype(np.uint8))
    print(f"loop pronto: {a.saida} ({n} quadros, {a.segundos}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
