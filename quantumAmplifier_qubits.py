import qutip as qt
import numpy as np
import matplotlib.pyplot as plt
import math
import time

#Still tunable parameters are
#cool_ext - cooling strength
#w_coupl - coupling resonator frequency
#The control signal

#GUIDELINES:
#ext_freq must be equal to the frequency of the drive qubit to excite it
#ext_strength should be equal to wamp/wstor for the drive qubit to have a frequency equal to the rabi oscillations between these two
#   ext_strength having 2*wamp/wstor or higher allows for the high frequency to excite other qubits such as the storage qubit
#This amplifier works on a perturbative effect, therefore g<1.0 at all times
#   likely will perform better for smaller couplings(supress high order couplings), but will take longer to transfer energy from drive to amp
#cool_ext should be as high as is reasonable
#
#TO DO: test wcoupl=10.5 with ext_strength=1.2 signal=0

timelength = 3000
g = 1.0 #coupling strength
cool_ext = 0.2#cooling strength 0.15

#Strength of the driving tone
global ext_strength
ext_strength = 3#1.25#1.2#wamp/wstor #wdrive/wamp #1.2 or 1.25,has to be 1.25 = wamp/wstor or 1.2 = wdrive/wamp

modes = 4 #number of modes to consider in each resonator


"""Frequencies Format
wamp = gamma #amplification resonator frequency
wdrive = gamma - delta #drive qubit frequency
wstor = gamma + delta #storage qubit frequency
wcool = gamma - 2*delta #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies1
wamp = 5.0 #amplification resonator frequency
wdrive = 6.0 #drive qubit frequency
wstor = 4.0 #storage qubit frequency
wcool = 7.0 #coolant resonator frequency
wcoupl = 0.3#10.5 #coupling resonator frequency
#"""
"""Frequencies2
wamp = 5.0 #amplification resonator frequency
wdrive = 4.0 #drive qubit frequency
wstor = 6.0 #storage qubit frequency
wcool = 3.0 #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies3
wamp = 4.0 #amplification resonator frequency
wdrive = 3.0 #drive qubit frequency
wstor = 5.0 #storage qubit frequency
wcool = 2.0 #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies4
wamp = 10.0 #amplification resonator frequency
wdrive = 9.0 #drive qubit frequency
wstor = 11.0 #storage qubit frequency
wcool = 8.0 #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""
#"""Type 2
#wamp = gamma #amplification resonator frequency
#wdrive = gamma + delta #drive qubit frequency
#wstor = gamma - delta #storage qubit frequency
#wcool = gamma + 2*delta #coolant resonator frequency
#wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies5
wamp = 7.0 #amplification resonator frequency
wdrive = 8.0 #drive qubit frequency
wstor = 6.0 #storage qubit frequency
wcool = 9.0 #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies5
wamp = 6.0 #amplification resonator frequency
wdrive = 8.0 #drive qubit frequency
wstor = 4.0 #storage qubit frequency
wcool = 10.0 #coolant resonator frequency
wcoupl = .301 #coupling resonator frequency
#"""
#"""Frequencies5 BEST!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
delta = 1.5
gamma = 6.0
wamp = gamma #amplification resonator frequency         6.0
wdrive = gamma + delta #drive qubit frequency           7.5
wstor = gamma - delta #storage qubit frequency          4.5
wcool = gamma + 2*delta #coolant resonator frequency    9.0
wcoupl = .3 #coupling resonator frequency
#"""
"""Type 3
gamma = 6.0
delta = 1.5
wamp = gamma #amplification resonator frequency         6.0
wdrive = gamma - delta #drive qubit frequency           4.5
wstor = gamma + delta #storage qubit frequency          7.5
wcool = gamma - 2*delta #coolant resonator frequency    3.0
wcoupl = .3 #coupling resonator frequency
#"""
"""Frequencies6
wamp = 10.0 #amplification resonator frequency
wdrive = 8.0 #drive qubit frequency
wstor = 12.0 #storage qubit frequency
wcool = 6.0 #coolant resonator frequency
wcoupl = .3 #coupling resonator frequency
#"""



#can tune individual coupling to the coupling resonator
g_amp = g
g_drive = g
g_stor = g
g_cool = g

amp_modes = modes
drive_modes = 2
stor_modes = 2
cool_modes = 2
coupl_modes = 2

#anihhilation operators for the resonators
a_amp = qt.tensor(qt.destroy(amp_modes), qt.qeye(drive_modes), qt.qeye(stor_modes), qt.qeye(cool_modes), qt.qeye(coupl_modes))
a_drive = qt.tensor(qt.qeye(amp_modes), qt.destroy(drive_modes), qt.qeye(stor_modes), qt.qeye(cool_modes), qt.qeye(coupl_modes))#sigma minus drive qubit operator
a_stor = qt.tensor(qt.qeye(amp_modes), qt.qeye(drive_modes), qt.destroy(stor_modes), qt.qeye(cool_modes), qt.qeye(coupl_modes))#sigma minus storage qubit operator
a_cool = qt.tensor(qt.qeye(amp_modes), qt.qeye(drive_modes), qt.qeye(stor_modes), qt.destroy(cool_modes), qt.qeye(coupl_modes))
a_coupl = qt.tensor(qt.qeye(amp_modes), qt.qeye(drive_modes), qt.qeye(stor_modes), qt.qeye(cool_modes), qt.destroy(coupl_modes))

#pauli operators for the qubits
sz_drive = qt.tensor(qt.qeye(amp_modes), qt.sigmaz(), qt.qeye(stor_modes), qt.qeye(cool_modes), qt.qeye(coupl_modes))

#drive qubit sigma x operator for external driving
sx_drive = qt.tensor(qt.qeye(amp_modes), qt.sigmax(), qt.qeye(stor_modes), qt.qeye(cool_modes), qt.qeye(coupl_modes))

#noninteracting terms
#       amp resonator            drive qubit          storage qubit       coolant resonator            coupling resonator
noninteracting = wamp*a_amp.dag()*a_amp + wdrive*a_drive.dag()*a_drive + wstor*a_stor.dag()*a_stor + wcool*a_cool.dag()*a_cool + wcoupl*a_coupl.dag()*a_coupl
H_0 = noninteracting# + noninteracting.dag()
#interacting terms
interactions = g_amp*a_amp*a_coupl.dag() + g_drive*a_drive*a_coupl.dag() + g_stor*a_stor*a_coupl.dag() + g_cool*a_cool*a_coupl.dag()#g*(sm_stor.dag()*a_coupl*a_cool.dag()*a_coupl*a_amp*a_coupl.dag()*sm_drive*a_coupl.dag())
#        amp resonator to coupling resonator              drive qubit to coupling resonator                        Storage qubit to coupling resonator             coolant resonator to coupling resonator
H_I = interactions + interactions.dag()
#H_I = 0.8*((a_amp*a_coupl.dag()*sm_drive*a_coupl.dag()*sm_stor.dag()*a_coupl*a_cool.dag()*a_coupl) + (a_amp*a_coupl.dag()*sm_drive*a_coupl.dag()*sm_stor.dag()*a_coupl*a_cool.dag()*a_coupl).dag())#0.8*(a_amp*sm_drive*sm_stor.dag()*a_cool.dag() + a_amp.dag()*sm_drive.dag()*sm_stor*a_cool)#*a_cool.dag()*sm_drive*a_amp#g_amp*(a_amp.dag()*a_coupl + a_amp*a_coupl.dag()) + g_drive*(sm_drive.dag()*a_coupl + sm_drive*a_coupl.dag()) + g_stor*(sm_stor.dag()*a_coupl + sm_stor*a_coupl.dag()) + g_cool*(a_cool.dag()*a_coupl + a_cool*a_coupl.dag())

#external driving tone on drive qubit
ext_freq = wdrive
Drive_X = sx_drive.dag()
Drive_Z = sz_drive#sx_drive.dag()

def H_const_ext_coeff(t, args):
    global ext_strength
    return ext_strength*math.cos(ext_freq*t)


def H_square_ext_coeff(t, args):
    global ext_strength
    if(t < 1):
        return ext_strength*math.cos(ext_freq*t)
    else:
        return 0
    
def ControlSequence0_1(t, args):
    global ext_strength
    if(t < 1):
        return ext_strength*math.cos(ext_freq*t)
    elif(t > 500 and t < 501):
        return ext_strength*math.cos(ext_freq*t)
    
    elif(t > 610 and t < 611):
        return ext_strength*math.cos(ext_freq*t)
    elif(t > 2500 and t < 2501):
        return ext_strength*math.cos(ext_freq*t)
    elif(t > 2610 and t < 2611):
        return ext_strength*math.cos(ext_freq*t)
    else:
        return 0

H = [(H_0+H_I), [Drive_X, ControlSequence0_1]]

#starting state with amplification resonator empty
psi0 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [0,0,0,0,0])
#starting state with an excitation in the amplification resonator
psi1 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [1,0,0,0,0])

psidrive0 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [0,1,0,0,0])
psidrive1 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [1,1,0,0,0])

psidrivestorage0 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [0,1,1,0,0])
psidrivestorage1 = qt.basis([amp_modes,drive_modes,stor_modes,cool_modes,coupl_modes], [1,1,1,0,0])


tlist = np.linspace(0, timelength, timelength + 1)
#print(tlist)

print("Begining Simulation...")
print()
for state in [1]:# no-signal = 0, signal = 1
    starttime = time.time()
    print("Starting State "+str(state))
    #                                   cooling        [0]photons in amp  [1]photons in drive      [2]photons in storage  [3]coolant photons   [4]photons in coupler
    if(state == 0):
        res = qt.mesolve(H, psi0, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])
    elif(state == 1):    
        res = qt.mesolve(H, psi1, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])

    elif(state == 2):    
        res = qt.mesolve(H, psidrive0, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])
    elif(state == 3):    
        res = qt.mesolve(H, psidrive1, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])
    elif(state == 4):    
        res = qt.mesolve(H, psidrivestorage0, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])
    elif(state == 5):    
        res = qt.mesolve(H, psidrivestorage1, tlist, [cool_ext*a_cool], [a_amp.dag()*a_amp, a_drive.dag()*a_drive, a_stor.dag()*a_stor, a_cool.dag()*a_cool, a_coupl.dag()*a_coupl])

    plt.scatter(tlist, res.expect[4], c="c", marker="o", label="coupling qubit")
    plt.scatter(tlist, res.expect[3], c="y", marker="o", label="coolant qubit")
    plt.scatter(tlist, res.expect[1], c="b", marker="o", label="drive qubit")
    plt.scatter(tlist, res.expect[2], c="g", marker="o", label="storage qubit")
    plt.scatter(tlist, res.expect[0], c="r", marker="x", label="signal resonator")
    plt.xlabel("Time"), plt.ylabel("Photon number")
    plt.legend()
    if(state == 0):
        plt.savefig("NoSignal_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")
    elif(state == 1):
        plt.savefig("Signal_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")

    elif(state == 2):
        plt.savefig("Drive0_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")
    elif(state == 3):
        plt.savefig("Drive1_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")
    elif(state == 4):
        plt.savefig("DriveStorage0_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")
    elif(state == 5):
        plt.savefig("DriveStorage1_wcoupl"+str(wcoupl)+"__g"+str(g)+"__ext_strength"+str(ext_strength)+"_len_"+str(timelength)+"_coolext_"+str(cool_ext)+".png")
    
    plt.close()
    print("Done with state="+str(state))
    print("took "+str(time.time()-starttime))
    print()
print("FINISHED")