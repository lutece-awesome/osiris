from enum import Enum, unique

class _meta:
    __slots__ = (
        'full',
        'version',
        'image',
        'file',
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
class Language( Enum ):
    GNU = _meta(
        full = 'GNU G++/GCC',
        version = '7.3.0',
        image = 'osiris-gcc:7.3.0',
        file = 'GNU',
    )
    CLANG = _meta(
        full = 'Clang',
        version = '6.0.0',
        image = 'osiris-clang:6.0.0',
        file = 'Clang'
    )
    PYTHON = _meta(
        full = 'Python',
        version = '3.6.5',
        image = 'osiris-python:3.6.5-stretch',
        file = 'Python'
    )
    JAVA = _meta(
        full = 'Java',
        version = '10',
        image = 'osiris-java:10',
        file = 'Java'
    )