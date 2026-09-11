"""Design parameters for the Pixel 6a conversion of the Juggernaut MOLLE case.
Same coordinate frame as the original case + mount (mount.stl is never moved).
   X = phone long axis (-X = port end)   Y = width (-Y = button edge)   Z = thickness (+Z = screen)
All phone numbers measured from Pixel6AModel.3mf.
"""
MODEL = "pixel6a"
# ---------------------------------------------------------------- stretch ----
X_SPLIT = 59.50          # inside the mount's tab-free window (56.95 .. 61.93)
DX      = 1.45           # each half moves outward -> +2.90 mm total length

# ------------------------------------------------- phone placement (6a) ------
# phone-frame -> case-frame:  Xc = yp + CX ;  Yc = -xp + CY ;  Zc = zp + CZ
CX, CY, CZ = 46.95, -10.815, -0.90
PH_L, PH_W, PH_T = 152.20, 71.79, 8.90
PH_XN, PH_XP = -25.695, 46.10      # phone-frame body x range
PC_Y = -(PH_XN+PH_XP)/2 + CY       # -21.02, the pocket centre line in Y
PH_YN, PH_YP = -62.70, 89.502      # phone-frame body y range

# ---------------------------------------------- untouched mount interface ----
Y_RAIL_N, Y_RAIL_P = -62.48, 20.45
Y_GRV_N,  Y_GRV_P  = -60.02, 17.98
Z_GRV0,   Z_GRV1   =   1.00,  9.00
Z_BACK_RAIL, Z_BACK_WIN = -3.00, -2.40
RIB_X0, RIB_X1 = 57.44, 61.44

# --------------------------------------------------------------- pocket ------
CLR_SIDE, CLR_END, CLR_TOP = 0.45, 0.60, 0.30
POCK_X0, POCK_X1 = -14.90-DX, 135.60+DX          # -16.35 .. 137.05  (153.40)
POCK_Y0, POCK_Y1 = PC_Y-PH_W/2-CLR_SIDE, PC_Y+PH_W/2+CLR_SIDE   # -57.365 .. 15.325
POCK_Z0, POCK_Z1 = CZ, CZ+PH_T+CLR_TOP           # -0.90 .. 8.30
PH_X0, PH_X1 = POCK_X0+CLR_END, POCK_X0+CLR_END+PH_L
CASE_X1  = 139.90+DX                              # 141.35
ENTRY_X1 = CASE_X1+0.01

# ----------------------------------------------------------- screen opening --
LIP = 3.00
LIP_FILL_Z = 11.90
CHAMF = 1.20

# ------------------------------------------------------------------ camera ---
# visor footprint where it meets the phone's back (z = 0), + clearance
VIS_XN, VIS_XP = -23.228, 43.628          # phone-frame x
VIS_YN, VIS_YP =  61.850, 78.500          # phone-frame y
VIS_PROUD = 1.50                          # how far the visor stands off the back
CAM_CLR = 0.60
CO_X0, CO_X1 = VIS_YN+CX-CAM_CLR, VIS_YP+CX+CAM_CLR       # 108.20 .. 126.05
CO_Y0, CO_Y1 = -VIS_XP+CY-CAM_CLR, -VIS_XN+CY+CAM_CLR     # -55.043 .. 13.013
CO_R = 1.20
Z_VIS_OUT = CZ-VIS_PROUD                  # -2.40, the visor's outer face
# raised shelf across the back that both hoods the visor and carries the slide channel
SHELF_X0 = CO_X0-3.30
SHELF_Y0, SHELF_Y1 = CO_Y0-2.90, CO_Y1+2.90
SHELF_Z  = -4.20
SHELF_TAPER = 1.80
CHAN_Z  = Z_VIS_OUT-0.20                  # -2.60 slide channel floor
CHAN_X0 = CO_X1-1.00

# ----------------------------------------------------------------- buttons ---
BTN_Z0, BTN_Z1 = 3.60+CZ, 6.05+CZ         # 2.70 .. 5.15
VOL_X0, VOL_X1 = 13.52+CX, 33.50+CX       # 60.47 .. 80.45
PWR_X0, PWR_X1 = 41.67+CX, 51.65+CX       # 88.62 .. 98.60
VOL_MID = (VOL_X0+VOL_X1)/2
BTN_PROUD  = 0.40                         # buttons stand 0.40 proud of the body
Y_BTN_FACE = -46.50+CY                    # -57.315
RELIEF_D   = 0.30
Y_RELIEF   = POCK_Y0-RELIEF_D             # -57.665  slide relief for the proud buttons
Z_RELIEF0, Z_RELIEF1 = BTN_Z0-0.45, BTN_Z1+0.45
FLANGE_T   = 0.80
Y_RECESS   = Y_RELIEF-FLANGE_T            # -58.465  flange-recess shoulder
Y_PAD_FACE = -60.95                       # clears the mount's tab tips at -61.10
REC_MX, REC_MZ = 1.20, 1.15
WIN_MX, WIN_MZ = -0.30, 0.40

# -------------------------------------------------------- bottom-end ports ---
WALL_X0, WALL_X1 = -16.90-DX, -14.90-DX   # -18.35 .. -16.35
SPK_Y0, SPK_Y1 = -34.048+CY, -25.057+CY   # -44.863 .. -35.872  speaker grille
USB_Y0, USB_Y1 = -14.392+CY,  -6.013+CY   # -25.207 .. -16.828  USB-C
LFT_Y0, LFT_Y1 =   4.652+CY,  13.643+CY   #  -6.163 ..   2.828  left grille
SPK_Z0, SPK_Z1 = 3.650+CZ, 4.900+CZ       # 2.750 .. 4.000
USB_Z0, USB_Z1 = 2.800+CZ, 5.400+CZ       # 1.900 .. 4.500
LFT_Z0, LFT_Z1 = 3.649+CZ, 4.900+CZ
TOPMIC_Y0, TOPMIC_Y1 = 9.195+CY, 10.195+CY   # -1.620 .. -0.620
TOPMIC_Z0, TOPMIC_Z1 = 4.400+CZ, 5.400+CZ    #  3.500 ..  4.500
