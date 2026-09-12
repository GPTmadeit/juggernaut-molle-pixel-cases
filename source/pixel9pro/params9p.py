"""Design parameters for the Pixel 9 Pro conversion of the Juggernaut MOLLE case.
Phone numbers measured from pixel_9_pro.stl (the1dynasty, Thingiverse 6746749),
scaled x1000 (the file is in metres) and parked at the origin.
Cross-checked against the Google Pixel 9 Pro XL STEP (GrabCAD, Sri Ram) for the
bottom-edge port layout.  Case frame is the original mount frame; mount.stl never moves.
"""
MODEL = "pixel9pro"
# ---------------------------------------------------------------- stretch ----
X_SPLIT = 59.50
DX      = 1.75                       # +3.50 mm total length

# ------------------------------------------------ phone placement (9 Pro) ----
# phone-frame -> case-frame:  Xc = -yp + CX ;  Yc = -xp + CY ;  Zc = -zp + CZ   (det +1)
CX, CY, CZ = 136.75, 14.98, 7.60
PH_L, PH_W, PH_T = 152.80, 72.00, 8.50
PH_R = 12.00                          # body corner radius (3 of 4 corners fit to 0.005 mm)

# ---------------------------------------------- untouched mount interface ----
Y_RAIL_N, Y_RAIL_P = -62.48, 20.45
Y_GRV_N,  Y_GRV_P  = -60.02, 17.98
Z_GRV0,   Z_GRV1   =   1.00,  9.00
Z_BACK_RAIL, Z_BACK_WIN = -3.00, -2.40
RIB_X0, RIB_X1 = 57.44, 61.44

# --------------------------------------------------------------- pocket ------
CLR_SIDE, CLR_END, CLR_TOP = 0.45, 0.60, 0.30
POCK_X0, POCK_X1 = -14.90-DX, 135.60+DX            # -16.65 .. 137.35 (154.00)
PC_Y = -21.02
POCK_Y0, POCK_Y1 = PC_Y-PH_W/2-CLR_SIDE, PC_Y+PH_W/2+CLR_SIDE    # -57.47 .. 15.43
POCK_Z0, POCK_Z1 = -0.90, -0.90+PH_T+CLR_TOP       # -0.90 .. 7.90
POCK_R = PH_R+CLR_SIDE                             # 12.45
PH_X0, PH_X1 = POCK_X0+CLR_END, POCK_X0+CLR_END+PH_L
CASE_X1  = 139.90+DX                               # 141.65
ENTRY_X1 = CASE_X1+0.01

# ----------------------------------------------------------- screen opening --
LIP = 3.00
OPEN_X0, OPEN_X1 = POCK_X0+LIP, POCK_X1-LIP
OPEN_Y0, OPEN_Y1 = POCK_Y0+LIP, POCK_Y1-LIP
OPEN_R = POCK_R-LIP
LIP_FILL_Z = 11.90
CHAMF = 1.20

# ------------------------------------------------------------------ camera ---
# camera bar: 64.44 x 21.50, R 10.45, standing 3.52 mm proud of the phone's back
BAR_XN, BAR_XP =  3.78, 68.22        # phone-frame x
BAR_YN, BAR_YP = 13.86, 35.36        # phone-frame y
BAR_PROUD = 3.52
CAM_CLR = 0.70
CO_X0, CO_X1 = -BAR_YP+CX-CAM_CLR, -BAR_YN+CX+CAM_CLR     # 100.69 .. 123.59
CO_Y0, CO_Y1 = -BAR_XP+CY-CAM_CLR, -BAR_XN+CY+CAM_CLR     # -53.94 .. 11.90
CO_R = 10.45+CAM_CLR
Z_BAR_OUT = POCK_Z0-BAR_PROUD                             # -4.42
# raised camera shelf: hoods the bar and carries the slide-in channel
SHELF_X0 = CO_X0-3.20
SHELF_Y0, SHELF_Y1 = CO_Y0-2.50, CO_Y1+2.50
SHELF_Z  = -6.00
SHELF_TAPER = 2.20
CHAN_Z  = Z_BAR_OUT-0.20                                   # -4.62 (plate stays 1.38 mm)
CHAN_X0 = CO_X0-0.50   # the channel must span the whole opening: the pill ends narrow in Y

# ----------------------------------------------------------------- buttons ---
BTN_Z0, BTN_Z1 = -5.77+CZ, -2.78+CZ         # 1.83 .. 4.82
VOL_X0, VOL_X1 = -82.51+CX, -60.62+CX       # 54.24 .. 76.13
PWR_X0, PWR_X1 = -53.61+CX, -41.75+CX       # 83.14 .. 95.00
VOL_MID = (VOL_X0+VOL_X1)/2
BTN_PROUD  = 0.47
Y_BTN_FACE = -72.47+CY                      # -57.49
RELIEF_D   = 0.35
Y_RELIEF   = POCK_Y0-RELIEF_D               # -57.82
Z_RELIEF0, Z_RELIEF1 = BTN_Z0-0.45, BTN_Z1+0.45
FLANGE_T   = 0.80
Y_RECESS   = Y_RELIEF-FLANGE_T              # -58.62
Y_PAD_FACE = -60.95
REC_MX, REC_MZ = 1.20, 1.15
WIN_MX, WIN_MZ = -0.30, 0.40

# -------------------------------------------------------- bottom-end ports ---
WALL_X0, WALL_X1 = -16.90-DX, -14.90-DX     # -18.65 .. -16.65
def _y(xp): return -xp+CY
def _z(zp): return -zp+CZ
SPK_Y0, SPK_Y1 = _y(24.67), _y(10.36)       #  -9.69 ..  4.62  speaker grille
USB_Y0, USB_Y1 = _y(40.41), _y(31.59)       # -25.43 .. -16.61  USB-C (dead centre)
MIC_Y0, MIC_Y1 = _y(48.57), _y(47.32)       # -33.59 .. -32.34  mic
AUX_Y0, AUX_Y1 = _y(65.11), _y(64.02)       # -50.13 .. -49.04  second port hole
SPK_Z0, SPK_Z1 = _z(5.14), _z(3.84)         #  2.46 ..  3.76
USB_Z0, USB_Z1 = _z(5.85), _z(3.22)         #  1.75 ..  4.38
MIC_Z0, MIC_Z1 = _z(5.14), _z(3.89)
AUX_Z0, AUX_Z1 = _z(5.13), _z(4.03)
TOPMIC_Y0, TOPMIC_Y1 = _y(60.20), _y(59.00) # -45.22 .. -44.02  (falls inside the stock top-cap vent)
TOPMIC_Z0, TOPMIC_Z1 = _z(4.99), _z(3.79)
