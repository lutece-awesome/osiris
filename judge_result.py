from enum import Enum, unique

class _meta:
    __slots__ = (
        'full',
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


@unique
class Judge_result( Enum ):
    PD = _meta(
        full = 'Pending',
    )
    PR = _meta(
        full = 'Preparing',
    )
    AC = _meta(
        full = 'Accepted',
    )
    RN = _meta(
        full = 'Running',
    )
    CE = _meta(
        full = 'Compile Error',
    )
    WA = _meta(
        full = 'Wrong Answer',
    )
    RE = _meta(
        full = 'Runtime Error',
    )
    TLE = _meta(
        full = 'Time Limit Exceeded',
    )
    OLE = _meta(
        full = 'Output Limit Exceeded',
    )
    MLE = _meta(
        full = 'Memory Limit Exceeded',
    )
    JE = _meta(
        full = 'Judger Error',
    )


def get_judge_result( result ):
    for each_result in Judge_result:
        if each_result.value.full == result:
            return each_result
    return None