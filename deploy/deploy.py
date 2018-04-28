import docker

client = docker.from_env()

client.images.pull( 'gcc:7.3.0' )