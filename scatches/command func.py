def additional_to_2(bits: str):
    if bits[0] == '0':
        return int(bits, 2)
    return -int(''.join(map(str, [int((not int(i))) for i in bits[1:]])), 2) - 1


# 0	    00000000
print(additional_to_2('00000000'), additional_to_2('00000000') == 0)
# 1	    00000001
print(additional_to_2('00000001'), additional_to_2('00000001') == 1)
# 2	    00000010
print(additional_to_2('00000010'), additional_to_2('00000010') == 2)
# 126	01111110
print(additional_to_2('01111110'), additional_to_2('01111110') == 126)
# 127	01111111
print(additional_to_2('01111111'), additional_to_2('01111111') == 127)
# −128	10000000
print(additional_to_2('10000000'), additional_to_2('10000000') == -128)
# −127	10000001
print(additional_to_2('10000001'), additional_to_2('10000001') == -127)
# −126	10000010
print(additional_to_2('10000010'), additional_to_2('10000010') == -126)
# −2	11111110
print(additional_to_2('11111110'), additional_to_2('11111110') == -2)
# −1	11111111
print(additional_to_2('11111111'), additional_to_2('11111111') == -1)

