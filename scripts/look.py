"""v3 look. grade(rgb float 0-1 HxWx3, mask float 0-1 HxW) -> rgb.
Built from the reference study:
- McKinnon / Johnny Harris: subject brighter than the room, room darker + cooler, deep but not crushed blacks.
- D'Avella: restrained saturation (~0.25-0.35), slightly lifted blacks, warm-neutral skin, soft highlight roll-off.
"""
import numpy as np

H, W = 1920, 1080
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
KEY = np.exp(-(((xx - W * 0.52) / (W * 0.60)) ** 2 + ((yy - H * 0.50) / (H * 0.40)) ** 2))
VIG = (1 - 0.45 * np.clip(((xx - W / 2) / (W * 0.70)) ** 2 + ((yy - H * 0.56) / (H * 0.60)) ** 2 - 0.2, 0, 1)) * (0.80 + 0.20 * np.clip(yy / (H * 0.45), 0, 1))
LW = np.array([0.2126, 0.7152, 0.0722], np.float32)

P = dict(bg_stop=-0.75, bg_sat=0.6, bg_tint=(0.95, 0.99, 1.045), sj_stop=-0.05, sj_sat=0.90,
         sj_tint=(0.99, 1.0, 0.965), contrast=1.10, pivot=0.40, black=0.03, white=0.965, sat=0.95,
         sh_tone=(-0.010, 0.004, 0.014), hi_tone=(0.012, 0.003, -0.012), key=0.35, magenta_fix=0.055)


def lum(x): return x @ LW


def sat(x, s):
    l = lum(x)[..., None]
    return l + (x - l) * s


def curve(x, p):
    # contrast around pivot in a log-ish space, soft shoulder above 0.75
    c = p['pivot'] + (x - p['pivot']) * p['contrast']
    sh = 0.75
    over = np.maximum(c - sh, 0)
    c = np.where(c > sh, sh + (1 - sh) * (1 - np.exp(-over / (1 - sh))), c)
    c = np.clip(c, 0, 1)
    return p['black'] + c * (p['white'] - p['black'])


def grade(rgb, m, p=P):
    m3 = (np.clip(m, 0, 1) ** 1.8)[..., None]
    lin = np.clip(rgb, 0, 1) ** 2.2
    bg = sat(lin * 2 ** p['bg_stop'], p['bg_sat']) * np.array(p['bg_tint'], np.float32)
    sj = sat(lin * 2 ** p['sj_stop'], p['sj_sat']) * np.array(p['sj_tint'], np.float32)
    # pull the iPhone's pink/magenta out of skin: lower R and B a touch vs G where the subject is
    sj = sj * np.array([1 - p['magenta_fix'], 1.0, 1 - p['magenta_fix'] * 0.7], np.float32)
    o = bg * (1 - m3) + sj * m3
    o = o * ((1 - p['key']) + p['key'] * 1.25 * KEY[..., None]) * VIG[..., None]
    o = np.clip(o, 0, None) ** (1 / 2.2)
    o = curve(o, p)
    l = lum(o)[..., None]
    o = o + (1 - l) ** 2 * np.array(p['sh_tone'], np.float32) + l ** 2 * np.array(p['hi_tone'], np.float32)
    o = sat(o, p['sat'])
    return np.clip(o, 0, 1)
