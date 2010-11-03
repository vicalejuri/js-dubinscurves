#!/usr/bin/python
from ctypes import *

lib = CDLL('../libdubinspaths.so')
inf = float('inf')

class DubinsPath(Structure):
    _fields_ = [('qi',    c_double * 3),
                ('params', c_double * 3),
                ('type',  c_int)]

def createDubinsFunction( name ):
    func = getattr(lib, name)
    def res( alpha, beta, d ):
        output = (c_double * 3)(inf, inf, inf)
        print output[:]
        func( c_double(alpha), c_double(beta), c_double(d), output )
        return output[:]
    return res

LRL = createDubinsFunction( 'dubins_LRL' )
RLR = createDubinsFunction( 'dubins_RLR' )
LSL = createDubinsFunction( 'dubins_LSL' )
LSR = createDubinsFunction( 'dubins_LSR' )
RSL = createDubinsFunction( 'dubins_RSL' )
RSR = createDubinsFunction( 'dubins_RSR' )

def dubinsInitNormalised( alpha, beta, d ):
    path = DubinsPath()
    lib.dubins_init_normalised( c_double(alpha), c_double(beta), c_double(d), pointer(path) );
    return path

def dubinsNormalised2( alpha, beta, d ):
    funcs = [ LRL, RLR, LSL, LSR, RSL, RSR ]
    outs  = [ fun(alpha,beta,d) for fun in funcs ]
    lens  = [ sum(o) for o in outs ]
    for f, o, l in zip(funcs,outs,lens):
        print f, o, l    

dubinsNormalised2( 1., 1., 5. )
path = dubinsInitNormalised( 1., 1., 5. )
print path.type
print path.qi[:]
print path.params[:]
