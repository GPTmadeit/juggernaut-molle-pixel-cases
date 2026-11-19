"""Design parameters for the Pixel 10 conversion of the Juggernaut MOLLE case.

The Pixel 10 shares the 9 Pro's footprint (152.8 x 72.0), so this kit is derived from the
finished Pixel 9 Pro kit rather than from the S8 original: the stretch, mount groove, rib,
T-slots and end caps are inherited unchanged, and only the phone-facing features that differ
are refilled and recut.

Phone numbers measured from Pixel10.stl (Jan Vejtasa, Printables 1391738), cross-checked
against "Google Pixel 10 Model.step" (Jumpbase, Printables 1538957).  Both agree on the
outline, the camera bar and the bottom-edge ports to within 0.5 mm.
Case frame is the original mount frame; mount.stl never moves.
"""
MODEL = "pixel10"
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pixel9pro"))
import params9p as P9                         # the base kit

DX = P9.DX                                    # same stretch as the 9 Pro (+3.50 mm)

# ------------------------------------------------ phone placement (Pixel 10) --
# native STL: buttons on x=0, camera near y=L.  Rotate 180 deg about Z first so it matches
# the 9 Pro's native layout (buttons at +x, camera near y=0), then the 9 Pro mapping:
#   Xc = -yp + CX ;  Yc = -xp + CY ;  Zc = -zp + CZ
NAT_W, NAT_L = 72.46, 152.80                  # native bounds incl. the 0.50 mm proud buttons
CX, CY = P9.CX, P9.CY                         # 136.75, 14.98
CZ = 7.70                                     # 9 Pro 7.60: phone is 0.1 mm thicker, back stays on the floor
PH_L, PH_W, PH_T = 152.80, 71.96, 8.59
def Xc(y_native): return y_native - NAT_L + CX     # = y - 16.05
def Yc(x_native): return x_native - NAT_W + CY     # = x - 57.48
def Zc(z_native): return -z_native + CZ

# --------------------------------------------------------------- pocket ------
CLR_TOP  = 0.30
POCK_X0, POCK_X1 = P9.POCK_X0, P9.POCK_X1          # -16.65 .. 137.35
POCK_Y0, POCK_Y1 = P9.POCK_Y0, P9.POCK_Y1          # -57.47 .. 15.43
POCK_Z0 = P9.POCK_Z0                               # -0.90 (floor unchanged)
POCK_Z1 = Zc(0.0) + CLR_TOP                        #  8.00 (9 Pro 7.90)
# the two reference models disagree on the corner radius (R12 vs R10); cut the pocket
# for the tighter one so either fits -- costs 0.8 mm of extra gap at each corner if R12.
POCK_R  = 10.00 + P9.CLR_SIDE                      # 10.45
CASE_X1, ENTRY_X1 = P9.CASE_X1, P9.ENTRY_X1

# ------------------------------------------------------------------ camera ---
# camera bar (native): x 4.00..68.96, y 116.03..138.91, top z 12.00 on a 8.59 back
BAR_X = (4.00, 68.96); BAR_Y = (116.03, 138.91)
BAR_PROUD = 12.00 - PH_T                            # 3.41
BAR_R = (BAR_Y[1]-BAR_Y[0])/2                       # pill: full-round ends, R 11.44
CAM_CLR = 0.70
CO_X0, CO_X1 = Xc(BAR_Y[0])-CAM_CLR, Xc(BAR_Y[1])+CAM_CLR    # 99.28 .. 123.56
CO_Y0, CO_Y1 = Yc(BAR_X[0])-CAM_CLR, Yc(BAR_X[1])+CAM_CLR    # -54.18 .. 12.18
CO_R = BAR_R + CAM_CLR
Z_BAR_OUT = POCK_Z0 - BAR_PROUD                              # -4.31
SHELF_X0 = CO_X0 - 3.20                                      # 96.08 (taper base, before clipping)
SHELF_X_LIMIT = P9.SHELF_X0                                  # 97.49: the adapter's arms are just below this
SHELF_Y0, SHELF_Y1 = CO_Y0 - 2.50, CO_Y1 + 2.50
SHELF_Z, SHELF_TAPER = P9.SHELF_Z, P9.SHELF_TAPER            # -6.00, 2.20
CHAN_Z  = P9.CHAN_Z                                          # -4.62 -- keep the 9 Pro channel floor
CHAN_X0 = CO_X0 - 0.50
Z_BACK_WIN = P9.Z_BACK_WIN

# ----------------------------------------------------------------- buttons ---
# native: volume y 70.11..91.10, power y 98.03..110.19, z 2.65..5.94, 0.50 mm proud on x=0
BTN_Z0, BTN_Z1 = Zc(5.94), Zc(2.65)          # 1.76 .. 5.05
VOL_X0, VOL_X1 = Xc(70.11), Xc(91.10)        # 54.06 .. 75.05
PWR_X0, PWR_X1 = Xc(98.03), Xc(110.19)       # 81.98 .. 94.14
VOL_MID = (VOL_X0+VOL_X1)/2
Y_BTN_FACE = Yc(0.0)                         # -57.48
RELIEF_D   = P9.RELIEF_D
Y_RELIEF   = POCK_Y0 - RELIEF_D              # -57.82
Z_RELIEF0, Z_RELIEF1 = BTN_Z0-0.45, BTN_Z1+0.45
FLANGE_T, Y_RECESS, Y_PAD_FACE = P9.FLANGE_T, P9.Y_RECESS, P9.Y_PAD_FACE
REC_MX, REC_MZ, WIN_MX, WIN_MZ = P9.REC_MX, P9.REC_MZ, P9.WIN_MX, P9.WIN_MZ
Y_RAIL_N, Y_GRV_N = P9.Y_RAIL_N, P9.Y_GRV_N

# -------------------------------------------------------- bottom-end ports ---
WALL_X0, WALL_X1 = P9.WALL_X0, P9.WALL_X1    # -18.65 .. -16.65
# native (bottom face y=0): grille x 14.31..23.69 and 49.27..58.65 at z 3.50..5.09,
#                           USB-C x 32.29..40.68 at z 2.99..5.59
GRL_A = (Yc(14.31), Yc(23.69)); GRL_B = (Yc(49.27), Yc(58.65))   # -43.17..-33.79 / -8.21..1.17
GRL_Z = (Zc(5.09), Zc(3.50))                                      #  2.61 .. 4.20
USB_Y = (Yc(32.29), Yc(40.68)); USB_Z = (Zc(5.59), Zc(2.99))      # -25.19..-16.80 / 2.11..4.71
# top face mic, native x 12.50..13.79 z 3.65..4.94 -> Y -44.98..-43.69: inside the stock
# top-cap vent (Y -46.54..-43.54), same as the 9 Pro, so the top cap needs no new hole.
TOPMIC_Y = (Yc(12.50), Yc(13.79))

# the 9 Pro bottom cap's port wall (file frame) and the cable cap's, which is exported 38.42 mm off
CAP_P0, CAP_P1 = -21.03-DX, -17.40-DX
USB_OFFSET = 38.42
