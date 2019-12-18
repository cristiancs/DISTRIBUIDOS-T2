import grpc
import chat_pb2 as chat__pb2

class ChatServerStub(object):

  pass

  def __init__(self, channel):
    self.ChatStream = channel.unary_stream(
        '/grpc.ChatServer/ChatStream',
        request_serializer=chat__pb2.Empty.SerializeToString,
        response_deserializer=chat__pb2.Note.FromString,
        )
    self.SendNote = channel.unary_unary(
        '/grpc.ChatServer/SendNote',
        request_serializer=chat__pb2.Note.SerializeToString,
        response_deserializer=chat__pb2.Empty.FromString,
        )


class ChatServerServicer(object):

  pass

  def ChatStream(self, request, context):
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SendNote(self, request, context):

    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

def add_ChatServerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ChatStream': grpc.unary_stream_rpc_method_handler(
          servicer.ChatStream,
          request_deserializer=chat__pb2.Empty.FromString,
          response_serializer=chat__pb2.Note.SerializeToString,
      ),
      'SendNote': grpc.unary_unary_rpc_method_handler(
          servicer.SendNote,
          request_deserializer=chat__pb2.Note.FromString,
          response_serializer=chat__pb2.Empty.SerializeToString,
      ),
  }
  
  generic_handler = grpc.method_handlers_generic_handler(
      'grpc.ChatServer', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
