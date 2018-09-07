import socket
import math
import time
import threading
import multiprocessing
from ctypes import cdll
lib = cdll.LoadLibrary("primes.dll")


class Benchmarker(object):
    def __init__(self):
        self.msg_len = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1", 4444))
        self.sock.recv(self.msg_len).decode("UTF-8")
        print("Established connection to Socket Server...")
        self.ceiling = int()
        self.processes = list()
        self.threads = list()

        self.threads.append(threading.Thread(target=self.get_py_primes))
        self.threads.append(threading.Thread(target=self.get_cpp_primes))
        self.threads.append(threading.Thread(target=self.get_java_primes))

        self.processes.append(multiprocessing.Process(target=self.get_py_primes))
        self.processes.append(multiprocessing.Process(target=self.get_cpp_primes))
        self.processes.append(multiprocessing.Process(target=self.get_java_primes))

        self.user_contine = True

        command = input("Enter a ceiling integer for prime search, or 'test' to test functionality: ")
        if command == "test":
            self.test_accuracy()
        else:
            self.ceiling = int(command)
            single_start = time.clock()
            self.get_py_primes()
            self.get_cpp_primes()
            self.get_java_primes()
            single_total = time.clock() - single_start
            print("Total time with single-threading %s seconds." % (single_total,))
            time.sleep(1)

            multi_start = time.clock()
            for thread in self.threads:
                thread.start()
            for thread in self.threads:
                thread.join()
            multi_total = time.clock() - multi_start
            print("Total time with multi-threading %s seconds." % (multi_total,))
            del self.threads
            time.sleep(1)

            process_start = time.clock()
            for process in self.processes:
                process.start()
            for process in self.processes:
                process.join()
            process_total = time.clock() - process_start
            print("Total time with multiprocessing %s seconds" % (process_total,))
            """
            print("\nPython, the cpp-library, and the Java Socket Server took %s, %s, and %s seconds to complete" %
                  (self.py_time, self.cpp_time, self.java_time),
                  "a prime search of %s, respectively." % self.ceiling)
            """

    def py_is_prime(self, possible_prime):
        if possible_prime < 2:
            return False
        elif possible_prime == 2:
            return True
        else:
            for denominator in range(2, math.ceil(math.sqrt(possible_prime)) + 1):
                if possible_prime % denominator == 0:
                    return False
        return True

    def get_py_primes(self):
        start = time.clock()
        for num in range(self.ceiling):
            self.py_is_prime(num)
        total = time.clock() - start
        print("\nPython finished in %s seconds." % (total,))

    def get_cpp_primes(self):
        start = time.clock()
        for num in range(self.ceiling):
            lib.cpp_is_prime(num)
        total = time.clock() - start
        print("\nCpp finished in %s seconds." % (total,))

    def get_java_primes(self):
        start = time.clock()
        for num in range(2, self.ceiling):
            byte_packet = bytes("%s\n" % num, "UTF-8")
            self.sock.send(byte_packet)
            self.sock.recv(self.msg_len)
        total = time.clock() - start
        print("\nJava finished in %s seconds." % (total,))

    def test_accuracy(self):
        ceiling = 100000
        cpp_primes_found = list()
        java_primes_found = list()
        python_primes_found = list()
        for num in range(2, ceiling):
            if self.py_is_prime(num):
                python_primes_found.append(num)
            if lib.cpp_is_prime(num):
                cpp_primes_found.append(num)
            byte_packet = bytes("%s\n" % num, "UTF-8")
            self.sock.send(byte_packet)
            response = str(self.sock.recv(self.msg_len).decode("UTF-8")).replace("0", "")
            if "True" in response:
                java_primes_found.append(num)

        assert cpp_primes_found == java_primes_found == python_primes_found
        print("\nAll lists identical, functions successful.\n")


if __name__ == "__main__":
    bench = Benchmarker()
