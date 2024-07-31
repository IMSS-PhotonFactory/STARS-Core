#!/usr/bin/python3
import argparse
import scriptlib

parser = argparse.ArgumentParser()
parser.add_argument('count', type = int, help = 'Count of \"GetValue\"')
parser.add_argument('remote', nargs = '?', help = 'Remote terminal') #nargs:'*','?','+',number
#parser.add_argument('-t', '--timeout', type = int, default = 3, help = 'Ping timeout')
args = parser.parse_args()

sc = scriptlib.ScriptLib(remote = args.remote)
sc.data_file = 'test2.csv'
for t in range(args.count):
    rt = sc.send_command('System','gettime')
    sc.write_file("{},{}".format(t,rt.parameters))
    sc.sleep(5)

