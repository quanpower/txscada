# encoding: utf-8
#===============================================================================
# Mara Protocol Structures
#===============================================================================
from construct import *
from datetime import datetime
from utils.checksum import make_cs_bigendian
from utils.bitfield import bitfield
#===============================================================================
# Adapters
#===============================================================================
class EnergyValueAdapter(Adapter):
    """Energy qualifier is stored in it's first two bits"""
    MAX_ENERGY_VALUE = 2**15 # Solo 14 bits posibles
    MAX_Q_VALUE = 5 # Solo 5 bits
    
    def _encode(self, obj, context):
        '''Validates input values'''
        try:
            val, q = obj['val'], obj['q']
        except (AttributeError, TypeError):
            raise ValueError("Can't get item 'val' or 'q' from %s, is it a construct.Container?" % obj)
        assert 0 <= val < self.MAX_ENERGY_VALUE
        assert 0 <= q <= self.MAX_Q_VALUE
        data = bitfield(0)
        data[0:14] = obj['val']
        data[14:16] = obj['q']
        return int(data)
    
    def _decode(self, int_val, context):
        data = bitfield(int_val)
        retval = Container(val=data[0:14], q=data[14:16]) 
        return retval

class MaraDateTimeAdapter(Adapter):
    '''
    Mara bytes <--> datetime.datetime
    '''
    def _decode(self, obj, context):
        return datetime(obj.year+2000, obj.month, obj.day, obj.hour, obj.minute, obj.second)
    
    def _encode(self, obj, context):
        return Container(year=obj.year-2000, month=obj.month, day=obj.day, 
                         hour=obj.hour, minute=obj.minute, second=obj.second)
        
class SubSecondAdapter(Adapter):
    '''Mara timestamp sub-second data is measured in 1/32 second steps,
    and its value is given by a counter which goes from 0 to 0x7FFF'''
    def _encode(self, obj, context):
        raise AdaptationError("Cant encode yet :(")
    
    def _decode(self, obj, context):
        return obj / float(32768)
    
def subsecond(name):
    return SubSecondAdapter
#===============================================================================
# Mara protocol SubConstructs
#===============================================================================

TCD = BitStruct('TCD',
    Enum(BitField("evtype", 2),
         DIGITAL=0,
         ENERGY=1,
         INVALID_2=2,
         INVALID_3=3
    ),
    BitField("q", 2),
    BitField("addr485", 4),
)


BPE = BitStruct('BPE',
    BitField("bit", 4),
    BitField("port", 3),
    BitField("status", 1),
)

IdleCan = BitStruct('idlecan',
    BitField('idle', 5),
    BitField('channel', 3) 
)

TimerTicks = Struct('ticks', 
    #UBInt8('cseg'),
    #UBInt8('dmseg'),
    ULInt16('ticks')
)

Value = BitStruct('val', 
    BitField('q', length=2, ),
    BitField('value', length=14,)
)


DateTime = Struct('datetime',
    UBInt8('year'),
    UBInt8('month'),
    UBInt8('day'),
    UBInt8('hour'),
    UBInt8('minute'),
    UBInt8('second'),
)

Event = Struct("event",
    Embed(TCD),
    Switch("evdetail", lambda ctx: ctx.evtype,  
           {
            "DIGITAL": Embed(BPE),
            "ENERGY":  Embed(IdleCan),
            }
    ),
    # TODO: Python datetime <-> mara bytes
    #MaraDateTimeAdapter(Embed(DateTime)), 
    
    UBInt8('year'),
    UBInt8('month'),
    UBInt8('day'),
    UBInt8('hour'),
    UBInt8('minute'),
    UBInt8('second'),
    
    If(lambda ctx: ctx['evtype'] == "DIGITAL",
       #Embed(SubSecondAdapter(ULInt16('ticks'))),
       SubSecondAdapter(ULInt16('subsec'))
    ),
          
    If(lambda ctx: ctx.evtype == "ENERGY",
       EnergyValueAdapter(ULInt16('value')),
    ),           
    
    
    #Switch("taildata", lambda ctx: ctx.evtype, {
    #    "DIGITAL": ULInt16('ticks'),
    #    #"ENERGY":  EnergyValueAdapter(ULInt16('copete')),
    #    "ENERGY":  ULInt16('value'),
    #}, default = Pass),
)

#===============================================================================
# Payload del comando 10 - Encuesta de energías al COMaster
#===============================================================================
Payload_10 = Struct("payload_10",
    ULInt8('canvarsys'),
    Array(lambda ctx: ctx.canvarsys / 2, ULInt16('varsys')),
    ULInt8('candis'),
    Array(lambda ctx: ctx.candis / 2, ULInt16('dis')),
    ULInt8('canais'),
    Array(lambda ctx: ctx.canais / 2, ULInt16('ais')),
    ULInt8('canevs'),
    Array(lambda ctx: ctx.canevs / 10, Event),
)
#===============================================================================
# Paquete Mara 14
#===============================================================================
MaraFrame = Struct('Mara', 
            ULInt8('sof'),
            ULInt8('length'),
            ULInt8('dest'),
            ULInt8('source'),
            ULInt8('sequence'),
            ULInt8('command'),
            Optional(Payload_10),
            ULInt16('bcc')
)


def ints2buffer(hexstr):
    '''
    '''
    parts = [ chr(an_int) for an_int in hexstr ]
    return ''.join(parts)

def hexstr2buffer(a_str):        
    '''
    "FE  01" => '\xFE\x01'    
    '''
    import re
    a_str = a_str.strip().replace('\n', ' ')
    a_list = [ chr(int(bytestr, 16)) for bytestr in  re.split('[:\s]', a_str) if len(bytestr) ]
    return ''.join(a_list)

def any2buffer(data):
    if isinstance(data, list):
        return ints2buffer(data)
    elif isinstance(data, basestring):
        return hexstr2buffer(data)
    raise Exception("%s can't be converted to string buffer")

# Buffer -> Upper Human Readable Hex String
upperhexstr = lambda buff: ' '.join([ ("%.2x" % ord(c)).upper() for c in buff])

def dtime2dict(dtime = None):
    '''
    Converts a datetime.datetime instance into
    a dictionary suitable for ENERGY event
    timestamp
    '''
    import datetime
    if not dtime:
        dtime = datetime.datetime.now()
    d = {}
    d['year']   = dtime.year % 100 
    d['month']  = dtime.month
    d['day']    = dtime.day
    d['hour']   = dtime.hour
    d['minute'] = dtime.minute
    d['second'] = dtime.second
    # Ticks de cristal que va de 0 a 32K-1 en un segundo
    d['ticks'] = dtime.microsecond * (float(2<<14)-1) / 1000000
    return d    


def build_frame(obj, subcon=MaraFrame):
    '''Generates a mara frame, with checksum and qty'''
    stream = subcon.build(obj)
    data= "".join([
                    stream[0],
                    UBInt8('qty').build(len(stream)),
                    stream[2:-2],
                    ])
    cs = make_cs_bigendian(data)
    cs_str = Array(2, Byte('cs')).build(cs)
    return "".join((data, cs_str))

def parse_frame(buff, as_hex_string=False):
    if as_hex_string:
        buff = hexstr2buffer(buff)
    data = MaraFrame.parse(buff)
    return data

def format_frame(buff, as_hex_string=False):
    d = parse_frame(buff, as_hex_string)
    print "SOF:", d.sof
    print "QTY:", d.length
    print "DST:", d.dest
    print "SRC:", d.source
    print "SEQ:", d.sequence
    print "CMD:", d.command
    # Payload
    if d.payload_10:
        p = d.payload_10
        print "%12s" % "CANVARSYS:", p.canvarsys, "%d valores de word de 16" % (p.canvarsys/2)
        print "%12s" % "VARSYS:",    p.varsys 
        print "%12s" % "CANDIS:",    p.candis, "%d valores de word de 16" % (p.candis/2) 
        print "%12s" % "DIS:", p.dis
        print "%12s" % "CANAIS:", p.candis, "%d valores de word de 16" % (p.canais/2)
        print "%12s" % "DIS:", p.ais
        # Eventos
        print "%12s" % "CANEVS:", p.canevs, "%d cada evento ocupa 10 bytes" % (p.canevs/10)
        for ev in p.event:
            if ev.evtype == "DIGITAL":
                print '\t',
                print "DIGITAL",
                print "Q:", ev.q, 
                print "ADDR485", ev.addr485, 
                print "BIT:", ev.bit,
                print "PORT:", ev.port,
                print "STATUS:", ev.status,
                print "%d/%d/%d %2d:%.2d:%.2d" % (ev.year+2000, ev.month, ev.day, ev.hour, ev.minute, ev.second),
                print "%.2f" % ev.subsec
                
                
            elif ev.evtype == "ENERGY":
                print "\t",
                print "ENERGY Q: %d" % ev.q,
                print "ADDR485: %d" % ev.q, ev.addr485,
                print "CHANNEL: %d" % ev.channel,
                print "%d/%d/%d %2d:%.2d:%.2d" % (ev.year+2000, ev.month, ev.day, ev.hour, ev.minute, ev.second),
                print "Value: %d Q: %d" % (ev.value.val, ev.value.q)
            else:
                print "Tipo de evento no reconocido"
    print "BCC:", d.bcc
        

def test():
    '''Testing de tramas y subtramas'''

    int2str = lambda l: ''.join(map(chr, l))
    #int2strgen = lambda *l: (chr(i) for i in l)
    result = MaraFrame.parse(any2buffer('FE    08    01    40    80    10    80    A7'))
    print result
    r = TCD.build(Container(evtype="ENERGY", q=1, addr485=1))
    print r
    #result.data = range(1, 10)
    event_data = Container(evtype="DIGITAL", 
                            q=0, addr485=5, 
                            bit=0, port=3, status=0, 
                            year=12, month=1, day=1, 
                            hour=12, minute=24,
                            second=10, 
                            ticks=4212)
    
    print "Construyendo un evento digital de puerto con puerto 3, bit 0, estado 0" #event_data
    pkg = Event.build(event_data)
    print upperhexstr(pkg)
    print "Evento de energía"
    energy_data = Container(evtype="ENERGY", q=0, addr485=4,
                            idle=0, channel=0, 
                            value=0x032F, 
                            **dtime2dict())
    pkg = Event.build(energy_data)
    print upperhexstr(pkg)
    
    print "Construyendo payload del comando 10"
    payload_10_data = Container(canvarsys=5, varsys=[0x1234, 0xfeda], candis=3, dis=[0x4567],  canais=0,ais=[], canevs=31, event=[event_data, event_data, energy_data])
    
    pkg = Payload_10.build(payload_10_data)
    print upperhexstr(pkg)
    frame_data = Container(sof=0xFE, length=0, source=1, dest=2, sequence=0x80, command=0x10, 
                                    payload_10=payload_10_data,
                                    bcc=0)
    pkg = MaraFrame.build(frame_data)
    
    print "Trama Mara c/QTY=0 y sin CS: ",  upperhexstr(pkg)
    print "Trama completa:", upperhexstr(build_frame(frame_data))

def test_events():
    '''
    Testing events
    '''
    ev = 0x40, 0x12, 0xC, 0x8, 0x7, 0x9, 0x30, 0x0, 0x00, 0x40
    print Event.parse(''.join(map(chr, ev)))
    
    ev = 0x00, 0x12, 0xC, 0x8, 0x7, 0x9, 0x30, 0x0, 0x00, 0x40
    print Event.parse(''.join(map(chr, ev)))

def test_frames():
    print "-"*80
    print "Trama 1"
    print "-"*80
    trama_1 = """
    FE 44 40 01 4A 10 19 00 00 90 1D 01 00 00 00 00 00 80 80 00 00 80 80 00 00 80 80 00
    00 80 80 0F 00 00 43 00 00 00 00 04 00 04 00 04 00 04 13 48 05 51 00 51 00 51 00 51
    00 51 00 51 00 51 00 51 00 01 E1 29
    """
    # Primera trama
    format_frame(trama_1, as_hex_string=True)
    
    
    print "-"*80
    print "Trama 2"
    print "-"*80
    trama_2 = """
    FE 44 40 01 4C 10 19 00 00 85 1D 01 00 00 00 00 00 00 01 00 00 00 01 00 00 00 01 00 00 00 01 0F 
    00 00 43 00 00 00 00 04 00 04 00 04 00 04 13 4C 05 51 00 51 00 51 00 51 00 51 00 51 00 51 00 51 
    00 01 DD 30
    """
    # Segunda trama
    format_frame(trama_2, as_hex_string=True)

    print "-"*80
    print "Trama 3"
    print "-"*80
    trama_3 = """
    FE F8 40 01 4D 10 19 00 00 8D 1D 01 00 00 00 00 00 00 01 00 00 00 01 00 00 00 01 00 00 00 01 0F
    00 00 43 00 00 00 00 04 00 04 00 04 00 04 13 81 09 51 00 51 00 51 00 51 00 51 00 51 00 51 00 51
    00 B5 01 93 0C 01 01 01 08 22 00 14 01 E3 0C 01 01 01 08 22 00 14 01 05 0C 01 01 01 08 22 00 14 
    01 92 0C 01 01 01 08 22 00 18 01 E2 0C 01 01 01 08 22 00 18 01 04 0C 01 01 01 08 22 00 18 01 F1 
    0C 01 01 01 08 22 00 1C 01 93 0C 01 01 01 08 22 00 1C 01 F3 0C 01 01 01 08 22 00 1C 01 05 0C 01 
    01 01 08 22 00 1C 01 F2 0C 01 01 01 08 22 00 20 01 04 0C 01 01 01 08 22 00 20 01 F0 0C 01 01 01 
    08 22 00 24 01 92 0C 01 01 01 08 22 00 24 01 15 0C 01 01 01 08 22 00 60 01 14 0C 01 01 01 08 22 
    00 7C 01 F3 0C 01 01 01 08 23 00 00 01 15 0C 01 01 01 08 23 00 00 3C 91
    """
    # Tercer trama
    format_frame(trama_3, as_hex_string=True)
    
    print "-"*80
    print "Trama 4"
    print "-"*80
    
    #sys.exit()
    
    trama_4 = """
    FE E4 40 01 F1 10 19 00 00 86 1D 01 00 00 00 00 EF 00 03 00 00 00 04 00 00 80 80 00 00 80 80 0F
    00 00 43 00 00 00 40 F6 40 F6 00 F4 00 3A 13 7F 09 00 40 00 40 00 40 00 40 00 40 00 40 00 40 00
    40 A1 45 00 0C 08 03 0F 00 00 00 00 45 01 0C 08 03 0F 00 00 00 00 
    42 00 0C 08 03 0F 00 00 00 00
    42 01 0C 08 03 0F 00 00 00 00 
    43 00 0C 08 03 0F 00 00 00 00 
    43 01 0C 08 03 0F 00 00 00 00 
    44 00 0C 08 03 0F 00 00 00 00 
    44 01 0C 08 03 0F 00 00 00 00 
    43 00 0C 08 03 0F 0F 00 00 00 
    43 01 0C 08 03 0F 0F 00 00 00 
    44 00 0C 08 03 0F 0F 00 00 00 
    44 01 0C 08 03 0F 0F 00 00 00 
    45 00 0C 08 03 0F 0F 00 00 00 
    45 01 0C 08 03 0F 0F 00 00 00 
    42 00 0C 08 03 0F 0F 00 00 00 
    42 01 0C 08 03 0F 0F 00 00 00 
    1D C2
    """
    
    format_frame(trama_4, as_hex_string=True)

if __name__ == '__main__':
    #===========================================================================
    # Debug with ipython --pdb -c "%run constructs.py"
    #===========================================================================
    
    import sys
    
    #sys.exit(test_events())
    sys.exit(test_frames())
    
    
    