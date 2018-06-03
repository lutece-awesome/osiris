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
        self._field = [x for x in kw]

    def __str__(self):
        return self.full

    def __repr__(self):
        return str( self.full )
    
    @property
    def attribute(self):
        return { x : getattr( self , x ) for x in self._field }