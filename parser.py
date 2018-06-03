from language import get_language


receive_transfer_field = {
    'submission_id' : 'submission'
}

def parse( ** kwargs ):
    for _ in receive_transfer_field:
        ori = _
        tr = receive_transfer_field[_]
        kwargs[tr] = kwargs[_]
        kwargs.pop( ori )
    kwargs['language'] = get_language( kwargs['language'] )
    return kwargs