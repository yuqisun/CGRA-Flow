"""
==========================================================================
messages.py
==========================================================================
Collection of messages definition.

Convention: The fields/constructor arguments should appear in the order
            of [ payload_nbits, predicate_nbits ]

Author : Cheng Tan
  Date : Dec 3, 2019
"""
from pymtl3 import *

#=========================================================================
# Generic data message
#=========================================================================

def mk_data( payload_nbits=16, predicate_nbits=1, prefix="CGRAData" ):

  PayloadType   = mk_bits( payload_nbits   )
  PredicateType = mk_bits( predicate_nbits )

  new_name = f"{prefix}_{payload_nbits}_{predicate_nbits}"

  def str_func( s ):
    return f"{s.payload}.{s.predicate}"

  return mk_bitstruct( new_name, {
      'payload'  : PayloadType,
      'predicate': PredicateType,
    },
    namespace = { '__str__': str_func }
  )

#=========================================================================
# Generic config message
#=========================================================================

def mk_ctrl( num_inports=5, num_outports=5, prefix="CGRAConfig" ):

  ctrl_nbits = 5
  CtrlType = mk_bits( ctrl_nbits )
  InportsType  = mk_bits( clog2( num_inports  + 1 ) )
  OutportsType = mk_bits( clog2( num_outports + 1 ) )

  new_name = f"{prefix}_{ctrl_nbits}_{num_inports}_{num_outports}"

  def str_func( s ):
    out_str = ''
    for i in range( num_outports ):
      if i != 0:
        out_str += '|'
      out_str += str(int(s.outport[i]))
    return f"{s.ctrl}|{out_str}"

  field_dict = {}
  field_dict['ctrl'] = CtrlType
  field_dict[ 'outport' ] = [ InportsType for _ in range( num_outports ) ]

  return mk_bitstruct( new_name, field_dict,
    namespace = { '__str__': str_func }
  )

