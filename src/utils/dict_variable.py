from typing import Dict


def var_name(var: Dict[str, list]):
	return list(var.keys())[0]


def var_value(var: Dict[str, list]):
	return list(var.values())[0]
