from typing import Dict, Optional, Any
from openllm_core._typing_compat import LiteralSerialisation, LiteralQuantise, LiteralString
from _openllm_tiny._llm import Dtype

model_id: str = ...
model_name: LiteralString = ...
model_tag: Optional[str] = ...
model_version: Optional[str] = ...
quantise: LiteralQuantise = ...
serialisation: LiteralSerialisation = ...
dtype: Dtype = ...
trust_remote_code: bool = ...
max_model_len: Optional[int] = ...
gpu_memory_utilization: int = ...
services_config: Dict[str, Any] = ...