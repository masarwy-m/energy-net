
import json
from pathlib import Path


ENV_CFG_FILE = Path(__file__).parent / 'test_env_configs.json'


def get_test_env_cfgs():
    with open(ENV_CFG_FILE, 'r') as f:
        env_cfgs = json.load(f)
    return env_cfgs


test_env_cfgs = get_test_env_cfgs()
single_agent_cfgs = {k: cfg for k, cfg in test_env_cfgs.items() if 'network_entities' not in cfg or len(cfg['network_entities']) == 1}