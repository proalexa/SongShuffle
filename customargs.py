from sys import argv


class ArgParser:
    def __init__(self, description):
        self.description = description
        self.optional = []
        self.required = []

    def add_argument(self, name, prefix, storetype, optional):
        if optional:
            self.optional.append(Arg(name, prefix, storetype))
        else:
            self.required.append(Arg(name, prefix, storetype))
        return 0

    def parse(self):
        resdict = {}
        {key: None for key in self.required+self.optional}
        for id, i in enumerate(self.optional+self.required):
            if i.prefix in argv[1:]:
                print(i.name)
                if i.storetype == bool:
                    resdict[i.name] = True
                else:
                    try:
                        resdict[i.name] = argv[id+2]
                    except:
                        self.usage()
            else:
                self.usage()
        return resdict

    def usage(self):
        print("Usage!")
        exit()


class Arg:
    def __init__(self, name, prefix, storetype):
        self.name = name
        self.prefix = prefix
        self.storetype = storetype


bla = ArgParser(description="Hi")
bla.add_argument("add", "add", str, True)
bla.add_argument("--autoplay", "autoplay", bool, False)
print(bla.parse())
# Do not use still in alpha.
# Lots of bugs.
# Closer to pseudo code that has stupid algorithm.
