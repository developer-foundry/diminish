from invoke import task

@task
def build_libraries(c):
  print("Building")
  c.run("gcc -c -Wall -Werror -O3 -fPIC external-libraries/server.c external-libraries/dotenv.c")
  c.run("gcc -shared -o server.so server.o dotenv.o")

  c.run("gcc -c -Wall -Werror -O3 -fPIC external-libraries/client.c external-libraries/dotenv.c")
  c.run("gcc -shared -o client.so client.o dotenv.o")

  c.run("gcc -c -Wall -Werror -O3 -funsafe-math-optimizations -fpic external-libraries/filtering.c")
  c.run("gcc -shared -o filtering.so filtering.o")

  print("Completed Build")

@task
def clean(c):
  print("Cleaning...")
  c.run("rm *.o")
  c.run("rm *.so")
  print("Cleaned!")
