import argparse
import scriptlib

#Source device and measurement device
source = 'simmotor.th'
measure = 'testdev-single'
datafile = 'scanth.csv'

#Get parameters from command line
parser = argparse.ArgumentParser()
parser.add_argument('start', type = int, help = 'Start value of source device.')
parser.add_argument('end', type = int, help = 'End value of source device.')
parser.add_argument('step', type = int, help = 'Step of values.')
parser.add_argument('remote', nargs = '?', help = 'Remote stars node') #nargs:'*','?','+',number
args = parser.parse_args()

sc = scriptlib.ScriptLib()
sc.data_file = datafile

sc.send_command('System', 'flgon {}'.format(source))
for t in range(args.start, args.end, args.step):
    sc.send_command(source, 'SetValue {}'.format(t))
    sc.wait_for('_ChangedIsBusy 0')
    rt = sc.send_command(measure,'GetValue')
    sc.write_file("{},{}".format(t,rt.parameters))
