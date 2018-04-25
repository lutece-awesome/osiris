from fetch import fetch_waiting_submission
from judger import judge

def fetch_test():
    r = fetch_waiting_submission()
    judge(
        submission_id = r['submission_id'],
        lang = r['language'],
        code = r['code'],
        problem = r['problem']
    )
    print( r )



if __name__ == '__main__':
    fetch_test()