import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
  name='chat.proto',
  package='grpc',
  syntax='proto3',
  serialized_pb=_b('\n\nchat.proto\x12\x04grpc\"\x07\n\x05\x45mpty\"%\n\x04Note\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t2Z\n\nChatServer\x12\'\n\nChatStream\x12\x0b.grpc.Empty\x1a\n.grpc.Note0\x01\x12#\n\x08SendNote\x12\n.grpc.Note\x1a\x0b.grpc.Emptyb\x06proto3')
)

_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='grpc.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=27,
)

_NOTE = _descriptor.Descriptor(
  name='Note',
  full_name='grpc.Note',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='grpc.Note.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='grpc.Note.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=66,
)

DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
DESCRIPTOR.message_types_by_name['Note'] = _NOTE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'chat_pb2'
  ))
_sym_db.RegisterMessage(Empty)

Note = _reflection.GeneratedProtocolMessageType('Note', (_message.Message,), dict(
  DESCRIPTOR = _NOTE,
  __module__ = 'chat_pb2'
  ))
_sym_db.RegisterMessage(Note)

_CHATSERVER = _descriptor.ServiceDescriptor(
  name='ChatServer',
  full_name='grpc.ChatServer',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=68,
  serialized_end=158,
  methods=[
  _descriptor.MethodDescriptor(
    name='ChatStream',
    full_name='grpc.ChatServer.ChatStream',
    index=0,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_NOTE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendNote',
    full_name='grpc.ChatServer.SendNote',
    index=1,
    containing_service=None,
    input_type=_NOTE,
    output_type=_EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CHATSERVER)

DESCRIPTOR.services_by_name['ChatServer'] = _CHATSERVER