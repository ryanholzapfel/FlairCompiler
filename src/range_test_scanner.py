
from scanner import Scanner

test_cases ="wbvgxquccsexayxxcfoqkvjqscafbohbfshcreyvipkdckhymzwqhmftoydivdouamkmbtglvveiftapscdackxxvloewlesvtnrbmqkfrhqqlokljqtoafhshdhkceaisiynhxmjjumnqyirurhpetsyralszcouxsaqpwdgonvpkzkojtmhxicfnmdlprwrxetigqrvkxltgdlkuddjtjnidksqraahwsoxfundxyiruqwbsdkuxxmlvcrsfqs 4294967295 -4294967296 wbvgxquccsexayxxcfoqkvjqscafbohbfshcreyvipkdckhymzwqhmftoydivdouamkmbtglvveiftapscdackxxvloewlesvtnrbmqkfrhqqlokljqtoafhshdhkceaisiynhxmjjumnqyirurhpetsyralszcouxsaqpwdgonvpkzkojtmhxicfnmdlprwrxetigqrvkxltgdlkuddjtjnidksqraahwsoxfundxyiruqwbsdkuxxmlvcrsfqsff -4294967297  4294967296 1 2 3 a b c"
#edge cases x3, fail cases x3

tokens = Scanner(test_cases)

while True:
    try:
        ct = tokens.next_token()
        print(ct)
        if ct.is_eof():
            break
    except:
        print("token failed")


