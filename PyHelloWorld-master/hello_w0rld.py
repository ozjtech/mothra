import sys
The_Message = '{S}{a}{l}{v}{e} {m}{u}{n}{d}{i}'
One = input('''You enter a DARK AND SPOOKY DUNGEON. In the FOYÉR there is a STONE PILLAR with an ETCHING on top. There is a IMPENETRABLE DOOR beyond the PILLAR.
What do you do?

READ THE ETCHING
LEAVE

''')
if 'READ' in One:
            print('''
The ETCHING reads:
            
    'Beware all those who enter here
    Remember those who were spurned for fear
    Great knowledge within to last your days
    If only you translate this ancient phrase:
            
    ''', The_Message, '''''')
            Two = input('''
With that, a STONE KEYBOARD slides out from the PILLAR. Now would be the perfect time for your
TRUSTY DECODER RING! 
           
Did you bring it?
            
YES
NO

''')
            if 'YES' in Two:
                Three = input('''
You reach a hand out to enter the password from your DECODER RING. You breathlessly type: 

''')
                if Three.startswith('{') and Three.endswith('}'):
                    try: Decoder_Ring = eval(Three)
                    except: print('''
With the last keystroke, the PILLAR sinks to the ground. The DUNGEON WALLS begin to crumble. It occurs to your in your dying moments that that may have been the wrong DECODER RING. ''')
                else: sys.exit('''
With the last keystroke, the PILLAR sinks to the ground. The DUNGEON WALLS begin to crumble. It 
occurs to your in your dying moments that that may have been the wrong DECODER RING. ''')
                if The_Message.format(**Decoder_Ring) == ('Hello world'):
                        print('''
With your last keystroke, the ETCHING morphs before your eyes, bearing the translated phrase:
                    
''', The_Message.format(**Decoder_Ring), ''' 
                    
The PILLAR sinks to the ground. The IMPENETRABLE DOOR slides open.
For one fleeting moment, you know true bliss. Or something. Idk. ''')
            else: sys.exit('''
You leave the DUNGEON in a huff. Why would you attempt this ADVENTURE without your 
TRUSTY DECODER RING? Foolish.''')
else: sys.exit('''
You leave the DUNEGON without a word. Well that was weird. No more LATE NIGHT PICKLES, you think to yourself.''')