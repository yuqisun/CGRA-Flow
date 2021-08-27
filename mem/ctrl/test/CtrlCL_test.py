"""
==========================================================================
CtrlCL_test.py
==========================================================================
Test cases for control memory.

Author : Cheng Tan
  Date : Dec 21, 2019

"""

from pymtl3 import *
from pymtl3.stdlib.test           import TestSinkCL
from pymtl3.stdlib.test.test_srcs import TestSrcRTL

from ....fu.single.AdderRTL       import AdderRTL
from ..CtrlMemCL                  import CtrlMemCL
from ....lib.opt_type             import *
from ....lib.messages             import *

#-------------------------------------------------------------------------
# Test harness
#-------------------------------------------------------------------------

class TestHarness( Component ):

  def construct( s, MemUnit, DataType, ConfigType, ctrl_mem_size, data_mem_size,
                 src0_msgs, src1_msgs, ctrl_msgs, sink_msgs ):

    AddrType = mk_bits( clog2( ctrl_mem_size ) )

    s.src_data0 = TestSrcRTL( DataType,   src0_msgs  )
    s.src_data1 = TestSrcRTL( DataType,   src1_msgs  )
    s.sink_out  = TestSinkCL( DataType,   sink_msgs  )

    s.alu       = AdderRTL( DataType, ConfigType, 2, 2, data_mem_size )
    s.ctrl_mem  = MemUnit( ConfigType, ctrl_mem_size, len(ctrl_msgs), ctrl_msgs )

    connect( s.alu.recv_opt,   s.ctrl_mem.send_ctrl  )

    connect( s.src_data0.send, s.alu.recv_in[0]      )
    connect( s.src_data1.send, s.alu.recv_in[1]      )
    connect( s.alu.send_out[0],  s.sink_out.recv     )

  def done( s ):
    return s.src_data0.done() and s.src_data1.done() and\
           s.sink_out.done()

  def line_trace( s ):
    return s.alu.line_trace() + " || " +s.ctrl_mem.line_trace()

def run_sim( test_harness, max_cycles=100 ):
  test_harness.elaborate()
  test_harness.apply( SimulationPass() )
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

def test_PseudoCtrl():
  MemUnit       = CtrlMemCL
  DataType      = mk_data( 16, 1 )
  CtrlType      = mk_ctrl()
  ctrl_mem_size = 8
  data_mem_size = 8
  num_inports   = 2
  FuInType      = mk_bits( clog2( num_inports + 1 ) )
  pickRegister  = [ FuInType( x+1 ) for x in range( num_inports ) ]
  AddrType      = mk_bits( clog2( ctrl_mem_size ) )
  src_data0     = [ DataType(1,1), DataType(5,1), DataType(7,1), DataType(6,1) ]
  src_data1     = [ DataType(6,1), DataType(1,1), DataType(2,1), DataType(3,1) ]
  src_wdata     = [ CtrlType( OPT_ADD, b1( 0 ), pickRegister ),
                    CtrlType( OPT_SUB, b1( 0 ), pickRegister ),
                    CtrlType( OPT_SUB, b1( 0 ), pickRegister ),
                    CtrlType( OPT_ADD, b1( 0 ), pickRegister ) ]
  sink_out      = [ DataType(7,1),DataType(4,1),DataType(5,1),DataType(9,1)]
  th = TestHarness( MemUnit, DataType, CtrlType, ctrl_mem_size, data_mem_size,
                    src_data0, src_data1, src_wdata, sink_out )
  run_sim( th )

