import docker
import compiler
import settings
import language
client = docker.from_env()

def modify( submission_id , judge_status , info ):
    pass

def run( lang , sourcefile ):
    pass



def judge( submission_id , lang , code , problem , sourcefile ):
    st , info = compiler.Compile( 
        lang = lang ,
        code = code ,
        sourcefile = sourcefile)
    if st != 'Success':
        modify( submission_id , st , info )
    pass