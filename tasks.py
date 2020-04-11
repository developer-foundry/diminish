from invoke import task

@task
def build(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -fpic cmult.c")
  c.run("gcc -shared -o libcmult.so cmult.o")
  print("Completed Build")

@task
def clean(c):
  print("Cleaning...")
  c.run("rm cmult.o")
  c.run("rm libcmult.so")
  print("Cleaned!")
