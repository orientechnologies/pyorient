__author__ = 'Ostico'

from BaseMessage import *
from Fields.SendingField import SendingField
from Fields.ReceivingField import ReceivingField
from Fields.OrientOperations import *
from Fields.OrientPrimitives import *
from pyorient.utils import *

class DbExistsMessage(BaseMessage):

    _db_name = ''
    _storage_type = STORAGE_TYPE_LOCAL

    def __init__(self, _orient_socket ):
        super( DbExistsMessage, self ).\
            __init__(_orient_socket)

        self._protocol = _orient_socket.protocol  # get from socket
        self._session_id = _orient_socket.session_id  # get from socket

        # order matters
        self.append( SendingField( ( BYTE, DB_EXIST ) ) )
        self.append( SendingField( ( INT, self._session_id ) ) )  # session_id

    def prepare(self, params=None):

        try:
            self._db_name = params[0]
            self._storage_type = params[1]  # user choice storage if present
        except IndexError:
            # Use default for non existent indexes
            pass

        if self.get_protocol() >= 6:
            self.append( SendingField( ( STRING, self._db_name ) ) )  # db_name

        if self.get_protocol() >= 16:
            # > 16 1.5-snapshot
            # custom choice server_storage_type
            self.append( SendingField( ( STRING, self._storage_type ) ) )

        return super( DbExistsMessage, self ).prepare()

    @need_connected
    def fetch_response(self):
        self._set_response_header_fields()
        self.append( ReceivingField( BOOLEAN ) )
        return super( DbExistsMessage, self ).fetch_response()[0]

    def set_db_name(self, db_name):
        self._db_name = db_name

    def set_storage_type(self, storage_type):
        self._storage_type = storage_type