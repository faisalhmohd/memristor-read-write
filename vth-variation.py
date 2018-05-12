import glob, os
from subprocess import call
import numpy

# Preconfig

os.chdir(os.getcwd())

def modify_ext(file, ext):
    return file.split('.')[0] + '.' + ext

# Get all libs

libs = list()
for file in glob.glob('*.pm'):
    libs.append(file)

# Clean Up

for file in libs:
    if(os.path.exists(modify_ext(file, 'cir'))):
        os.remove(modify_ext(file, 'cir'))

# Get Template

with open('read_write_01_template.cir', 'r') as myfile:
    template_file = myfile.read()

# Execute the real shit!
# Output simulation onto log file

read_datas = list()
write_datas = list()

for file in libs:

    print '-----------------------'
    print 'Processing - ' + file
    print '-----------------------'
    print 'Executing ...'
    tmp_contents = template_file.replace('{{filename}}', file)
    tmp_filename = modify_ext(file, 'cir')
    with open(tmp_filename, 'w') as output_file:
        output_file.write(tmp_contents)
    call('/Applications/LTspice.app/Contents/MacOS/LTspice -Run -ascii -b ./' + tmp_filename, shell=True)

    # Extract values from log file and calculate 3*sigma/mu

    print 'Extracting ...'
    result_contents = tuple(open(modify_ext(tmp_filename, 'log')))

    skip_read = False
    skip_write = False
    read_data = list()
    write_data = list()

    for line in result_contents:
        if line == 'Measurement: readtime\n':
            skip_read = True
            continue
        elif line == 'Measurement: writetime\n':
            skip_write = True
            continue
        elif skip_read:
            if line != '\n':
                read_data.append(line.split('\t')[1])
            else:
                skip_read = False
        elif skip_write:
            if line != '\n':
                write_data.append(line.split('\t')[1])
            else:
                skip_write = False

    # Reformat List

    read_data.pop(0)
    read_data = numpy.array(read_data)
    read_data = read_data.astype(numpy.float)
    write_data.pop(0)
    write_data = numpy.array(write_data)
    write_data = write_data.astype(numpy.float)

    read_datas.append(numpy.mean(read_data))
    write_datas.append(numpy.mean(write_data))

print '-----------------------'
print "Processing Completed"

# Reformat List
read_datas = numpy.array(read_datas)
read_datas = read_datas.astype(numpy.float)
write_datas = numpy.array(write_datas)
write_datas = write_datas.astype(numpy.float)

print 'Read 3*sigma/mu = '
print 3*numpy.std(read_datas)/numpy.mean(read_datas)
print 'Write 3*sigma/mu = '
print 3*numpy.std(write_datas)/numpy.mean(write_datas)
print "Done"