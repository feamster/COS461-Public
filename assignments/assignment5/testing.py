import hashlib

def check(value, correct_hash):
    m = hashlib.md5()
    m.update(value)
    test_hash = m.digest()
    if correct_hash == test_hash:
        return True
    else:
        return False


def check_synonly_percent(percentage):
    correct_hash = 'J\r\xe9bAA\x99\xfb\xda)L;II\xcd\xc6'
    test_percentage = str(round(percentage))
    if check(test_percentage, correct_hash):
        print "Hashes match. Your percentage of SYN-only flows is correct."
    else:
        print "Hashes do not match. Check for bugs in your percentage of SYN-only flows."


def check_percent_knownbad(percentage):
    correct_hash = '\x9fA\xf9\xf1\xc44q\x8a\xe6\xe5\x0f\xfb\xa6\x11R\xd0'
    test_percentage = str(round(percentage))
    if check(test_percentage, correct_hash):
        print "Hashes match. Your percentage of known bad flows is correct."
    else:
        print "Hashes do not match. Check for bugs in your percentage of known bad flows."


def check_percent_synonly_knownbad(percentage):
    correct_hash = 'b\xdc\xa4\x9f\x07\x81\xbf&\xb40[\xdd\xb0AK\xea'
    test_percentage = str(round(percentage))
    if check(test_percentage, correct_hash):
        print "Hashes match. Your percentage of SYN-only flows out of the known bad flows is correct."
    else:
        print "Hashes do not match. Check for bugs in your SYN-only flows out of the total known bad flows."


def check_percent_synonly_other(percentage):
    correct_hash = 'J\r\xe9bAA\x99\xfb\xda)L;II\xcd\xc6'
    test_percentage = str(round(percentage))
    if check(test_percentage, correct_hash):
        print "Hashes match. Your percentage of SYN-only flows out of the remaining flows is correct."
    else:
        print "Hashes do not match. Check for bugs in your SYN-only flows out of the remaining flows."


def check_num_malicious_hosts(num):
    correct_hash = '\xc8\x9c\xa3nM\x040\xe7\\\xa29\x04p\xa5\x9aY'
    test_num = str(num)
    if check(test_num, correct_hash):
        print "Hashes match. Your number of malicious hosts is correct."
    else:
        print "Hashes do not match. Check for bugs in your number of malicious hosts."


def check_num_benign_hosts(num):
        correct_hash = '2\x95\xc7j\xcb\xf4\xca\xae\xd3<6\xb1\xb5\xfc,\xb1'
        test_num = str(num)
        if check(test_num, correct_hash):
            print "Hashes match. Your number of benign hosts is correct."
        else:
            print "Hashes do not match. Check for bugs in your number of benign hosts."


def check_num_questionable_hosts(num):
        correct_hash = "\xc2\n\xd4\xd7o\xe9wY\xaa'\xa0\xc9\x9b\xffg\x10"
        test_num = str(num)
        if check(test_num, correct_hash):
            print "Hashes match. Your number of questionable hosts is correct."
        else:
            print "Hashes do not match. Check for bugs in your number of questionable hosts."
