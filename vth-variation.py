import glob, os
from subprocess import call

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

print 'Executing - ' + libs[0]
tmp_contents = template_file.replace('{{filename}}', libs[0])
tmp_filename = modify_ext(libs[0], 'cir')
with open(tmp_filename, 'w') as output_file:
    output_file.write(tmp_contents)
    print 'About to call - ' + tmp_filename
call('/Applications/LTspice.app/Contents/MacOS/LTspice -Run -ascii -b ./' + tmp_filename, shell=True)
print "Done"