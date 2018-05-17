from migen import *

from litex.soc.interconnect.csr import *


# Pulse Width Modulation
# https://en.wikipedia.org/wiki/Pulse-width_modulation
#     ________              ________
# ___|        |____________|        |___________
#    <-width->
#    <--------period------->

class _PWM(Module, AutoCSR):
    def __init__(self):
        self.enable = enable = Signal()
        self.width = width = Signal(32)
        self.period = period = Signal(32)

        # # #
        self.pwm = pwm = Signal()

        count = Signal(32)

        self.sync += [
            If(enable, 
            	count.eq(count + 1), 

            	If(count > width, 
            		pwm.eq(0)).
            	Else(pwm.eq(1)) ,

            	If(count > period, 
            		count.eq(0))
            ).Else(
                count.eq(0),
                pwm.eq(0)
            )
        ]


class PWM(Module, AutoCSR):
    def __init__(self):
        self.enable = CSRStorage()
        self.width = CSRStorage(32)
        self.period = CSRStorage(32)
        self.pwm_out = pwm_out = Signal()

        # # #

        _pwm = _PWM()
        self.submodules += _pwm

        self.comb += [
            _pwm.enable.eq(self.enable.storage),
            _pwm.width.eq(self.width.storage),
            _pwm.period.eq(self.period.storage),
            pwm_out.eq(_pwm.pwm)
        ]


if __name__ == '__main__':

    dut = _PWM()

    def dut_tb(dut):
        yield dut.enable.eq(1)
        for width in [0, 25, 50, 75, 100]:
            yield dut.width.eq(width)
            yield dut.period.eq(100)
            for i in range(1000):
                yield

    run_simulation(dut, dut_tb(dut), vcd_name="pwm.vcd")
