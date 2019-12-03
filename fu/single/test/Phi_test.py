"""
==========================================================================
Phi_test.py
==========================================================================
Test cases for functional unit Phi.

Author : Cheng Tan
  Date : November 27, 2019

"""

from pymtl3 import *
from pymtl3.stdlib.test           import TestSinkCL
from pymtl3.stdlib.test.test_srcs import TestSrcRTL

from ..Phi                        import Phi
from ....lib.opt_type             import *
from ....lib.messages             import *

#-------------------------------------------------------------------------
# Test harness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, FunctionUnit, DataType, src0_msgs, src1_msgs,
                 sink_msgs ):

    s.src_in0   = TestSrcRTL( DataType, src0_msgs   )
    s.src_in1   = TestSrcRTL( DataType, src1_msgs   )
    s.sink_out  = TestSinkCL( DataType, sink_msgs   )

    s.dut = FunctionUnit( DataType )

    connect( s.src_in0.send,   s.dut.recv_in0   )
    connect( s.src_in1.send,   s.dut.recv_in1   )
    connect( s.dut.send_out,   s.sink_out.recv  )

  def done( s ):
    return s.src_in0.done() and s.src_in1.done() and s.sink_out.done()

  def line_trace( s ):
    return s.dut.line_trace()

def run_sim( test_harness, max_cycles=1000 ):
  test_harness.elaborate()
  test_harness.apply( SimulationPass )
  test_harness.sim_reset()

  # Run simulation

  ncycles = 0
  print()
  print( "{}:{}".format( ncycles, test_harness.line_trace() ))
  while not test_harness.done() and ncycles < max_cycles:
    test_harness.tick()
    ncycles += 1
    print( "{}:{}".format( ncycles, test_harness.line_trace() ))

  # Check timeout

  assert ncycles < max_cycles

  test_harness.tick()
  test_harness.tick()
  test_harness.tick()

def test_Phi():
  FU = Phi
  DataType  = mk_data( 16, 1 )
  src_in0   = [ DataType(1, 0), DataType(3, 1), DataType(3, 0) ]
  src_in1   = [ DataType(0, 0), DataType(5, 0), DataType(2, 1) ]
  sink_out  = [ DataType(0, 0), DataType(3, 1), DataType(2, 1) ]
  th = TestHarness( FU, DataType, src_in0, src_in1, sink_out )
  run_sim( th )
