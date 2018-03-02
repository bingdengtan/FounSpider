import time
import re

class common():
    @staticmethod
    def props(obj):
        pr = {}
        for name in dir(obj):
            value = getattr(obj, name)
            if not name.startswith('__') and not callable(value) and not name.startswith('_'):
                pr[name] = value
        return pr

    @staticmethod
    def getCurrentDateTimeString():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @staticmethod
    def getFirstCharAsPingYin(str_input):
        if isinstance(str_input, str):
            unicode_str = str_input
        else:
            try:
                unicode_str = str_input.decode('utf8')
            except:
                try:
                    unicode_str = str_input.decode('gbk')
                except:
                    print('unknown coding')
                    return

        charLst = []
        for l in unicode_str:
            charLst.append(common.get_cn_first_letter(l))

        return ''.join(charLst)

    @staticmethod
    def get_cn_first_letter(str_input):
        if re.compile(r'[0-9a-zA-Z]').match(str_input):
            return str_input.lower()

        str1 = str_input.encode('gbk')
        try:
            ord(str1)
            return ""
        except:
            asc = str1[0] * 256 + str1[1] - 65536

        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''
