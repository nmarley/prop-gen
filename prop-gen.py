import subprocess
import sys
from pprint import pprint
import sys
import os
import simplejson as json
import signal
# ============================================================================

ntime = 0
epoch = 0

def signal_handler(sig, frame):
    print('ntime = %s' % ntime)
    print('epoch = %s' % epoch)


signal.signal(signal.SIGINT, signal_handler)


# if either of these hashes is found, stop immediately, we have a winner
needles = [
    '6be5634f38282ae6a889a3e6a7ca4616bbf597915d91676cbd401683e732bd15',
    '15bd32e7831640bd6c67915d9197f5bb1646caa7e6a389a8e62a28384f63e56b',
    # 'f2b8d5a2d4d9ce5f5db365b648d02548e274f24f1dfea84a05d3c7f7f97a5807'
]

def serialise(obj):
    import binascii

    o = [["proposal", obj]]
    s = json.dumps(o, sort_keys=True, indent=None, separators=(',', ':'))

    return binascii.hexlify(s.encode('utf-8'))


def rangeit(ntime, start, stop):
    global epoch

    for epoch in range(start, stop + 1):
        # print(epoch)

        # proposal generator always adds this many seconds between start_epoch
        # and end_epoch
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
        # cmd = "dash-cli gobject genhash 0 1 {} {}".format(ntime, serialise(obj))
        # print(cmd)

        special_dash_dir = '/home/nmarley/dash-86525601d5915f380976c9d2e686ad7f66db991f'
        cmd = [
            '{}/bin/dash-cli'.format(special_dash_dir),
            'gobject', 'genhash', '0', '1', str(ntime), serialise(obj)
        ]

        # result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout = result.stdout or b''
        out = stdout.decode('utf-8').rstrip()
        hsh = json.loads(out)

        val = hsh['genhash']
        fields = val.split(' ')
        objhash = fields[2]
        #print('objhash = %s' % objhash)

        # stop immediately, we have a winner !
        if objhash in needles:
            print('Got it!')
            print(val)
            sys.exit(0)

        # nt[1499923860] se[1500509375] f2b8d5a2d4d9ce5f5db365b648d02548e274f24f1dfea84a05d3c7f7f97a5807
        # import pdb; pdb.set_trace(); 1
        # print(cmd)

        # 6be5634f38282ae6a889a3e6a7ca4616bbf597915d91676cbd401683e732bd15
        # 15bd32e7831640bd6c67915d9197f5bb1646caa7e6a389a8e62a28384f63e56b


#ntime_start = 1499923860
#ntime_start = 1499970260
ntime_start = 1499970284
#ntime_start = 1499903860
ntime_stop = 1499973860

#epoch_start = 1500386019
#epoch_stop = 1500731619

#epoch_start = 1500386019
#epoch_stop = 1500731619

#epoch_start = 1500494975
#epoch_stop = 1500539372

# smallest range
#epoch_start = 1500509375
#epoch_stop = 1500523775

# smallest(er) range
epoch_start = 1500514775
epoch_stop = 1500519572 

for ntime in range(ntime_start, ntime_stop + 1):
    print('ntime = %s' % ntime)
    rangeit(ntime, epoch_start, epoch_stop)
