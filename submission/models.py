from functools import reduce


class Submission( object ):
    '''
        include the basic information of submission:
    '''

    __slots__ = (
        'submission',
        'problem',
        'time_limit',
        'memory_limit',
        'output_limit',
        'stack_limit',
        'language',
        'sourcefile',
        'code',
        'checker',
        'case_number',
        'data_dir',
        'work_dir',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = kw

    def __str__(self):
        return self.submission

    def __repr__(self):
        return str( self._field )

    @property
    def attribute(self):
        return self._field
    
    receive_transfer_field = {
        'submission_id' : 'submission'
    }


def parse( ** kwargs ):
    for _ in Submission.receive_transfer_field:
        ori = _
        tr = Submission.receive_transfer_field[_]
        kwargs[tr] = kwargs[_]
        kwargs.pop( ori )
    return kwargs