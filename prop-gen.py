import subprocess
import sys
from pprint import pprint
import sys
import os
# ============================================================================
usage = "%s <range_start> <range_stop> <timestamp>" % sys.argv[0]

if len(sys.argv) < 4:
    print(usage)
    sys.exit(1)
else:
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
#    ntime = int(sys.argv[3])

# print("start = %s" % start)
# print("stop = %s" % stop)
# print("ntime = %s" % ntime)


def serialise(obj):
    import binascii
    import simplejson as json

    o = [["proposal", obj]]
    s = json.dumps(o, sort_keys=True, indent=None, separators=(',', ':'))

    return binascii.hexlify(s)


def rangeit(ntime, start, stop):

    for epoch in range(start, stop + 1):
        # print(epoch)

        gap = 2575480
        obj = {
            "end_epoch": str(epoch + gap),
            "name": "Survey-why-Merchants-not-using-Dash",
            "payment_address": "XwUeFiUQz1qLurzcpzKBDUTPvj1Tzx3FYs",
            "payment_amount": "82.75",
            "start_epoch": str(epoch),
            "type": 1,
            "url": "https://www.dash.org/forum/threads/project-proposal-understanding-the-barriers-to-adoption-of-dash-by-uk-businesses-and-merchants.15770/"
        }

        # Correct usage is 'gobject genhash <parent-hash> <revision> <time> <data-hex>'
        cmd = "dash-cli gobject genhash 0 1 {} {}".format(ntime, serialise(obj))
        print(cmd)


rangeit(ntime, start, stop)
