from invoke import task

@task
def build(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -fpic clms.c")
  c.run("gcc -shared -o libclms.so clms.o")
  print("Completed Build")

@task
def clean(c):
  print("Cleaning...")
  c.run("rm clms.o")
  c.run("rm libclms.so")
  print("Cleaned!")
