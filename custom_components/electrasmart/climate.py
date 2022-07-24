import json

from typing import Dict, List

from .const import OperationMode, Feature


class ElectraAirConditioner(object):
    def __init__(self, data) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.regdate: str = data["regdate"]
        self.model = data["model"]
        self.mac: str = data["mac"]
        self.serial_number: str = data["sn"]
        self.manufactor: str = data["manufactor"]
        self.type: str = data["deviceTypeName"]
        self.status: str = data["status"]
        self.token: str = data["deviceToken"]
        self._time_delta: int = 0
        self.features: List[Feature] = []

        self.current_mode: str = None
        self.collected_measure: int = None
        self._oper_data: Dict = None

    def is_disconnected(self, thresh_sec: int = 60) -> bool:
        return self._time_delta > thresh_sec

    def update_features(self) -> None:
        if "VSWING" in self._oper_data:
            self.features.append(Feature.V_SWING)
        if "HSWING" in self._oper_data:
            self.features.append(Feature.H_SWING)

    def get_sensor_temperature(self) -> int:
        return self.collected_measure

    def get_mode(self) -> str:
        return self._oper_data["AC_MODE"]

    def set_mode(self, mode: str) -> None:
        if mode in [
            OperationMode.MODE_AUTO,
            OperationMode.MODE_COOL,
            OperationMode.MODE_DRY,
            OperationMode.MODE_FAN,
            OperationMode.MODE_HEAT,
        ]:
            if mode != self._oper_data["AC_MODE"]:
                self._oper_data["AC_MODE"] = mode

    def set_horizontal_swing(self, enable: bool):
        if "HSWING" in self._oper_data:
            self._oper_data["HSWING"] = (
                OperationMode.ON if enable else OperationMode.OFF
            )

    def set_vertical_swing(self, enable: bool):
        if "VSWING" in self._oper_data:
            self._oper_data["VSWING"] = (
                OperationMode.ON if enable else OperationMode.OFF
            )

    def is_vertical_swing(self):
        if "VSWING" in self._oper_data:
            return self._oper_data["VSWING"] == OperationMode.ON
        return False

    def is_horizontal_swing(self):
        if "HSWING" in self._oper_data:
            return self._oper_data["HSWING"] == OperationMode.ON
        return False

    def is_on(self):
        if "TURN_ON_OFF" in self._oper_data:
            return self._oper_data["TURN_ON_OFF"] == OperationMode.ON
        else:
            return self._oper_data["AC_MODE"] != OperationMode.STANDBY

    def turn_on(self):
        if not self.is_on():
            if "TURN_ON_OFF" in self._oper_data:
                self._oper_data["TURN_ON_OFF"] = OperationMode.ON

    def turn_off(self):
        if self.is_on():
            if "TURN_ON_OFF" in self._oper_data:
                self._oper_data["TURN_ON_OFF"] = OperationMode.OFF
            else:
                self._oper_data["AC_MODE"] = OperationMode.STANDBY

    def get_temperature(self):
        return int(self._oper_data["SPT"])

    def set_temperature(self, val: int):
        if self.get_temperature() != val:
            self._oper_data["SPT"] = str(val)

    def get_fan_speed(self):
        return self._oper_data["FANSPD"]

    def set_fan_speed(self, speed):
        if speed in [
            OperationMode.FAN_SPEED_AUTO,
            OperationMode.FAN_SPEED_HIGH,
            OperationMode.FAN_SPEED_MED,
            OperationMode.FAN_SPEED_LOW,
        ]:
            if speed != self._oper_data["FANSPD"]:
                self._oper_data["FANSPD"] = speed

    def set_turbo_mode(self, enable: bool):
        self._oper_data["TURBO"] = OperationMode.ON if enable else OperationMode.OFF

    def get_turbo_mode(self):
        return self._oper_data["SHABAT"] == OperationMode.ON

    def set_shabat_mode(self, enable: bool):
        self._oper_data["SHABAT"] = OperationMode.ON if enable else OperationMode.OFF

    def get_shabat_mode(self):
        return self._oper_data["SHABAT"] == OperationMode.ON

    def update_operation_states(self, data):
        self._oper_data = json.loads(data["commandJson"]["OPER"])["OPER"]
        self._time_delta = data["timeDelta"]
        measurments = json.loads(data["commandJson"]["DIAG_L2"])["DIAG_L2"]
        if "I_RAT" in measurments:
            self.collected_measure = int(measurments["I_RAT"])
        if "I_CALC_AT" in measurments:
            self.collected_measure = int(measurments["I_CALC_AT"])

        self.current_mode = measurments["O_ODU_MODE"]

    def get_operation_state(self):
        if "AC_STSRC" in self._oper_data:
            self._oper_data["AC_STSRC"] = "WI-FI"

        json_state = json.dumps({"OPER": self._oper_data})
        return json_state
