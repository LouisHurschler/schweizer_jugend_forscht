# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: TimeSpanLog.proto
# Protobuf Python Version: 5.27.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 27, 1, "", "TimeSpanLog.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11TimeSpanLog.proto\x12\x12\x44\x61taLoggerProtobuf\x1a\x1fgoogle/protobuf/timestamp.proto"\xed\t\n\x0bTimeSpanLog\x12\n\n\x02id\x18\x01 \x01(\r\x12&\n\x04type\x18\x02 \x01(\x0e\x32\x18.DataLoggerProtobuf.Type\x12\x32\n\x0etimestamp_from\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0ctimestamp_to\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1f\n\x17L1_power_factor_average\x18\x05 \x01(\x05\x12\x1b\n\x13L1_power_factor_min\x18\x06 \x01(\x05\x12\x1b\n\x13L1_power_factor_max\x18\x07 \x01(\x05\x12\x1f\n\x17L2_power_factor_average\x18\x08 \x01(\x05\x12\x1b\n\x13L2_power_factor_min\x18\t \x01(\x05\x12\x1b\n\x13L2_power_factor_max\x18\n \x01(\x05\x12\x1f\n\x17L3_power_factor_average\x18\x0b \x01(\x05\x12\x1b\n\x13L3_power_factor_min\x18\x0c \x01(\x05\x12\x1b\n\x13L3_power_factor_max\x18\r \x01(\x05\x12\x19\n\x11measurement_count\x18\x0e \x01(\x05\x12\x1a\n\x12L1_voltage_average\x18\x0f \x01(\r\x12\x1a\n\x12L2_voltage_average\x18\x10 \x01(\r\x12\x1a\n\x12L3_voltage_average\x18\x11 \x01(\r\x12\x1a\n\x12L1_current_average\x18\x12 \x01(\r\x12\x1a\n\x12L2_current_average\x18\x13 \x01(\r\x12\x1a\n\x12L3_current_average\x18\x14 \x01(\r\x12\x16\n\x0eL1_voltage_max\x18\x15 \x01(\r\x12\x16\n\x0eL2_voltage_max\x18\x16 \x01(\r\x12\x16\n\x0eL3_voltage_max\x18\x17 \x01(\r\x12\x16\n\x0eL1_current_max\x18\x18 \x01(\r\x12\x16\n\x0eL2_current_max\x18\x19 \x01(\r\x12\x16\n\x0eL3_current_max\x18\x1a \x01(\r\x12\x16\n\x0eL1_voltage_min\x18\x1b \x01(\r\x12\x16\n\x0eL2_voltage_min\x18\x1c \x01(\r\x12\x16\n\x0eL3_voltage_min\x18\x1d \x01(\r\x12\x16\n\x0eL1_current_min\x18\x1e \x01(\r\x12\x16\n\x0eL2_current_min\x18\x1f \x01(\r\x12\x16\n\x0eL3_current_min\x18  \x01(\r\x12\x1a\n\x12L1_apparent_energy\x18! \x01(\x12\x12\x1a\n\x12L2_apparent_energy\x18" \x01(\x12\x12\x1a\n\x12L3_apparent_energy\x18# \x01(\x12\x12\x11\n\tsensor_id\x18$ \x01(\x05\x12\x18\n\x10L1_active_energy\x18% \x01(\x12\x12\x18\n\x10L2_active_energy\x18& \x01(\x12\x12\x18\n\x10L3_active_energy\x18\' \x01(\x12\x12\x1a\n\x12L1_reactive_energy\x18( \x01(\x12\x12\x1a\n\x12L2_reactive_energy\x18) \x01(\x12\x12\x1a\n\x12L3_reactive_energy\x18* \x01(\x12\x12\x19\n\x11\x66requency_average\x18+ \x01(\r\x12\x15\n\rfrequency_max\x18, \x01(\r\x12\x15\n\rfrequency_min\x18- \x01(\r*C\n\x04Type\x12\x11\n\rtype_1_second\x10\x00\x12\x13\n\x0ftype_30_seconds\x10\x01\x12\x13\n\x0ftype_15_minutes\x10\x02\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "TimeSpanLog_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_TYPE"]._serialized_start = 1338
    _globals["_TYPE"]._serialized_end = 1405
    _globals["_TIMESPANLOG"]._serialized_start = 75
    _globals["_TIMESPANLOG"]._serialized_end = 1336
# @@protoc_insertion_point(module_scope)