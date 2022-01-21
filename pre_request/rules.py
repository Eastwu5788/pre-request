# -*- coding: utf-8 -*-
# sys
import typing as t
from datetime import datetime
from decimal import Decimal


class Rule:  # pylint: disable=too-many-instance-attributes
    """ This class is designed to describe special rule that params must follow
    """

    def __init__(self, **kwargs):
        # Type
        self.direct_type: t.Type[t.Any] = kwargs.get("type", str)

        # Flask
        self.location: t.Optional[t.Union[t.List[str], str]] = kwargs.get("location", None)

        # Strings
        self.len: t.Optional[int] = kwargs.get("len", None)
        self.trim: bool = kwargs.get("trim", False)
        self.reg: t.Optional[str] = kwargs.get("reg", None)
        self.contains: t.List[t.Any] = kwargs.get("contains", [])
        self.contains_any: t.List[t.Any] = kwargs.get("contains_any", [])
        self.excludes: t.List[t.Any] = kwargs.get("excludes", [])
        self.startswith: t.Optional[str] = kwargs.get("startswith", None)
        self.endswith: t.Optional[str] = kwargs.get("endswith", None)
        self.lower: bool = kwargs.get("lower", False)
        self.upper: bool = kwargs.get("upper", False)
        self.split: t.Optional[str] = kwargs.get("split", None)

        # Network
        self.ipv4: bool = kwargs.get("ipv4", False)
        self.ipv6: bool = kwargs.get("ipv6", False)
        self.mac: bool = kwargs.get("mac", False)

        # Format
        self.skip: bool = kwargs.get("skip", False)
        self.deep: bool = kwargs.get("deep", True)
        self.multi: bool = kwargs.get("multi", False)
        self.structure: t.Optional[t.Dict[str, t.Union[dict, "Rule"]]] = kwargs.get("structure", None)
        self.latitude: bool = kwargs.get("latitude", False)
        self.longitude: bool = kwargs.get("longitude", False)
        self.fmt: t.Optional[str] = kwargs.get("fmt", "%Y-%m-%d %H:%M:%S")

        # Field
        self.eq_key: t.Optional[str] = kwargs.get("eq_key", None)
        self.neq_key: t.Optional[str] = kwargs.get("neq_key", None)
        self.gt_key: t.Optional[str] = kwargs.get("gt_key", None)
        self.gte_key: t.Optional[str] = kwargs.get("gte_key", None)
        self.lt_key: t.Optional[str] = kwargs.get("lt_key", None)
        self.lte_key: t.Optional[str] = kwargs.get("lte_key", None)

        # Comparisons
        self.eq: t.Optional[t.Any] = kwargs.get("eq", None)
        self.neq: t.Optional[t.Any] = kwargs.get("neq", None)
        self.gt: t.Optional[int] = kwargs.get("gt", None)
        self.gte: t.Optional[int] = kwargs.get("gte", None)
        self.lt: t.Optional[int] = kwargs.get("lt", None)
        self.lte: t.Optional[int] = kwargs.get("lte", None)

        # Other
        self.default: t.Optional[t.Any] = kwargs.get("default", None)
        self.enum: t.List[t.Any] = kwargs.get("enum", [])
        self.required: bool = kwargs.get("required", True)
        self.required_with: t.Optional[str] = kwargs.get("required_with", None)
        self.key_map: t.Optional[str] = kwargs.get("dest", None)
        self.json_load: bool = kwargs.get("json", False)
        self.callback: t.Optional[t.Callable] = kwargs.get("callback", None)

    @property
    def gt(self):
        return self._gt

    @gt.setter
    def gt(self, value):
        """ Add input value type check

        :param value: User input gt value
        """
        # Ignore None
        if value is None:
            self._gt = value
            return

        # check input value type
        if not isinstance(value, (int, float, Decimal, datetime)):
            raise TypeError("property `gt` must be type of int, or datetime, or float, or Decimal")

        self._gt = value

    @property
    def gte(self):
        return self._gte

    @gte.setter
    def gte(self, value):
        """ Add input value type check

        :param value: User input gte value
        """
        # Ignore None
        if value is None:
            self._gte = value
            return

        # check input value type
        if not isinstance(value, (int, float, Decimal, datetime)):
            raise TypeError("property `gte` must be type of int, or datetime, or float, or Decimal")

        self._gte = value

    @property
    def lt(self):
        return self._lt

    @lt.setter
    def lt(self, value):
        """ Add input value type check

        :param value: User input lt value
        """
        # Ignore None
        if value is None:
            self._lt = value
            return

        # check input value type
        if not isinstance(value, (int, float, Decimal, datetime)):
            raise TypeError("property `lt` must be type of int, or datetime, or float, or Decimal")

        self._lt = value

    @property
    def lte(self):
        return self._lte

    @lte.setter
    def lte(self, value):
        """ Add input value type check

        :param value: User input lte value
        """
        # Ignore None
        if value is None:
            self._lte = value
            return

        # check input value type
        if not isinstance(value, (int, float, Decimal, datetime)):
            raise TypeError("property `lte` must be type of int, or float, or Decimal, or datetime")

        self._lte = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        """ Add type check for key location
        """
        df_location = ["args", "form", "values", "headers", "cookies", "json"]

        if value is None:
            self._location = value
            return

        if not isinstance(value, str) and not isinstance(value, list):
            raise TypeError("location must be type of list or str")

        if not value:
            raise ValueError("location value is empty")

        if isinstance(value, str):
            value = [value]

        for location in value:
            if location not in df_location:
                raise ValueError("params `location` must be in %s" % df_location)

        self._location = value

    @property
    def structure(self):
        return self._structure

    @structure.setter
    def structure(self, value):
        """ Params structure must be type of dict
        """
        if value is None:
            self._structure = value
            return

        if not isinstance(value, dict):
            raise TypeError("structure must be type of dict")

        if not value:
            raise TypeError("structure can not empty")

        self._structure = value
