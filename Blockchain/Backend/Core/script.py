from Blockchain.Backend.Util.util import encode_variant, int_to_little_endian


class Script:
    def __init__(self,cmds = None):
        if cmds == None:
            self.cmds = []
        else:
            self.cmds = cmds

    def serialize(self):
        # initialize what we'll send back
        result = b""
        # go through each cmd
        for cmd in self.cmds:
            # if the cmd is an integer, it's an opcode
            if type(cmd) == int:
                # turn the cmd into a single byte integer using int_to_little_endian
                # result += int_to_little_endian(cmd, 1)
                result += int_to_little_endian(cmd, 1)
            else:
                # otherwise, this is an element
                # get the length in bytes
                length = len(cmd)
                # for large lengths, we have to use a pushdata opcode
                if length < 75:
                    # turn the length into a single byte integer
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:
                    # 76 is pushdata1
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError("too long an cmd")

                result += cmd
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return encode_variant(total) + result




    @classmethod
    def p2pkh_script(cls,h160):
        '''takes hash160 and return the p2pkh ScriptPubKey'''
        return Script([
            0x76, 
            0xa9, 
            h160, 
            0x88, 
            0xac
            ])