import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/xavier/Desktop/medical/Medical_Bot/install/arm_bot'
