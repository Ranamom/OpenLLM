#!/usr/bin/env python3
from __future__ import annotations
import os, typing as t, sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent

sys.path.insert(0, (_ROOT / 'openllm-core' / 'src').__fspath__())
sys.path.insert(1, (_ROOT / 'openllm-python' / 'src').__fspath__())
from openllm_core._configuration import LiteralRuntime
from openllm.models import auto
from openllm import CONFIG_MAPPING

if t.TYPE_CHECKING: from collections import OrderedDict

config_requirements = {k: [_.replace('-', '_') for _ in v.__openllm_requirements__] if v.__openllm_requirements__ else None for k, v in CONFIG_MAPPING.items()}
_dependencies: dict[LiteralRuntime, str] = {k: v for k, v in zip(LiteralRuntime.__args__, ('torch', 'tensorflow', 'flax', 'vllm'))}
_auto: dict[str, str] = {k: v for k, v in zip(LiteralRuntime.__args__, ('AutoLLM', 'AutoTFLLM', 'AutoFlaxLLM', 'AutoVLLM'))}

def get_target_dummy_file(framework: LiteralRuntime) -> Path:
  return _ROOT / 'openllm-python' / 'src' / 'openllm' / 'utils' / f'dummy_{framework}_objects.py'

def mapping_names(framework: LiteralRuntime):
  return 'MODEL_MAPPING_NAMES' if framework == 'pt' else f'MODEL_{framework.upper()}_MAPPING_NAMES'

def get_mapping(framework: LiteralRuntime) -> OrderedDict[t.Any, t.Any]:
  return getattr(auto, mapping_names(framework))

def make_class_stub(model_name: str, framework: LiteralRuntime, indentation: int = 2, auto: bool = False) -> list[str]:
  _dep_list: list[str] = [
      f'"{v}"' for v in [_dependencies[framework], *(t.cast(t.List[str], config_requirements[model_name]) if model_name != '__default__' and config_requirements[model_name] else [])]
  ]
  if auto: cl_ = _auto[framework]
  else: cl_ = get_mapping(framework)[model_name]
  lines = [
      f'class {cl_}(metaclass=_DummyMetaclass):',
      ' '*indentation + f"_backends=[{','.join(_dep_list)}]",
      ' '*indentation + f"def __init__(self,*param_decls:_t.Any,**attrs: _t.Any):_require_backends(self,[{','.join(_dep_list)}])"
  ]
  return lines

def write_stub(framework: LiteralRuntime, _path: str) -> list[str]:
  base = [
      f'# This file is generated by {_path}. DO NOT EDIT MANUALLY!',
      f'# To update this, run ./{_path}',
      'from __future__ import annotations',
      'import typing as _t',
      'from openllm_core.utils import DummyMetaclass as _DummyMetaclass, require_backends as _require_backends',
  ]
  base.extend([v for it in [make_class_stub(k, framework) for k in get_mapping(framework)] for v in it])
  # autoclass
  base.extend(make_class_stub('__default__', framework, auto=True))
  # mapping and export
  _imports = [f'"{v}"' for v in get_mapping(framework).values()]
  base += [f'{mapping_names(framework)}:_t.Any=None', f"__all__:list[str]=[\"{mapping_names(framework)}\",\"{_auto[framework]}\",{','.join(_imports)}]\n"]
  return base

def main() -> int:
  _path = os.path.join(os.path.basename(os.path.dirname(__file__)), os.path.basename(__file__))
  for framework in _dependencies:
    with get_target_dummy_file(framework).open('w') as f:
      f.write('\n'.join(write_stub(framework, _path)))
  return 0

if __name__ == '__main__': raise SystemExit(main())
