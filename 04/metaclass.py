class CustomMeta(type):
    def __new__(cls, name, bases, classdict):
        attrs = {}

        def __setattr__(self, attr_name, attr_val):
            object.__setattr__(self, f"custom_{attr_name}", attr_val)

        for name, value in classdict.items():
            if not name[:2] == "__" and not name[-2:] == "__":
                attrs[f"custom_{name}"] = value
            else:
                attrs[name] = value

        cls = super().__new__(cls, name, bases, attrs)
        setattr(cls, __setattr__.__name__, __setattr__)
        return cls
