from invoke import task

@task
def build_pi_library(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -O3 -funsafe-math-optimizations -fpic -mcpu=cortex-a53 -mfpu=neon-fp-armv8 -mfloat-abi=hard filtering.c")
  c.run("gcc -shared -o filtering.so filtering.o")
  print("Completed Build")

@task
def build_exec_pi(c):
  print("Building")
  c.run("gcc -Wall -Werror -O3 -funsafe-math-optimizations -fpic -mcpu=cortex-a53 -mfpu=neon-fp-armv8 -mfloat-abi=hard filtering.c")
  print("Completed Build")

@task
def build_pc_library(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -O3 -funsafe-math-optimizations -fpic filtering.c")
  c.run("gcc -shared -o filtering.so filtering.o")
  print("Completed Build")

@task
def build_exec_pc(c):
  print("Building")
  c.run("gcc -Wall -Werror -O3 -funsafe-math-optimizations -fpic filtering.c")
  print("Completed Build")

@task
def build_networking(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -O3 soundwave/networking/server.c soundwave/networking/dotenv.c")
  c.run("gcc -shared -o server.so server.o dotenv.o")

  c.run("gcc -c -Wall -Werror -O3 -fPIC soundwave/networking/client.c soundwave/networking/dotenv.c")
  c.run("gcc -shared -o client.so client.o dotenv.o")
  print("Completed Build")

@task
def clean(c):
  print("Cleaning...")
  c.run("rm *.o")
  c.run("rm *.so")
  print("Cleaned!")
