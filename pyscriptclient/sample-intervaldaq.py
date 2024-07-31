import scriptlib
sc = scriptlib.ScriptLib()
sc.data_file = 'test1.csv'

for t in range(20):
    rt = sc.send_command('sanwadmm','GetValue')
    sc.write_file("{},{}".format(t,rt.parameters))
    sc.sleep(5)
