"""All design parameters for the Pixel 9a conversion of the Juggernaut MOLLE case.
Coordinate frame = the original case/mount frame (mount.stl is NEVER moved).
   X = phone long axis  (-X = bottom / port end,  +X = top)
   Y = phone width axis (-Y = phone's right side / buttons,  +Y = phone's left side)
   Z = thickness        (-Z = back / mount side,  +Z = front / screen)
"""
# ---------------------------------------------------------------- stretch ----
X_SPLIT = 59.50      # split plane: inside the mount's tab-free window (56.95..61.93)
DX      = 2.70       # each half moves outward by this  -> +5.40 mm total length

# ------------------------------------------------- phone placement (Pixel 9a) --
# phone-frame -> case-frame:  Xc = yp + CX ;  Yc = -xp + CY ;  Zc = zp + CZ
CX, CY, CZ = 60.35, -21.02, -0.90
PH_L, PH_W, PH_T, PH_R = 154.70, 73.30, 8.90, 12.027   # length, width, thickness, corner R

# ---------------------------------------------- untouched mount interface ----
Y_RAIL_N, Y_RAIL_P = -62.48, 20.45     # outer rail faces
Y_GRV_N,  Y_GRV_P  = -60.02, 17.98     # side-groove floors (mount retention tabs live here)
Z_GRV0,   Z_GRV1   =   1.00,  9.00     # side-groove height (z=1.00 shoulder = the snap ledge)
Z_BACK_RAIL, Z_BACK_WIN = -3.00, -2.40 # rail underside / recessed back-window floor
RIB_X0, RIB_X1 = 57.44, 61.44          # groove rib - MUST stay inside mount gap 56.95..61.93

# --------------------------------------------------------------- the pocket ---
CLR_SIDE, CLR_END, CLR_TOP = 0.45, 0.60, 0.30
POCK_X0, POCK_X1 = -14.90-DX, 135.60+DX          # -17.60 .. 138.30  (155.90)
POCK_Y0, POCK_Y1 = CY-PH_W/2-CLR_SIDE, CY+PH_W/2+CLR_SIDE   # -58.12 .. 16.08
POCK_Z0 = CZ                                     # -0.90 pocket floor
POCK_Z1 = CZ+PH_T+CLR_TOP                        #  8.30 lip underside
POCK_R  = PH_R+CLR_SIDE                          # 12.48

PH_X0, PH_X1 = POCK_X0+CLR_END, POCK_X0+CLR_END+PH_L      # -17.00 .. 137.70
PH_Y0, PH_Y1 = CY-PH_W/2, CY+PH_W/2                       # -57.67 .. 15.63

# ---------------------------------------------------------- screen opening ---
LIP = 3.00
OPEN_X0, OPEN_X1 = POCK_X0+LIP, POCK_X1-LIP        # keep 3 mm side lip
OPEN_Y0, OPEN_Y1 = POCK_Y0+LIP, POCK_Y1-LIP
OPEN_R = POCK_R-LIP
LIP_FILL_Z = 11.90        # top of the lip fill (matches original lip inner top edge)
CHAMF = 1.20              # 45 deg chamfer around the screen opening

# ------------------------------------------------------------------ camera ---
CAM_X0, CAM_X1 = 44.73+CX, 62.73+CX        # 105.08 .. 123.08
CAM_Y0, CAM_Y1 = -29.35+CY, 1.85+CY        # -50.37 .. -19.17
CAM_CLR = 0.75
CO_X0, CO_X1 = CAM_X0-CAM_CLR, CAM_X1+CAM_CLR
CO_Y0, CO_Y1 = CAM_Y0-CAM_CLR, CAM_Y1+CAM_CLR
CO_R = 9.00+CAM_CLR
HOOD_W, HOOD_DEPTH, HOOD_FOOT = 3.00, 2.20, 0.80   # rim width / how far it stands proud / foot
Z_HOOD = Z_BACK_WIN-HOOD_DEPTH                     # -4.60
BUMP_H = 0.60                                      # camera bar stands 0.6 proud of the phone back
CHAN_Z = POCK_Z0-BUMP_H-0.10                       # -1.60  slide-in channel floor
CHAN_X0 = CO_X0-0.5
CASE_X1 = 139.90+DX          # 142.60, the case's +X end
ENTRY_X1 = CASE_X1+0.01      # cut the pocket profile straight out through the top-cap socket
BOSS_X0, BOSS_X1 = 128.50, 139.90+DX+0.01
WIN_EXT = (-57.60, -55.00)   # widen the recessed back window so the lens cap has a flat seat
BOSS_PAD = 1.50

# ----------------------------------------------------------------- buttons ---
BTN_Z0, BTN_Z1 = 2.95+CZ, 5.95+CZ          # 2.05 .. 5.05 (phone button band)
VOL_X0, VOL_X1 = -6.65+CX, 15.35+CX        # 53.70 .. 75.70
PWR_X0, PWR_X1 = 22.35+CX, 34.35+CX        # 82.70 .. 94.70
VOL_MID = (VOL_X0+VOL_X1)/2
BTN_PROUD = 0.60                            # buttons stand 0.6 proud of the phone body
Y_RELIEF   = POCK_Y0-0.40                   # -58.52 slide relief for the proud buttons
Z_RELIEF0, Z_RELIEF1 = BTN_Z0-0.45, BTN_Z1+0.45
Y_RECESS   = -59.32                         # flange recess floor
Y_PAD_FACE = -60.95                         # pad face - clears mount tab tip at -61.10
FLANGE_T   = 0.95
REC_MX, REC_MZ = 1.20, 1.15                 # recess margin around the button in X / Z
WIN_MX, WIN_MZ = -0.30, 0.40                # window margin (negative = inset from button)
FIT = 0.15                                  # insert-to-recess clearance

# ------------------------------------------------------- bottom-end ports ----
WALL_X0, WALL_X1 = -16.90-DX, -14.90-DX     # -19.60 .. -17.60  (port end wall, 2.0 mm)
SPK_Y0, SPK_Y1 = -25.25+CY, -11.25+CY       # -46.27 .. -32.27  speaker grille
USB_Y0, USB_Y1 =  -4.25+CY,   4.25+CY       # -25.27 .. -16.77  USB-C
MIC_Y0, MIC_Y1 =   6.75+CY,   7.75+CY       # -14.27 .. -13.27  bottom mic
LFT_Y0, LFT_Y1 =  10.25+CY,  25.25+CY       # -10.77 ..   3.73  left grille
PORT_Z_MID = 4.45+CZ                        # 3.55  centre of the bottom-edge features
