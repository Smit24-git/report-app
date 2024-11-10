class FileManager():
    def __init__(self, filename):
        self.filename = filename


    def append_new_line(self):
        file = open(self.filename, 'a')
        try:
            file.write('\n')
        finally:
            file.close()

    def append_string(self, line):
        file = open(self.filename, 'a')
        try:
            file.write(line)
            file.write('\n')
        finally:
            file.close()

    def append_data_arr(self, data):
        file = open(self.filename, 'a')
        try:
            for d_line in data:
                s_arr = [str(d) for d in d_line]
                for s in s_arr:
                    file.write('{:15s} '.format(s))
                file.write('\n')
        finally:
            file.close()

   
