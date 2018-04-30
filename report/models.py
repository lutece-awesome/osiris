
class Report:
    '''
        include the information to send the server
    '''

    __slots__ = (
        'result',
        'submission',
        'time_cost',
        'memory_cost',
        'additional_info',
        'case',
        'complete',
        '_field'
    )

    def __init__( self , ** kw ):
        for _ in kw:
            self.__setattr__( _ , kw[_] )
        self._field = kw

    def __str__(self):
        return self.result
    
    def __repr__(self):
        return str( self._field )

    @property
    def attribute(self):
        return self._field