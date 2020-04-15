from invoke import task

@task
def build(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -fpic filtering.c")
  c.run("gcc -shared -o filtering.so filtering.o")
  print("Completed Build")

@task
def clean(c):
  print("Cleaning...")
  c.run("rm filtering.o")
  c.run("rm filtering.so")
  print("Cleaned!")
