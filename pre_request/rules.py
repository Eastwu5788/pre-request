# -*- coding: utf-8 -*-
from datetime import datetime


class Rule:  # pylint: disable=too-many-instance-attributes
    """ This class is designed to describe special rule that params must follow
    """

    def __init__(self, **kwargs):
        self.location = kwargs.get("location", None)
        self.direct_type = kwargs.get("type", str)
        self.skip = kwargs.get("skip", False)
        self.deep = kwargs.get("deep", True)
        self.multi = kwargs.get("multi", False)

        self.required = kwargs.get("required", True)
        self.required_with = kwargs.get("required_with", None)

        self.default = kwargs.get("default", None)
        self.trim = kwargs.get("trim", False)

        self.enum = kwargs.get("enum", list())

        self.reg = kwargs.get("reg", None)

        self.email = kwargs.get("email", False)
        self.mobile = kwargs.get("mobile", False)

        self.contains = kwargs.get("contains", list())
        self.contains_any = kwargs.get("contains_any", list())
        self.excludes = kwargs.get("excludes", list())
        self.startswith = kwargs.get("startswith", None)
        self.endswith = kwargs.get("endswith", None)
        self.lower = kwargs.get("lower", False)
        self.upper = kwargs.get("upper", False)
        # self.file = kwargs.get("file", False)
        self.split = kwargs.get("split", None)

        self.ipv4 = kwargs.get("ipv4", False)
        self.ipv6 = kwargs.get("ipv6", False)
        self.mac = kwargs.get("mac", False)

        self.latitude = kwargs.get("latitude", False)
        self.longitude = kwargs.get("longitude", False)

        self.fmt = kwargs.get("fmt", "%Y-%m-%d %H:%M:%S")

        self.eq_key = kwargs.get("eq_key", None)
        self.neq_key = kwargs.get("neq_key", None)
        self.gt_key = kwargs.get("gt_key", None)
        self.gte_key = kwargs.get("gte_key", None)
        self.lt_key = kwargs.get("lt_key", None)
        self.lte_key = kwargs.get("lte_key", None)

        self.eq = kwargs.get("eq", None)
        self.neq = kwargs.get("neq", None)

        self.gt = kwargs.get("gt", None)
        self.gte = kwargs.get("gte", None)
        self.lt = kwargs.get("lt", None)
        self.lte = kwargs.get("lte", None)

        self.key_map = kwargs.get("dest", None)

        self.json_load = kwargs.get("json", False)

        self.callback = kwargs.get("callback", None)

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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `gt` must be type of int datetime or float")

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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `gte` must be type of int datetime or float")

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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `lt` must be type of int datetime or float")

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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `lte` must be type of int or float")

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
