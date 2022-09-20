import os
from zipfile import ZipFile
# import tarfile
from struct import unpack
from time import sleep

for path, dirs, files in os.walk("data"):
    for file in files:
        # print(os.path.join(path, file))
        if file.endswith('.zip'):
            try:
                path_file = os.path.join(path, file)
            
                zf = ZipFile(os.path.join(path, file))
                uncompress_size = sum((file.file_size for file in zf.infolist()))

                compressed_size = os.stat(path_file).st_size

                if uncompress_size / 50 >= compressed_size:
                    print(f" {path_file} is a potential ZipBomb")
                    if compressed_size <= 350000000: #<=350 MB
                        owdata = os.urandom(compressed_size)
                        with open(path_file, 'wb') as fobj:
                            fobj.write(owdata)
                        owdata = os.urandom(compressed_size)
                        with open(path_file, 'wb') as fobj:
                            fobj.write(owdata)
                        owdata = os.urandom(compressed_size)
                        with open(path_file, 'wb') as fobj:
                            fobj.write(owdata)
                                #Overwrite with 100MB of zeroes
                        with open(path_file, 'w') as fobj:
                            fobj.write('0'*100000000)

                        fobj = open(path_file, 'w')
                        fobj.close()

                    else:
                        owchunks = compressed_size/1000
                        with open(path_file, 'wb') as fobj:
                            for x in range(1000):
                                fobj.write(os.urandom(owchunks))

                        #Overwrite with 100MB of zeroes
                        with open(path_file, 'w') as fobj:
                            fobj.write('0'*100000000)

                        fobj = open(path_file, 'w')
                        fobj.close()
                    sleep(0.3)
                    os.remove(path_file)
                    print("Threat secured.")
                elif uncompress_size / 50 < compressed_size:
                    print(f"Safe, {file} is only {uncompress_size} bytes big")
            except:
                pass

        elif file.endswith('.gz'):
            file_path = os.path.join(path, file)
            fo = open(file_path, 'rb')
            if fo == "":
                pass
            elif fo != "":
                try:
                    fo.seek(-4, 2)

                    r = fo.read()
                    fo.close()
                    uncompress_size_gzip = unpack('<I', r)[0]
                    compressed_size_gzip = os.stat(file_path).st_size
                    # if uncompress_size_gzip >= 10000000000 and compressed_size_gzip <= 550000000: # if the file's uncompressed size is 10 gb and compressed size is smaller than a gb we determine it as ZipBomb
                    if uncompress_size_gzip / 50 >= compressed_size_gzip:
                        print(f" {file_path} is a Potential ZipBomb")
                
                        if compressed_size_gzip <= 350000000: #<=350 MB
                            owdata = os.urandom(compressed_size_gzip)
                            with open(file_path, 'wb') as fobj:
                                fobj.write(owdata)
                            owdata = os.urandom(compressed_size_gzip)
                            with open(file_path, 'wb') as fobj:
                                fobj.write(owdata)
                            owdata = os.urandom(compressed_size_gzip)
                            with open(file_path, 'wb') as fobj:
                                fobj.write(owdata)
                                    #Overwrite with 100MB of zeroes
                            with open(file_path, 'w') as fobj:
                                fobj.write('0'*100000000)
                            
                            fobj = open(file_path, 'w')
                            fobj.close()
                    
                        else:
                            owchunks = compressed_size_gzip/1000
                            with open(file_path, 'wb') as fobj:
                                for x in range(1000):
                                    fobj.write(os.urandom(owchunks))
                    
                            #Overwrite with 100MB of zeroes
                            with open(file_path, 'w') as fobj:
                                fobj.write('0'*100000000)
                    
                            fobj = open(file_path, 'w')
                            fobj.close()
                        sleep(0.3)
                        os.remove(file_path)
                        print("Threat secured.")
                    else:
                        print(f"Safe, {file} is only {uncompress_size_gzip} bytes big")
                except OSError:
                    print(f"{file} is an invalid GZip.")
                    pass

"""
        elif file.endswith('.tar'):
            path_file_tar = os.path.join(path, file)
            tf = tarfile.TarFile(os.path.join(path, file))
            uncompress_size_tar = sum((file.file_size for file in tf.infolist()))

            compressed_size = os.stat(path_file_tar).st_size
            if uncompress_size_tar >= 10000000000 and compressed_size <= 800000000:
                print("Potential ZipBomb")
            else: 
                print(f"Safe, {file} is only {uncompress_size} bytes big")
"""