
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
        'compileerror_msg',
        'judgererror_msg',
        'case',
        'complete',
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