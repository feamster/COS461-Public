import hashlib

def check(value, correct_hash):
    m = hashlib.md5()
    m.update(value)
    test_hash = m.digest()
    if correct_hash == test_hash:
        return True
    else:
        return False


def prep_list(values):
    return " ".join([x[0] for x in values])


def check_ips_by_flows(ips_by_flows):
    correct_hash = '\xd6u\x96a\x104!\x16\xd3u!\xa9C}`\xd5'
    if check(prep_list(ips_by_flows), correct_hash):
        print "Hashes match. Your ips_by_flows is correct."
    else:
        print "Hashes do not match.  Check for bugs in your code."


def check_ips_by_volume(ips_by_volume):
    correct_hash = 'oz\xdf\xf8\x1d\xd8G\xbe\x8d\\\xea\xef\xb7\xca$T'
    if check(prep_list(ips_by_volume), correct_hash):
        print "Hashes match. Your ips_by_volume is correct."
    else:
        print "Hashes do not match.  Check for bugs in your code."


def check_ports_by_flows(ports_by_flows):
    correct_hash = '\x898\xb3yYT&\xfck\x0b\x94\xc1\x87\xde\xd7\xc9'
    if check(prep_list(ports_by_flows), correct_hash):
        print "Hashes match. Your ports_by_flows is correct."
    else:
        print "Hashes do not match.  Check for bugs in your code."


def check_ports_by_volume(ports_by_volume):
    correct_hash = '\xec\xbbL\xda\xb5c[\xe0zz\x91\xe6\x8b\x86\x05\xc0'
    if check(prep_list(ports_by_volume), correct_hash):
        print "Hashes match. Your ports_by_volume is correct."
    else:
        print "Hashes do not match.  Check for bugs in your code."

def check_longest_aspath(longest_aspath):
    correct_hash = '\xb1dd\x8dq\xbe\xf8\x8e\xd5\xfez\xb7q\x02\xca\xc3'
    if check(longest_aspath, correct_hash):
        print "Hashes match. Your longest_aspath is correct."
    else:
        print "Hashes do not match. Check for bugs in your code."
